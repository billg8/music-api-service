# music-api-service

USAGE:
1. docker compose up  (to bring up the container, required moidules, and expose port 8000 for listening)
2. curl http://localhost:8000/water   (in a second terminal window to fetch songs with the word 'water' in the lyrics

This repo contains a flask API app for exposing a service written in python that fetches songs from musixmatch whose lyrics contain the PARAMETER passed by the user in the
format shown above. After running the CURL command, go back to the FIRST terminal window where docker compose was run to see the output of the python script (list of songs)
whose album was released before 01-01-2010 and the language is English-en

The output is written to the musixmatch.csv file as well in the local folder
