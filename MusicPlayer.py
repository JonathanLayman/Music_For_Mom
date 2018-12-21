import PySimpleGUI as sg
import vlc
from gmusicapi import Mobileclient
import requests
from datetime import timedelta


class MusicPlayer:
    def __init__(self, device_id, token):
        # Gmusic API initialization
        print("initializing client")
        self.api = Mobileclient()
        print("logging in")
        self.api.oauth_login(device_id, token)
        print("loading all songs")
        self.all_songs = self.api.get_all_songs()
        print("loading playlists")
        self.all_playlists = self.api.get_all_user_playlist_contents()
        self.all_playlist_names = {}
        for playlist in self.all_playlists:
            self.all_playlist_names[playlist["name"]] = playlist["id"]

        # VLC initialization
        self.track_file = vlc.MediaPlayer()
        self.track_list = []
        self.titles = []
        self.track_number = 0
        self.playlists = []
        self.current_time = -1
        self.max_time = -1

        # Get playlists, songs from the first playlist, and load the first song
        self.get_playlists()
        self.get_songs_from_playlist(self.playlists[0])
        self.song = self.track_list[self.track_number]["trackId"]
        self.load_track()

        # GUI initialization
        print("creating window")
        self.song = ""
        self.player_layout = [
            [sg.Text("Music Player", size=(15, 1), font=("Helvetica", 25))],
            [sg.Listbox(values=self.playlists, size=(30, 20), bind_return_key=True, key="_playlists_"),
             # sg.Image(),
             sg.Listbox(values=self.titles, size=(30, 20), bind_return_key=True, key="_Tracks_")],
            [sg.Text(self.song, key="Song Name")],
            [sg.Button("Play"), sg.Button("Pause"), sg.Button("Next")]
        ]

        self.title = "Music Player"
        self.window = sg.Window(self.title).Layout(self.player_layout)

    def get_playlists(self):
        data = self.api.get_all_playlists()
        self.playlists = []
        for playlist in data:
            if not playlist['deleted']:
                self.playlists.append(playlist['name'])
        print(self.playlists)

    def change_playlists(self, name):
        for pos, title in enumerate(self.playlists):
            if title == name:
                self.get_songs_from_playlist(self.playlists[pos])

    def get_songs_from_playlist(self, name):
        print("Obtaining track list")
        tracks = []
        if name in self.all_playlist_names:
            for playlist in self.all_playlists:
                if playlist["name"] == name:
                    for track in playlist["tracks"]:
                        tracks.append(track)
                    break
        self.track_list = tracks
        self.get_playlist_song_titles()

    def get_playlist_song_titles(self):
        print("Getting playlist song titles")
        titles = []
        for song in self.track_list:
            if song["source"] == "2":
                titles.append(song["track"]["title"])
            else:
                for track in self.all_songs:
                    if track["id"] == song["trackId"]:
                        print("match found")
                        titles.append(track["title"])
                else:
                    print("No match found")
        print(titles)
        self.titles = titles

    def get_song_position_from_title(self, title):
        for pos, name in enumerate(self.titles):
            if name == title:
                return pos
        else:
            print("Couldn't find song in tracks")

    def download_song(self):
        print("downloading song")
        url = self.api.get_stream_url(self.song)
        doc = requests.get(url)
        with open("song.mp3", "wb") as f:
            f.write(doc.content)

    def load_track(self):
        # self.track_file = vlc.MediaPlayer(self.song)
        self.track_file = vlc.MediaPlayer("song.mp3")
        print("Time:", self.track_file.get_length())

    def play(self):
        self.track_file.play()

    def stop(self):
        self.track_file.stop()

    def pause(self):
        self.track_file.pause()

    def next(self):
        self.track_number += 1
        self.song = self.track_list[self.track_number]["trackId"]
        self.window.FindElement("_Tracks_").SetValue(self.titles[self.track_number])
        self.download_song()
        self.track_file.stop()
        self.load_track()
        self.track_file.play()
        self.max_time = self.track_file.get_time()

    def run(self):
        print("launching program")
        while True:
            self.current_time = self.track_file.get_time()
            if self.max_time == -1:
                self.max_time = self.track_file.get_length()
            elif self.max_time == 0:
                self.max_time = -1
            else:
                current = timedelta(milliseconds=self.current_time)
                max = timedelta(milliseconds=self.max_time)
                print("Current", current, "Max", max)
                print(((self.current_time) / self.max_time) * 100)

                if (self.current_time + 500) > self.max_time:
                    self.next()

            event, values = self.window.Read(timeout=100)
            if event is not None:
                if event == "Play":
                    self.play()
                    print("Max time:", self.track_file.get_length())
                    print("Current time:", self.track_file.get_time())
                elif event == "Stop":
                    self.stop()
                elif event == "Pause":
                    self.pause()
                elif event == "Next":
                    self.next()
                elif event == "_Tracks_":
                    self.track_number = self.get_song_position_from_title(values[event][0])
                    self.song = self.track_list[self.track_number]["trackId"]
                    self.download_song()
                    self.track_file.stop()
                    self.load_track()
                    self.track_file.play()
                elif event == "_playlists_":
                    print(values[event][0])
                    self.change_playlists(values[event][0])
                    self.window.FindElement("_Tracks_").Update(self.titles)
                else:
                    print(event)
            if event == "Quit" or values is None:
                break


if __name__ == "__main__":
    try:
        with open("oauth/device_id.txt", "r") as f:
            device_id = f.read()
        mp = MusicPlayer(device_id, "oauth/oauth_code.txt")
        mp.run()
    except FileNotFoundError:
        print("Authorization Token Missing. Run login.py")
        answer = input("Would you like to run now? y/n: ")
        if answer == "y":
            import login
            with open("oauth/device_id.txt", "r") as f:
                device_id = f.read()
            mp = MusicPlayer(device_id, "oauth/oauth_code.txt")
            mp.run()

