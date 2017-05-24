import random

debugger = False


# returns roll
def roll_dice(quantity, dice_type, modification=0, print_message=""):
    total = 0

    if debugger:
        print("\nRolling for: " + print_message)
        print("rolling " + str(quantity) + "d" + str(dice_type) + " + " + str(modification))
    for i in range(quantity):
        roll = random.randint(0, dice_type)
        if debugger:
            print("| -> " + str(roll))
        total += roll

    if debugger:
        print("Roll: " + str(total + modification))
    return total + modification


def temperature_dice_modifier(atmosphere, hot_edge=False, cold_edge=False):
    """
    returns the dm (which is semi complicated to calculate) based on table on page 171

    :param atmosphere: what kind of atmosphere it is.
    :param hot_edge: adds +4 to temp dm
    :param cold_edge: adds -4 to temp dm
    :return: returns the DM
    """
    dm = 0
    if atmosphere in [0, 1]:
        dm = 1000
        return dm
    if atmosphere in [2, 3]:
        dm -= 2
    if atmosphere in [4, 5, 14]:
        dm -= 1
    if atmosphere in [8, 9]:
        dm += 1
    if atmosphere in [10, 13, 15]:
        dm += 2
    if atmosphere in [11, 12]:
        dm += 6

    if hot_edge:
        dm += 4
    if cold_edge:
        dm -= 4

    return dm


def check_bounded_value(input_value, minimum_value, maximum_value):
    """
    This is for making sure values lie within a range
    """
    if input_value < minimum_value:
        if debugger:
            print("\nValue Below Minimum")
        return minimum_value
    else:

        if input_value > maximum_value:
            if debugger:
                print("\nValue Above Maximum")
            return maximum_value

        else:
            return input_value


def calculate_starport_quality():
    value = roll_dice(2, 6, 0, "starport quality")
    if value <= 2:
        return "X"
    if value in [3, 4]:
        return "E"
    if value in [5, 6]:
        return "D"
    if value in [7, 8]:
        return "C"
    if value in [9, 10]:
        return "B"
    if value >= 11:
        return "A"


def calculate_hydrographic_percentage(size, atmosphere_type, temperature):

    if size in [0, 1]:
        hydrographic_percentage = 0
    else:
        hydrographic_percentage = roll_dice(2, 6, size - 7, "hydro %")
        if atmosphere_type in [0, 1, 10, 11, 12]:
            hydrographic_percentage -= 4
        if atmosphere_type is not 13:  # if it is not dense atmosphere
            if temperature in [10, 11]:  # hot temp
                hydrographic_percentage -= 2
            if temperature >= 12:  # roasting temp
                hydrographic_percentage -= 6
    return hydrographic_percentage


def calculate_tech_level(starport_quality, size, atmosphere_type, hydrographic_percentage, population, government_type):
    dm = 0
    if starport_quality in "X":
        dm -= 4
    if starport_quality in "A":
        dm += 6
    if starport_quality in "B":
        dm += 4
    if starport_quality in "C":
        dm += 2

    if size in [0, 1]:
        dm += 2
    if size in [2, 3, 4]:
        dm += 1

    if atmosphere_type in [0, 1, 2, 3, 10, 11, 12, 13, 14, 15]:
        dm += 1

    if hydrographic_percentage in [0, 9]:
        dm += 1
    if hydrographic_percentage in [10]:
        dm += 2

    if population in [1, 2, 3, 4, 5, 9]:
        dm += 1
    if population in [10]:
        dm += 2
    if population in [11]:
        dm += 3
    if population in [12]:
        dm += 4

    if government_type in [0, 5]:
        dm += 1
    if government_type in [7]:
        dm += 2
    if government_type in [13, 14]:
        dm -= 2

    return roll_dice(1, 6, 0, "tech level") + dm



class World(object):
    def __init__(self, manual=None, size=None, starport_quality=None, atmosphere_type=None, temperature=None,
                 hydrographic_percentage=None, population=None, government_type=None,
                 law_level=None, tech_level=None, list_of_bases=None, trade_codes=None,
                 travel_code=None):
        if manual is not None:
            self.size = size
            self.starport_quality = starport_quality
            self.atmosphere_type = atmosphere_type
            self.temperature = temperature
            self.hydrographic_percentage = hydrographic_percentage
            self.population = population
            self.government_type = government_type
            self.law_level = law_level
            self.tech_level = tech_level
            self.list_of_bases = list_of_bases
            self.trade_codes = trade_codes
            self.travel_code = travel_code
        else:  # random generated world
            self.size = roll_dice(1, 10, 0, "size")
            self.starport_quality = calculate_starport_quality()  # could make this it's own object?
            self.atmosphere_type = check_bounded_value(roll_dice(2, 6, -7, "atmosphere") + self.size, 0, 10)
            self.temperature = roll_dice(2, 6, 0, "temperature") + temperature_dice_modifier(self.atmosphere_type)
            # there was too many characters for good style so following is broken up into two statements
            self.hydrographic_percentage = calculate_hydrographic_percentage(self.size, self.atmosphere_type,
                                                                             self.temperature)
            self.hydrographic_percentage = check_bounded_value(self.hydrographic_percentage, 0, 10)

            self.population = check_bounded_value(roll_dice(2, 6, -2, "population"), 0, 12)
            if population is 0:  # nobody for government!
                self.government_type = 0
                self.law_level = 0
                self.tech_level = 0
            else:
                self.government_type = check_bounded_value(roll_dice(2, 6, self.population - 7, "government type")
                                                           , 0, 13)
                self.law_level = check_bounded_value(roll_dice(2, 6, self.government_type - 7, "law level"), 0, 9)
                self.tech_level = calculate_tech_level(self.starport_quality, self.size, self.atmosphere_type,
                                                       self.hydrographic_percentage, self.population,
                                                       self.government_type)
            self.list_of_bases = []
            self.trade_codes = []
            self.travel_code = ""

    def __str__(self):
        return "\nSize: " + str(self.size) \
               + "\nAtmosphere Type: " + str(self.atmosphere_type) \
               + "\nTemperature: " + str(self.temperature) \
               + "\nHydrographic Percentage: " + str(self.hydrographic_percentage) \
               + "\nPopulation: " + str(self.population)\
               + "\nGovernment Type: " + str(self.government_type) \
               + "\nLaw Level: " + str(self.law_level) \
               + "\nTech Level: " + str(self.tech_level) \
               + "\nTrade Codes: " + "NOT IMPLEMENTED YET" \
               + "\nStarport Quality: " + self.starport_quality

# temp testing code
x = World()
print(x)

# print(str(temperature_dice_modifier(11, True)))
#