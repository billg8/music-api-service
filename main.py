import os
import sys
import csv
import json
import requests
from datetime import datetime
from datetime import date
from flask import Flask, request, Response, jsonify


# Create the app
app = Flask(__name__)

def search_lyrics(input_word):
    # TRACK & ALBUM API CALLS
    base_url_track_search = 'https://api.musixmatch.com/ws/1.1/track.search'
    base_url_album_search = 'https://api.musixmatch.com/ws/1.1/album.get'

    # INPUT VARIABLES
    api_key = os.environ['API_KEY']
    lyrics_lang = 'en'
    headers = {'Content-Type': 'application/json'}
    album_release = date(2010, 1, 1)
    page = 1
    page_size = 50
    fieldnames = ["song_name", "performer_name", "album_name", "song_share_url"]


    ## IMPORTANT: NEED TO LOOK-UP ALBUM RELEASE DATE AND NOT SONG DATE
    def find_album_release_date(album_id):
        payload_album = {'apikey': api_key, 'album_id': album_id}
        result = requests.get(base_url_album_search, headers=headers, params=payload_album)
        return result

    payload = {'apikey': api_key, 'q_lyrics': input_word, 'f_lyrics_language': lyrics_lang, 'page': page, 'page_size': page_size}

    # SUBMIT THE LYRICS SEARCH CALL AND DETECT EXCEPTIONS
    try:
        r = requests.get(base_url_track_search, headers=headers, params=payload)
    except requests.exceptions.Timeout:
        print("The API call timed-out. Exiting....")
        raise SystemExit(e)
    except requests.exceptions.TooManyRedirects:
        print("Too many redirects. Seems the URL used for the API call is bad")
    except requests.exceptions.RequestException as e:
        print("An error has occured and the request cannot be completed")
        raise SystemExit(e)

    ## PREPARE CSV FILE FOR WRITING
    with open('./musixmatch.csv', 'w', newline='') as csvfile:
      writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
      writer.writerow([fieldnames])

      json_data = r.json() if r and r.status_code == 200 else None
      for pf in json_data["message"]["body"]["track_list"]:
        song_name = pf["track"]["track_name"]
        artist_name = pf["track"]["artist_name"]
        album_name = pf["track"]["album_name"]
        track_share_url = pf["track"]["track_share_url"]
        album_id = pf["track"]["album_id"]
        print(song_name + ',' + artist_name + ',' + album_name + ',' + track_share_url)

        # check the release date of the ALBUM
        release_date_check = find_album_release_date(album_id)

        album_json_data = release_date_check.json() # if r and release_date_check.status_code == 200 else None
        release_date = album_json_data["message"]["body"]["album"]["album_release_date"]

        # MANIPULATE THE RELEASE_DATE since some albums don't have a release date, and others only release YEAR
        try:
          if len(release_date) == 4:
            compare_release_date = datetime.strptime(release_date, '%Y').date() < album_release
          else:
            compare_release_date = datetime.strptime(release_date, '%Y-%m-%d').date() < album_release
        except:
          # if no album release date, continue and skip it
          continue
        print(release_date + ' ' + str(compare_release_date))
        if compare_release_date == True:
          writer.writerow([song_name, artist_name, album_name, track_share_url])
    return 'Ok'

@app.route('/',defaults={'input_word' : 'car'})
@app.route('/<string:input_word>')
def start(input_word: str):
    result = search_lyrics(input_word)
    return result

                      