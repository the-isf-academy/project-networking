# closest_astroid.py
# by Jacob Wolf
#
# Example uasage of the NASA Near Earth Objects (Neo) API that finds the closest object that passes
# by the Earth on a given day.
#
# An example JSON returned by the Neo Feed Endpoint is included at the end of the file.

import requests

api_base_address = "https://api.nasa.gov/neo/rest/v1/"
feed_endpoint = "feed"
api_key = "DEMO_KEY"


def get_neos_for_date_range(start, end):
    # setting the parameters for the requests
    address = api_base_address + feed_endpoint
    params = {
        "start_date": start,
        "end_date": end,
        "api_key": api_key
    }
    # making the requests
    r = requests.get(address, params=params)

    # parsing the requests
    if r.ok:
        r_json = r.json()
        neo_dict = r_json["near_earth_objects"]
        neo_list = neo_dict[start]
        # returning the request
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
            if miss_distance_km < closest_approach_distance:
                closest_close_approach = close_approach
                closest_approach_distance = miss_distance_km
        # compare miss distance of this neo to the smallest miss distance of the neos we've seen so far
        miss_distance_km = closest_approach_distance
        if miss_distance_km < closest_miss_distance:
            closest_neo = neo
            closest_miss_distance = miss_distance_km
            closest_neo_closest_approach = closest_close_approach
    return closest_neo, closest_neo_closest_approach

print("This script finds the nearest astroid to pass earth on a particular date using the NASA Neo API. ☄️")
date = input("What date would you like to search for? (YYYY-MM-DD) ")
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



""" Example response from NASA Neo API:
{
    "element_count": 18,
    "links": {
        "next": "http://www.neowsapp.com/rest/v1/feed?start_date=2020-12-04&end_date=2020-12-04&detailed=false&api_key=DEMO_KEY",
        "prev": "http://www.neowsapp.com/rest/v1/feed?start_date=2020-12-02&end_date=2020-12-02&detailed=false&api_key=DEMO_KEY",
        "self": "http://www.neowsapp.com/rest/v1/feed?start_date=2020-12-03&end_date=2020-12-03&detailed=false&api_key=DEMO_KEY"
    },
    "near_earth_objects": {
        "2020-12-03": [
            {
                "absolute_magnitude_h": 22.2,
                "close_approach_data": [
                    {
                        "close_approach_date": "2020-12-03",
                        "close_approach_date_full": "2020-Dec-03 03:11",
                        "epoch_date_close_approach": 1606965060000,
                        "miss_distance": {
                            "astronomical": "0.0969767703",
                            "kilometers": "14507518.276359261",
                            "lunar": "37.7239636467",
                            "miles": "9014553.8465133618"
                        },
                        "orbiting_body": "Earth",
                        "relative_velocity": {
                            "kilometers_per_hour": "22963.3002511518",
                            "kilometers_per_second": "6.3786945142",
                            "miles_per_hour": "14268.5017588337"
                        }
                    }
                ],
                "estimated_diameter": {
                    "feet": {
                        "estimated_diameter_max": 707.9865871058,
                        "estimated_diameter_min": 316.6212271853
                    },
                    "kilometers": {
                        "estimated_diameter_max": 0.2157943048,
                        "estimated_diameter_min": 0.096506147
                    },
                    "meters": {
                        "estimated_diameter_max": 215.7943048444,
                        "estimated_diameter_min": 96.5061469579
                    },
                    "miles": {
                        "estimated_diameter_max": 0.134088323,
                        "estimated_diameter_min": 0.059966121
                    }
                },
                "id": "3015694",
                "is_potentially_hazardous_asteroid": false,
                "is_sentry_object": false,
                "links": {
                    "self": "http://www.neowsapp.com/rest/v1/neo/3015694?api_key=DEMO_KEY"
                },
                "name": "(1998 VD32)",
                "nasa_jpl_url": "http://ssd.jpl.nasa.gov/sbdb.cgi?sstr=3015694",
                "neo_reference_id": "3015694"
            },
        ]
    }
}
"""
