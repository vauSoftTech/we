#!/usr/bin/env python3
# -*- coding: utf_8 -*-
"""

    Copyright    : 2020 August 9. A. R. Bhatt.
    Organization : VAU SoftTech
    Project      : to study wobbling of earth
    Script Name  : we.py
    License      : GNU General Public License v3.0


    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""

from datetime import datetime, timedelta

prompt_text_event_type = """
WELCOME TO EARTH WOBBLING CALCULATOR PROGRAM
============================================
Please select event type you want to calculate wobbling for
a.) Summer Equinox
b.) Summer Solstice
c.) Winter Equinox
d.) Winter Solstice
x.) Exit

Please enter your choice as "A" to "E" or "X" to exit.
"""

prompt_text_number_of_years = """
Please enter number of years for which calculation should be performed.
(If you do not enter anything, default calculation is for 500 years from the
starting year.)
"""

prompt_text_starting_year = """
Please enter year from which calculation should be started.
(NOTE :- If you do not enter anything, default year is {} years in the past from
the date of current year.)
"""

prompt_text_sun_event_type = """
Please select Sun related event for which calculation should be performed.
a.) Sunrise
b.) Sun at Meridian
c.) Sunset
d.) Sun at Anti-Meridian

(NOTE :-
1. If you do not enter anything, default event for which calculation will
    be done is Sunrise.
2. All events will be calculated for the selected place - i.e. {}
)
"""


def accept_numeric_data_from_the_user(prompt, default, minimum_allowed, maximum_allowed):
    print(prompt)
    try:
        data = int(input("> "))
        while (data < minimum_allowed) or (data > maximum_allowed):
            print("Entered value must be within {} to {} both inclusive.".format(
                    minimum_allowed, maximum_allowed))
            data = int(input("> "))

    except ValueError:
        data = default

    return data


def accept_string_data_from_the_user(prompt, default, allowed_values):
    print(prompt)
    data = ""
    while data == "":
        data = input("> ").upper()
        if data == "":
            data = default
        else:
            if data not in allowed_values:
                print("Entered value is invalid.")
                data = ""
    return data


def get_place_information():
    return {"name": "Ahmedabad", "lat": "23.033863", "lon": "72.585022"}


def perform_calculations(uc_event, uc_noy, uc_st_y, uc_s_e):
    import ephem as ep

    place = ep.Observer()
    place.lat = get_place_information()["lat"]
    place.lon = get_place_information()["lon"]

    my_sun = ep.Sun(place)

    event_type_func_to_call = None
    if uc_event == "A":
        event_type_func_to_call = ep.next_spring_equinox
    elif uc_event == "B":
        event_type_func_to_call = ep.next_summer_solstice
    elif uc_event == "C":
        event_type_func_to_call = ep.next_autumn_equinox
    elif uc_event == "D":
        event_type_func_to_call = ep.next_winter_solstice
    else:
        exit()

    sun_event_type_to_call = None
    if uc_s_e == "A":
        sun_event_type_to_call = place.next_rising
    elif uc_s_e == "B":
        sun_event_type_to_call = place.next_transit
    elif uc_s_e == "C":
        sun_event_type_to_call = place.next_setting
    elif uc_s_e == "D":
        sun_event_type_to_call = place.next_antitransit
    else:
        exit()

    lst = []
    with open("result.txt", "w") as out_f:
        out_f.write("DATE&TIME,Year,TIME,AZIMUTH\n")
        for a_yr_no in range(uc_st_y, uc_st_y + uc_noy + 1):
            event_dt_tm = event_type_func_to_call(str(a_yr_no))
            place.date = event_dt_tm
            my_sun.compute(place)
            sun_event_dt_tm = sun_event_type_to_call(my_sun)
            place.date = sun_event_dt_tm
            my_sun.compute(place)
            lst.append((ep.localtime(sun_event_dt_tm), my_sun.az))
            out_f.write("{0:%Y-%m-%d %X}, {0:%Y},{0:%X},{1:}\n".format(ep.localtime(sun_event_dt_tm), my_sun.az))
            print(ep.localtime(sun_event_dt_tm), my_sun.az)

        out_f.write("Minimum\n")
        m = min(lst, key=lambda x: x[1])
        out_f.write("{:%Y-%m-%d %X},\t{}\n".format(m[0], m[1]))
        out_f.write("Maximum\n")
        m = max(lst, key=lambda x: x[1])
        out_f.write("{:%Y-%m-%d %X},\t{}\n".format(m[0], m[1]))
    return


def main():
    while True:
        user_choice_event_type = accept_string_data_from_the_user(prompt_text_event_type,
                                                                  "A",
                                                                  ("A", "B", "C", "D", "X"))
        if user_choice_event_type == "X":
            break

        while True:
            user_choice_number_of_years = 500
            user_choice_number_of_years = accept_numeric_data_from_the_user(prompt_text_number_of_years,
                                                                            user_choice_number_of_years, 10, 999)
            print(user_choice_number_of_years)

            while True:
                global prompt_text_starting_year
                prompt_text_starting_year = prompt_text_starting_year.format(user_choice_number_of_years //
                                                                             2)
                user_choice_starting_year = (datetime.now() - timedelta(days=365 * (user_choice_number_of_years //
                                                                                    2))).year
                user_choice_starting_year = accept_numeric_data_from_the_user(prompt_text_starting_year,
                                                                              user_choice_starting_year, 100, 3000)
                print(user_choice_starting_year)

                while True:
                    global prompt_text_sun_event_type
                    prompt_text_sun_event_type = prompt_text_sun_event_type.format(get_place_information()['name'])
                    user_choice_sun_event_type = accept_string_data_from_the_user(prompt_text_sun_event_type,
                                                                                  "A", ("A", "B", "C", "D"))
                    perform_calculations(
                            user_choice_event_type,
                            user_choice_number_of_years,
                            user_choice_starting_year,
                            user_choice_sun_event_type
                    )
                    break  # breaking out of fourth level inner loop
                break  # breaking out of third level inner loop

            print("Calculations have been done and saved to a file.\n\n\n")

            break  # breaking out of second level inner loop

    return None


if __name__ == '__main__':
    main()

