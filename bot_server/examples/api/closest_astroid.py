# closest_astroid.py
# by Jacob Wolf
#
# Example uasage of the NASA Near Earth Objects (Neo) API that finds the closest object that passes
# by the Earth on a given day.
#
# An example JSON returned by the Neo Feed Endpoint is included at the end of the file.

import requests

api_base = "https://api.nasa.gov/neo/rest/v1/"
feed_endpoint = "feed"
api_key = "DEMO_KEY"

def get_neos_for_date_range(start, end):
   address = api_base + feed_endpoint
   params = {
        "start_date": start,
        "end_date": end,
        "api_key": api_key
    }
   r = requests.get(address, params=params)
   if r.ok:
       r_json = r.json()
       near_earth_objects_dict = r_json["near_earth_objects"]
       neo_list = near_earth_objects_dict[date]
       return neo_list
   else:
       return None

def find_closest_neo_from(neo_list):
    # find closest neo from list
    closest_neo = neo_list[0]
    closest_miss_distance = float(closest_neo["close_approach_data"][0]["miss_distance"]["kilometers"])
    closest_neo_closest_approach = closest_neo["close_approach_data"][0]
    for neo in neo_list:
        close_approach_list = neo["close_approach_data"]
        # find closest approach of a given neo
        closest_close_approach = close_approach_list[0]
        closest_approach_distance = float(closest_close_approach["miss_distance"]["kilometers"])
        for close_approach in close_approach_list:
            # compare miss distance of this approach to the smallest miss_distance of the approaches we've seen so far
            miss_distance_km = float(close_approach["miss_distance"]["kilometers"])
            print("name: {}. distance: {}".format(neo["name"], miss_distance_km))
            if miss_distance_km < closest_approach_distance:
                print("closer than previously found approach")
                closest_close_approach = close_approach
                closest_approach_distance = miss_distance_km
        # compare miss distance of this neo to the smallest miss distance of the neos we've seen so far
        miss_distance_km = closest_approach_distance
        if miss_distance_km < closest_miss_distance:
            print("closer than previously found neo")
            closest_neo = neo
            closest_miss_distance = miss_distance_km
            closest_neo_closest_approach = closest_close_approach
    return closest_neo, closest_neo_closest_approach

print("This script finds the nearest astroid to pass earth on a particular date using the NASA Neo API")
date = input("What date would you like to search for? (YYY-MM-DD) ")
neo_list = get_neos_for_date_range(date, date)
if neo_list:
    closest_neo, closest_approach = find_closest_neo_from(neo_list)
    neo_name = closest_neo["name"]
    miss_distance_km = closest_approach["miss_distance"]["kilometers"]
    concern = closest_neo["is_potentially_hazardous_asteroid"]
    print("The closest astroid to pass by Earth on {} is {}. It will miss Earth by {} kilometers.".format(date, neo_name, miss_distance_km))
    if concern:
        print("According to NASA, this astroid is potentially hazardous.")
    else:
        print("According to NASA, this astroid is not potentially hazardous.")
else:
    print("Error while getting data from NASA.")
