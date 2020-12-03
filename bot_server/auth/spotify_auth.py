# spotify_auth.py
#
# A function to authenticate for SPotify API and an example of how to use it

import requests
import base64
import secrets

def get_access_token(client_id, client_secret):
    """Given a client_id and client_secret for a Spotify app, returns an
    access token for use with Spotify's WebAPI

    Returns None if the server responds with an error.
    """
    auth_endpoint = "https://accounts.spotify.com/api/token"
    payload = {"grant_type":"client_credentials"}
    client_header = client_id + ":" + client_secret
    client_header_base64 =  base64.b64encode(client_header.encode('ascii'))
    headers = {"Authorization": "Basic " + client_header_base64.decode()}
    r = requests.post(auth_endpoint, headers=headers, data=payload)
    if r.ok:
        return r.json()['access_token']
    else:
        return None


# example usage: searching for a playlist, printing out all the songs, finding
# more details about first song in the playlist
if __name__ == "__main__":

    # First, get an access token for Spotify
    access_token = get_access_token(secrets.spotify_client_id, secrets.spotify_client_secret)
    if access_token:
        search_address = "https://api.spotify.com/v1/search"
        query = "workout"
        qtype = "playlist"
        params = {"query": query, "type": qtype}
        headers = {"Authorization": "Bearer " + access_token}

        # Next, make a request to search for a playlist
        r = requests.get(search_address, headers=headers, params=params)
        if r.ok:
            # Parse the first playlist from the response
            response = r.json()
            first_playlist = response['playlists']['items'][0]
            tracks_address = first_playlist['tracks']['href']  # The playlist objects Spotify gives you has a link to data about the tracks on the playlist

            # Then, make a request to get the tracks from the playlist
            tracks_r = requests.get(tracks_address, headers=headers) # can use same access token header
            if tracks_r.ok:
                # Parse the track names from the response
                tracks_response = tracks_r.json()
                tracks = tracks_response['items']
                for track in tracks:
                    track = track['track']
                    name = track['name']
                    print(name)
            else:
                print("Error finding tracks")
        else:
            print("Error will getting playlist")
    else:
        print("Error while getting access token")

