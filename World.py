import random

debugger = False


# returns roll
def roll_dice(quantity, dice_type, modification=0):
    total = 0
    if debugger:
        print("\nrolling " + str(quantity) + "d" + str(dice_type) + " + " + str(modification))
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
        else:
            self.size = roll_dice(1, 10)
            self.starport_quality = ""
            self.atmosphere_type = check_bounded_value(roll_dice(2, 6, -7) + self.size, 0, 10)
            self.temperature = roll_dice(2, 6) + temperature_dice_modifier(self.atmosphere_type)
            self.hydrographic_percentage = 0
            self.population = 0
            self.government_type = 0
            self.law_level = 0
            self.tech_level = 0
            self.list_of_bases = []
            self.trade_codes = []
            self.travel_code = ""

    def __str__(self):
        return "\nSize: " + str(self.size) \
               + "\nAtmosphere Type: " + str(self.atmosphere_type) \
               + "\nTemperature: " + str(self.temperature)





# temp testing code
x = World()
print(x)

# print(str(temperature_dice_modifier(11, True)))
#