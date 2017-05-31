#!/usr/bin/env python3

import click
import random
import math
import itertools


passenger_rates = [
    {
        "high": 6000,
        "middle": 3000,
        "low": 1000
    },
    {
        "high": 12000,
        "middle": 6000,
        "low": 1200
    },
    {
        "high": 20000,
        "middle": 10000,
        "low": 1400
    },
    {
        "high": 30000,
        "middle": 15000,
        "low": 1600
    },
    {
        "high": 40000,
        "middle": 20000,
        "low": 1800
    },
    {
        "high": 50000,
        "middle": 25000,
        "low": 2000
    }
]

passenger_traffic = {
    "agricultural": {
        "current": 0,
        "destination": 0
    },
    "asteroid": {
        "current": 1,
        "destination": -1
    },
    "barren": {
        "current": -5,
        "destination": -5
    },
    "dessert": {
        "current": -1,
        "destination": -1
    },
    "fluid oceans": {
        "current": 0,
        "destination": 0
    },
    "garden": {
        "current": 2,
        "destination": 2
    },
    "high population": {
        "current": 0,
        "destination": 4
    },
    "ice-capped": {
        "current": 1,
        "destination": -1
    },
    "industrial": {
        "current": 2,
        "destination": 1
    },
    "low population": {
        "current": 0,
        "destination": -4
    },
    "non-agricultural": {
        "current": 0,
        "destination": 0
    },
    "poor": {
        "current": -2,
        "destination": -1
    },
    "rich": {
        "current": -1,
        "destination": 2
    },
    "water world": {
        "current": 0,
        "destination": 0
    },
    "amber zone": {
        "current": 2,
        "destination": -2
    },
    "red zone": {
        "current": 4,
        "destination": -4
    },
    "no classification": {
        "current": 0,
        "destination": 0
    },
}

availiable_passengers = {
    0: {
        "low": lambda: 0,
        "med": lambda: 0,
        "high": lambda: 0
    },
    1: {
        "low": lambda: roll(2, -6),
        "med": lambda: roll(1, -6),
        "high": lambda: 0
    },
    2: {
        "low": lambda: roll(2),
        "med": lambda: roll(1),
        "high": lambda: roll(1, -roll(1))
    },
    3: {
        "low": lambda: roll(2),
        "med": lambda: roll(2, -roll(1)),
        "high": lambda: roll(2, -roll(2))
    },
    4: {
        "low": lambda: roll(3, -6),
        "med": lambda: roll(2, -roll(1)),
        "high": lambda: roll(2, -roll(1))
    },
    5: {
        "low": lambda: roll(3, -roll(1)),
        "med": lambda: roll(3, -roll(2)),
        "high": lambda: roll(2, -roll(1))
    },
    6: {
        "low": lambda: roll(3),
        "med": lambda: roll(3, -roll(2)),
        "high": lambda: roll(3, -roll(2))
    },
    7: {
        "low": lambda: roll(3),
        "med": lambda: roll(3, -roll(1)),
        "high": lambda: roll(3, -roll(2))
    },
    8: {
        "low": lambda: roll(4),
        "med": lambda: roll(3, -roll(1)),
        "high": lambda: roll(3, -roll(1))
    },
    9: {
        "low": lambda: roll(4),
        "med": lambda: roll(3),
        "high": lambda: roll(3, -roll(1))
    },
    10: {
        "low": lambda: roll(5),
        "med": lambda: roll(3),
        "high": lambda: roll(3, -roll(1))
    },
    11: {
        "low": lambda: roll(5),
        "med": lambda: roll(4),
        "high": lambda: roll(3)
    },
    12: {
        "low": lambda: roll(6),
        "med": lambda: roll(4),
        "high": lambda: roll(3)
    },
    13: {
        "low": lambda: roll(6),
        "med": lambda: roll(4),
        "high": lambda: roll(4)
    },
    14: {
        "low": lambda: roll(7),
        "med": lambda: roll(5),
        "high": lambda: roll(4)
    },
    15: {
        "low": lambda: roll(8),
        "med": lambda: roll(5),
        "high": lambda: roll(4)
    },
    16: {
        "low": lambda: roll(9),
        "med": lambda: roll(6),
        "high": lambda: roll(5)
    }
}

def calc_effect(roll):
    return roll - 8

def roll(num_dice, mod=0):
    s = sum([ random.randint(1,6) for x in range(num_dice) ])
    return s + mod

@click.group()
def cli(): pass

@click.command()
@click.option('--distance', default=1)
@click.option('--dm', default=0)
@click.option('--current', default=None, help="The types of the current world, comma separated")
@click.option('--destination', default=None, help="The types of the destination world, comma separated")
@click.option("--staterooms", default=None)
@click.option("--low-berths", default=None)
@click.option("--steward-level", default=0)
def passengers(distance, dm, current, destination, staterooms, low_berths, steward_level):
    """
    Helps calculate the number of passengers availiable for ferrying between two planets.
    """

    if not current:
        click.echo("ERROR: current must be provided. See 'trav passengers --help' for details")
        exit()
    current = current.lower().replace(", ", ",")

    if not destination:
        click.echo("ERROR: destination must be provided. See 'trav passengers --help' for details")
        exit()
    destination = destination.lower().replace(", ", ",")

    streetwise_check = roll(2, dm)
    click.echo("Streetwise/Carouse Check (2d6 + {0}):".format(dm))
    click.echo("|-> Roll:{0}".format(streetwise_check))

    effect = calc_effect(streetwise_check)
    click.echo("|-> Calculated Effect: {0}".format(effect))

    click.echo("")
    click.echo("World Modifiers:")

    current_mod_total = 0
    click.echo("|-> Current:")
    for wtype in current.split(","):
        current_mod = passenger_traffic[wtype]["current"]
        current_mod_total += current_mod
        click.echo("| |-> {0}{1}: {2}".format(
            wtype[0].upper(), 
            wtype[1:], 
            current_mod))
    click.echo("| |-> TOTAL: {0}".format(current_mod_total))
    click.echo("|")

    dest_mod_total = 0
    click.echo("|-> Destination:")
    for wtype in destination.split(","):
        dest_mod = passenger_traffic[wtype]["destination"]
        dest_mod_total += dest_mod
        click.echo("| |-> {0}{1}: {2}".format(
            wtype[0].upper(), 
            wtype[1:], 
            dest_mod))
    click.echo("| |-> TOTAL: {0}".format(dest_mod_total))

    click.echo("")
    click.echo("Total Modifiers:")
    effect = math.floor(effect/2)
    click.echo("|-> Effect Modifier (half of effect): {0}".format(effect))
    click.echo("|-> Current World Modifier: {0}".format(current_mod_total))
    click.echo("|-> Destination World Modifier: {0}".format(dest_mod_total))
    mod = effect + current_mod_total + dest_mod_total
    click.echo("|-> TOTAL: {0}".format(dest_mod_total))

    # keep mod in sane bounds for availiablity table
    mod = mod if mod > 0 else 0
    mod = mod if mod <= 16 else 16

    avail= availiable_passengers[mod]
    high = avail["high"]()
    med = avail["med"]()
    low = avail["low"]()

    # correct for negatives 
    high = high if high > 0 else 0
    med = med if med > 0 else 0
    low = low if low > 0 else 0

    click.echo("")
    click.echo("Availiable Passengers:")
    click.echo("|-> High: {0}".format(high))
    click.echo("|-> Medium: {0}".format(med))
    click.echo("|-> Low Berth: {0}".format(low))


    optimize = False
    optimized_staterooms = False
    optimized_low_berths = False

    steward_level += 1 # account for lvl 0 counting as well

    rates = passenger_rates[distance - 1]
    high_rate = rates["high"]
    med_rate = rates["middle"]
    low_rate = rates["low"]

    if staterooms is not None:
        staterooms = int(staterooms)
        optimize = True
        optimized_staterooms = True

        taken = 0
        high_taken = 0
        med_taken = 0

        best_option = { 
            "high": 0, 
            "med": 0, 
            "income": 0 
        }

        for combo in itertools.combinations_with_replacement("hm ", steward_level):
                m_count = combo.count("m") * 5
                h_count = combo.count("h") * 2
                
                if(m_count > med ):  # if m*5 is more than there are, take all availiable
                    m_count = med

                if(h_count > high):
                    h_count = high

                income = (m_count * med_rate) + (h_count * high_rate)


                if(best_option["income"] < income):
                    best_option["income"] = income
                    best_option["high"] = h_count
                    best_option["med"] = m_count

        high_taken = best_option["high"]
        med_taken = best_option["med"]




    if low_berths is not None:
        low_berths = int(low_berths)
        optimize = True
        optimized_low_berths = True

        low_taken = 0
        taken = 0

        while(taken < low_berths):
            if(low_taken < low):
                low_taken += 1
                taken += 1
            else:
                # no more low berths left
                break


    if optimize:
        click.echo("")
        click.echo("Passenger Optimization:")




        if optimized_staterooms:
            high_sum = high_taken * high_rate
            click.echo("|-> High Passengers: {0} * {1} = {2} CR".format(
                high_taken, high_rate, high_sum ))

            med_sum = med_taken * med_rate
            click.echo("|-> Medium Passengers: {0} * {1} = {2} CR".format(
                med_taken, med_rate, med_sum))
        else:
            high_sum = 0
            med_sum = 0
            click.echo("|-> High Passengers: no staterooms availiable")
            click.echo("|-> Medium Passengers: no staterooms availiable")

        if optimized_low_berths:
            low_sum = low_taken * low_rate
            click.echo("|-> Low Berth Passengers: {0} * {1} = {2} CR".format(
                low_taken, low_rate, low_sum))
        else:
            low_sum = 0
            click.echo("|-> Low Berth Passengers: no low berth pods availiable")

        click.echo("|-> TOTAL INCOME: {0} CR".format(low_sum + med_sum + high_sum))
            






cli.add_command(passengers)




if __name__ == "__main__":
    cli()
