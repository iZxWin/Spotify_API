import json
import os
import re
import matplotlib.pyplot as plt

#Function to read album data from the json
def read_album_data():
    
    with open("artist_albums.json", "r") as json_file:
        data = json_file.read()
        if not data.strip():
            print("Error: Album data is empty")   
        try:
            return json.loads(data)
        except ValueError:
            print("Error: The file 'artist_albums.json' is not in valid JSON format :(")

#Function to read artist data from the json          
def read_artist_data():

    with open("artist_info.json", "r") as json_file2:
        data = json_file2.read()
        if not data.strip():
            print("Error: Artist data is empty")    
        try:
            return json.loads(data)
        except ValueError:
            print("Error: The file 'artist_info.json' is not in valid JSON format :(")

#Function to read and get the most popular song lyrics           
def read_most_popular_song_lyrics():
    
    with open("most_popular_song_lyrics.json", "r") as json_file4:
        lyrics_data1 = json_file4.read()
        if not lyrics_data1.strip():
            print("Error: Most popular song data is empty")
            return "unknow"
        try:
            lyrics_data = json.loads(lyrics_data1) 
            return lyrics_data.get("lyrics","unknow")        
        except ValueError:
            print("Error: The file 'most_popular_song_lyrics.json' is not in valid JSON format :(")

#Function to get the name of the most popular track            
def get_track_name():
    
    with open("song_name.json", "r") as json_file5:
        data1 = json_file5.read()
        if not data1.strip():
            print("Error: song name is empty")  
        try:
            data = json.loads(data1)
            return data.get("song_name", "Unknown") 
        except ValueError:
            print("Error: The file 'song_name.json' is not in valid JSON format :(")

#Function to just clean the console       
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_menu():
    print("\nWelcome to the Main Menu. Choose one of the options below: ")
    print("1. Exit")
    print("2. Check all the information about your artist")
    print("3. Is this word in the lyrics?")
    print("4. How many songs have been released by your artist each year?")
    print("5. What is the average length of words in the lyrics of the most popular song?")
    print("6. How many albums were released per season?")


#Display chart for songs released each year
def display_chart_1():
    message = f"""
 | Year  | Songs |
 |-------|-------|
    """
    print(message)

#Display chart for albums and total tracks
def display_char_2():
    message = f"""
 | Album Name                     | Total Tracks |
 |--------------------------------|--------------|
    """
    print(message)

#Display chart for albums by season
def display_char_3():
    message = (f"""
 | Album Name                     | Release Date | Season  |
 |--------------------------------|--------------|---------|
    """)
    print(message)

#Function to generate the graph for songs released each year
def generate_songs_released_year_graph(year_song_count):

    plt.figure(figsize=(10, 6))
    plt.bar(year_song_count.keys(), year_song_count.values(), color="orange") #the keys are going to X and the values to Y in the graph
    plt.title("Number of Songs Released Each Year", fontsize=14)
    plt.xlabel("Year", fontsize=12)
    plt.ylabel("Number of Songs", fontsize=12)

    plt.savefig("songs_released_each_year.png")  
    plt.show()

    print("Graph saved as 'songs_released_each_year.png'")
    input("\nPress any key to continue...")

#Function to generate the graph for albums by season
def generate_album_season_graph(album_season_data):
        
    plt.figure(figsize=(8, 5))
    plt.bar(album_season_data.keys(), album_season_data.values(), color="turquoise")
    plt.title("Number of Albums Released by Season", fontsize=14)
    plt.xlabel("Season", fontsize=12)
    plt.ylabel("Number of Albums", fontsize=12)

    plt.savefig("songs_released_each_season.png")  
    plt.show()

    print("Graph saved as 'songs_released_each_season.png'")
    input("\nPress any key to continue...")

#Function to determine season from release date
def get_season_from_date(release_date):
    season = ""
    if len(release_date) >= 7:  
        release_month = int(release_date[5:7])
    else:
        release_month = 0

    if release_month in [12, 1, 2]:
        season = "Winter"
    elif release_month in [3, 4, 5]:
        season = "Spring"
    elif release_month in [6, 7, 8]:
        season = "Summer"
    elif release_month in [9, 10, 11]:
        season = "Autumn"
    else:
        season = "Unknown"
    return season

#Function to show all artist data (option 2)
def show_all_artist_data():
    clear_console()
    
    artist_data = read_artist_data()
    if not artist_data:
        print("No artist data available to display")
        input("\nPress any key to continue...")
    else:

        print("All the information of your artist:\n")
        artist_name = artist_data.get("name", "Name is not available")
        popularity = artist_data.get("popularity", "Popularity is not available")
        followers = artist_data.get("followers", {}).get("total", "Followers count is not available")
        genres = artist_data.get("genres", "Genres are not available")
    
        print(f"☆  Artist name: {artist_name}")
        print(f"☆  popularity: {popularity}")
        print(f"☆  followers: {followers}")
        print(f"☆  Genres: {genres}")
        input("\nPress any key to continue...")

#FUnction to check if a word is in a song (option 3)
def check_words_in_song():
    clear_console()
    
    name = get_track_name()  
    lyrics = read_most_popular_song_lyrics()
    
    if lyrics == "unknow":  
        print("Error: Could not retrieve the lyrics")
        input("\nPress any key to continue...")
    else:
        print(lyrics)
        lyrics_lower = lyrics.lower()
        
        print("\nThe name of the most popular song you are analyzing is:", name)
        word_to_check = input("Enter the word you want to check: ").strip().lower()

        words = lyrics_lower.split()
        word_count = 0

        for word in words:
            if word == word_to_check:
                word_count += 1

        if word_count > 0:
            print(f"\nThe word '{word_to_check}' was found {word_count} time(s) in the lyrics ")
        else:
            print(f"\nThe word '{word_to_check}' was NOT found in the lyrics")

        input("\nPress any key to continue...")


#Function to show songs released each year (option 4)
def songs_released_each_year():
    clear_console()
    
    albums_data = read_album_data()
    if not albums_data:
        print("No album data available to process")
        input("\nPress any key to continue...")
    else:    
        year_song_count = {}

        for album in albums_data:
            release_year = album.get("release_date", "Date not available")[:4]
            total_tracks = album.get("total_tracks", 0)

            if release_year in year_song_count:
                year_song_count[release_year] += total_tracks
            else:
                year_song_count[release_year] = total_tracks

        choice = input("Do you want to see the data as text or as a graph? (type 'text' or 'graph'): ")
        if choice.lower() == 'text':
            print("Songs released by your artist each year:")
            display_chart_1()

            for year, count in year_song_count.items():
                print(f" | {year:<5} | {count:^5} |")  

            input("\nPress any key to continue...")
        elif choice.lower() == 'graph':
            generate_songs_released_year_graph(year_song_count)


#Function to show average length in the lyrics (option 5)
def average_word_length():
    clear_console()
    
    name = get_track_name()
    lyrics = read_most_popular_song_lyrics()  

    if lyrics == "unknow":  
        print("Error: Could not retrieve the lyrics")
        input("\nPress any key to continue...")
    else:
        
        words = lyrics.lower().split()
        total_length = 0
        word_count = 0  
        
        for word in words:
            word = re.sub(r"[^\w\s]", "", word)  #We used this regex to replace everything that's not an alphanumeric character or a whitespace with an empty string
            
            if word:  
                total_length += len(word)
                word_count += 1 

        if word_count > 0:
            average_length = total_length // word_count  
            print(f"\nThe average word length for the song '{name}' is: {average_length} characters")
        else:
            print("No words found to calculate average length")
        
        input("\nPress any key to continue...")

#FUnction to show albums by release season (option 6)
def albums_by_season():
    clear_console()
    
    albums_data = read_album_data()
    
    if not albums_data:
        print("No album data available to process")
        input("\nPress any key to continue...")
    else:   
        choice = input("Do you want to see the data as text or as a graph? (type 'text' or 'graph'): ")
        
        album_season_data = {}

        if choice.lower() == 'text':
            display_char_3()
            for album in albums_data:
                album_name = album.get("name", "Name is not available")[:30]
                release_date = album.get("release_date", "Date not available")
                season = get_season_from_date(release_date)
                
                print(f" | {album_name:<30} | {release_date:^12} | {season:<7} |")
    
                if season in album_season_data:
                    album_season_data[season] += 1
                else:
                    album_season_data[season] = 1
    
            input("\nPress any key to continue...")
        
        elif choice.lower() == 'graph':
            
            for album in albums_data:
                release_date = album.get("release_date", "Date not available")
                season = get_season_from_date(release_date)
                if season in album_season_data:
                    album_season_data[season] += 1
                else:
                    album_season_data[season] = 1
    
            generate_album_season_graph(album_season_data)
            
            
#Main function controlling the menu
def main():
    option = 0
    while option != "1":
        
        clear_console()
        display_menu()
        option = input("\ntype your option: ")
        match option:
            case "1":
                print("Thank you for using our program! See you next time!")
            case "2":
                show_all_artist_data()
            case "3":
                check_words_in_song()
            case "4":
                songs_released_each_year()
            case "5":
                average_word_length()
            case "6":
                albums_by_season()
            case _:
                clear_console()
                print("invalid option... choose between 1 and 6")
                input("\nPress any key to continue...")

if __name__ == "__main__":
    main()