import requests
import json

def display_artists_chart():
   message = f"""
       Artist's name    |         ID     
________________________________________________
   """
   print(message)
  

def get_artist_albums(service,artist_id, filename="artist_albums.json"):
 
    albums_url = f"{service}/artists/{artist_id}/albums"

    response = requests.get(albums_url)
    albums_data = response.json()

    if "items" in albums_data:
      
        with open(filename, "w") as json_file:
            json.dump(albums_data["items"], json_file) 
        print(f"Album data saved in '{filename}'")
    else:
        print("No albums found in API response")


def get_artist_info(service,artist_id, filename="artist_info.json"):
  
    artist_url = f"{service}/artists/{artist_id}"
 
    response = requests.get(artist_url)
    artist_data = response.json()

    with open(filename, "w",encoding= "UTF-8") as json_file:
        json.dump(artist_data, json_file, indent=4) 
    print(f"Artist data stored in '{filename}'")


def find_top_track(service, artist_id, filename="top_tracks.json"):
  
    url = f"{service}/artists/{artist_id}/top-tracks"
    response = requests.get(url)
    top_tracks_data = response.json()

    with open(filename, "w", encoding= "UTF-8") as json_file:
        json.dump(top_tracks_data, json_file, indent=4)
    print(f"Top tracks data stored in '{filename}'")

    if "tracks" in top_tracks_data and top_tracks_data["tracks"]: #here we are making sure that the tracks exists and are not empty
        tracks = top_tracks_data["tracks"]

        most_popular_track = tracks[0]
        for track in tracks:
            if track["popularity"] > most_popular_track["popularity"]:
                most_popular_track = track

        artist_name = most_popular_track["artists"][0]["name"]
        track_name = most_popular_track["name"]

        return artist_name, track_name
    else:
        print("No tracks found in the API response")
        
   
def get_track_lyrics(artist_name,track_name, filename = "most_popular_song_lyrics.json"):
    url = f"https://api.lyrics.ovh/v1/{artist_name}/{track_name}"
    response  = requests.get(url)
   
    try:
        lyrics_data = response.json()
        lyrics = lyrics_data.get("lyrics", "No lyrics found")
      
        song_data = {
            "lyrics" : lyrics
        }
       
        with open(filename,"w", encoding= "UTF-8") as json_file:
            json.dump(song_data, json_file, indent=4)
        print(f"Lyrics saved in '{filename}'")
    except ValueError:
       print("Error decoding JSON responses" )
       print("Response text:", response.text)

def save_song_name(song_name):
    with open("song_name.json", "w") as file:
        json.dump({"song_name": song_name}, file)
    print(f"Song name saved in 'song_name.json'")

def show_dict_of_artists():
  
    artist_dict = { "Twenty one pilots" : "3YQKmKGau1PzlVlkL1iodx" ,
                   "Bad Bunny" : "4q3ewBCX7sLwd24euuV69X" ,
                   "Future" : "1RyvyyTE3xzB2ZywiAwp0i" ,
                   "Frank Sinatra" : "1Mxqyy3pSjf8kZZL4QVxS0" ,
                   "Billie Eilish" : "6qqNVTkY8uBg9cP3Jd7DAH"    
                }
  
    display_artists_chart()
 
    for artist, artist_id in artist_dict.items():
       artist_name = artist[:20]
       print(f" | {artist_name:<20} | {artist_id} |")

def main():
    service = "https://dit009-spotify-assignment.vercel.app/api/v1"
   
    show_dict_of_artists()
    artist_id = input("\nCopy and paste your artist's id here: ").strip()
    print("wait a few seconds...")
   
    get_artist_albums(service,artist_id)
    get_artist_info(service,artist_id)
   
    artist_name, track_name = find_top_track(service,artist_id)
    get_track_lyrics(artist_name,track_name)
    save_song_name(track_name)
    print("Everything is okay, now you can you to the .analyser :)")
   
   
if __name__ == "__main__":
   main()