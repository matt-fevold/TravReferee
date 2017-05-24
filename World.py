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


def calculate_list_of_bases(starport_quality):
    """
    from page 178 calculates which bases exist according to starport quality level
    very ugly code but that is the cleanest way I can think of, the graph is complex.
    """
    list_of_bases = []
    if starport_quality in "A":
        roll = roll_dice(2, 6)
        if roll >= 8:
            list_of_bases.append("naval")
        roll = roll_dice(2, 6)
        if roll >= 10:
            list_of_bases.append("scout")
        roll = roll_dice(2, 6)
        if roll >= 8:
            list_of_bases.append("research")
        roll = roll_dice(2, 6)
        if roll >= 4:
            list_of_bases.append("tas")
        roll = roll_dice(2, 6)
        if roll >= 6:
            list_of_bases.append("imperial_consulate")

    if starport_quality in "B":
        roll = roll_dice(2, 6)
        if roll >= 8:
            list_of_bases.append("naval")
        roll = roll_dice(2, 6)
        if roll >= 8:
            list_of_bases.append("scout")
        roll = roll_dice(2, 6)
        if roll >= 10:
            list_of_bases.append("research")
        roll = roll_dice(2, 6)
        if roll >= 6:
            list_of_bases.append("tas")
        roll = roll_dice(2, 6)
        if roll >= 8:
            list_of_bases.append("imperial_consulate")
        roll = roll_dice(2, 6)
        if roll >= 12:
            list_of_bases.append("pirate")

    if starport_quality in "C":
        roll = roll_dice(2, 6)
        if roll >= 8:
            list_of_bases.append("scout")
        roll = roll_dice(2, 6)
        if roll >= 10:
            list_of_bases.append("research")
        roll = roll_dice(2, 6)
        if roll >= 10:
            list_of_bases.append("tas")
        roll = roll_dice(2, 6)
        if roll >= 10:
            list_of_bases.append("imperial_consulate")
        roll = roll_dice(2, 6)
        if roll >= 10:
            list_of_bases.append("pirate")

    if starport_quality in "D":
        roll = roll_dice(2, 6)
        if roll >= 7:
            list_of_bases.append("scout")
        roll = roll_dice(2, 6)
        if roll >= 12:
            list_of_bases.append("pirate")

    if starport_quality in "E":
        roll = roll_dice(2, 6)
        if roll >= 12:
            list_of_bases.append("pirate")
    if starport_quality in "X":
        list_of_bases.append("")

    return list_of_bases


def calculate_trade_codes(size, atmosphere_type, hydrographic_percentage, population, government_type,
                          law_level, tech_level):
    """
    messy table on page 181
    :param size:
    :param atmosphere_type:
    :param hydrographic_percentage:
    :param population:
    :param government_type:
    :param law_level:
    :param tech_level:
    :return:
    """
    trade_codes = []

    if (atmosphere_type in [4, 5, 6, 7, 8, 9]) and (hydrographic_percentage in [4, 5, 6, 7, 8])\
            and (population in [5, 6, 7]):
        trade_codes.append("Ag")

    if (size == 0) and (atmosphere_type == 0) and (hydrographic_percentage == 0):
        trade_codes.append("As")

    if (population == 0) and (government_type == 0) and (law_level == 0):
        trade_codes.append("Ba")

    if (atmosphere_type >= 2) and (hydrographic_percentage == 0):
        trade_codes.append("De")

    if (atmosphere_type >= 10) and (hydrographic_percentage >= 1):
        trade_codes.append("Fl")

    if (size >= 5) and (atmosphere_type in [4, 5, 6, 7, 8, 9]) and (hydrographic_percentage in [4, 5, 6, 7, 8]):
        trade_codes.append("Ga")

    if population >= 9:
        trade_codes.append("Hi")

    if tech_level >= 12:
        trade_codes.append("Ht")

    if (atmosphere_type in [0, 1]) and (hydrographic_percentage >= 1):
        trade_codes.append("IC")

    if (atmosphere_type in [0, 1, 2, 4, 7, 9]) and (population >= 9):
        trade_codes.append("In")

    if population in [1, 2, 3]:
        trade_codes.append("Lo")

    if tech_level >= 5:
        trade_codes.append("Lt")

    if (atmosphere_type <= 3) and (hydrographic_percentage <= 3) and (population >= 6):
        trade_codes.append("Na")

    if population in [4, 5, 6]:
        trade_codes.append("NI")

    if (atmosphere_type in [2, 3, 4, 5]) and (hydrographic_percentage <= 3):
        trade_codes.append("Po")

    if (atmosphere_type in [6, 8]) and (population in [6, 7, 8]):
        trade_codes.append("Ri")

    if atmosphere_type == 0:
        trade_codes.append("Va")

    if hydrographic_percentage == 10:
        trade_codes.append("Wa")

    return trade_codes


def calculate_travel_code(atmosphere, government_type, law_level):
    if atmosphere >= 10:
        return "A"
    if government_type in [0, 7, 10]:
        return "A"
    if law_level in [0, 9]:
        return "A"
    return "U"


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
            self.list_of_bases = calculate_list_of_bases(self.starport_quality)
            self.trade_codes = calculate_trade_codes(self.size, self.atmosphere_type, self.hydrographic_percentage,
                                                     self.population, self.government_type, self.law_level,
                                                     self.tech_level)
            self.travel_code = calculate_travel_code(self.atmosphere_type, self.government_type, self.law_level)

    def __str__(self):
        string_list_of_bases = ""
        for i in range(len(self.list_of_bases)):
            string_list_of_bases += self.list_of_bases[i] + " "

        string_trade_codes = ""
        for i in range(len(self.trade_codes)):
            string_trade_codes += self.trade_codes[i] + " "

        return "\nSize: " + str(self.size) \
               + "\nAtmosphere Type: " + str(self.atmosphere_type) \
               + "\nTemperature: " + str(self.temperature) \
               + "\nHydrographic Percentage: " + str(self.hydrographic_percentage) \
               + "\nPopulation: " + str(self.population)\
               + "\nGovernment Type: " + str(self.government_type) \
               + "\nLaw Level: " + str(self.law_level) \
               + "\nTech Level: " + str(self.tech_level) \
               + "\nTrade Codes: " + string_trade_codes \
               + "\nStarport Quality: " + self.starport_quality \
               + "\nBases: " + string_list_of_bases \
               + "\nTravel Code: " + self.travel_code

# temp testing code
x = World()
print(x)

# print(str(temperature_dice_modifier(11, True)))
#