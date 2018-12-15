import PySimpleGUI as sg
import vlc
from gmusicapi import Mobileclient
import requests


class MusicPlayer:
    def __init__(self, device_id, token):
        # Gmusic API initialization
        print("initializing client")
        self.api = Mobileclient()
        print("logging in")
        self.api.oauth_login(device_id, token)
        print("loading playlists")
        self.all_playlists = self.api.get_all_user_playlist_contents()
        self.all_playlist_names = {}
        for playlist in self.all_playlists:
            self.all_playlist_names[playlist["name"]] = playlist["id"]

        # VLC initialization
        self.track_file = None
        self.track_list = []
        self.titles = []
        self.track_number = 0
        self.playlists = []

        # need a better way to do this
        self.test_list()
        self.load_track()
        self.get_playlists()

        # GUI initialization
        print("creating window")
        self.song = ""
        self.player_layout = [
            [sg.Text("Music Player", size=(15, 1), font=("Helvetica", 25))],
            [sg.Listbox(values=self.titles, size=(15, 20), bind_return_key=True, key="_Tracks_"),
             # sg.Image(),
             sg.Listbox(values=self.playlists, size=(15, 20), bind_return_key=True, key="_playlists_")],
            [sg.Text(self.song, key="Song Name")],
            [sg.Button("Play"), sg.Button("Pause"), sg.Button("Next")]
        ]

        self.title = "Music Player"
        self.window = sg.Window(self.title).Layout(self.player_layout)

    def test_list(self):
        print("Loading Test method")
        self.get_songs_from_playlist("nin")
        # for item in self.track_list:
        #     print(item)
        self.song = self.track_list[self.track_number]["trackId"]
        self.download_song()

    def get_playlists(self):
        data = self.api.get_all_playlists()
        self.playlists = []
        for playlist in data:
            if not playlist['deleted']:
                self.playlists.append(playlist['name'])
        print(self.playlists)

    def get_songs_from_playlist(self, name):
        print("Obtaining track list")
        tracks = []
        if name in self.all_playlist_names:
            for playlist in self.all_playlists:
                if playlist["name"] == name:
                    for track in playlist["tracks"]:
                        if track["source"] == "2":
                            tracks.append(track)
                    break
        self.track_list = tracks
        self.get_playlist_song_titles()

    def get_playlist_song_titles(self):
        print("Getting playlist song titles")
        titles = []
        for song in self.track_list:
            titles.append(song["track"]["title"])
        print(titles)
        self.titles = titles

    def download_song(self):
        print("downloading song")
        url = self.api.get_stream_url(self.song)
        doc = requests.get(url)
        with open("song.mp3", "wb") as f:
            f.write(doc.content)

    def load_track(self):
        # self.track_file = vlc.MediaPlayer(self.song)
        self.track_file = vlc.MediaPlayer("song.mp3")

    def play(self):
        self.track_file.play()

    def stop(self):
        self.track_file.stop()

    def pause(self):
        self.track_file.pause()

    def next(self):
        self.track_number += 1
        self.song = self.track_list[self.track_number]["trackId"]
        self.download_song()
        self.track_file.stop()
        self.load_track()
        self.track_file.play()

    def run(self):
        print("launching program")
        while True:
            event, values = self.window.Read()
            if event is not None:
                if event == "Play":
                    self.play()
                elif event == "Stop":
                    self.stop()
                elif event == "Pause":
                    self.pause()
                elif event == "Next":
                    self.next()
                elif event == "_Tracks_":
                    print(values[event][0])
                    print(type(self.song))
                else:
                    print(event)
            if event == "Quit" or values is None:
                break


if __name__ == "__main__":
    with open("oauth/device_id.txt", "r") as f:
        device_id = f.read()
    mp = MusicPlayer(device_id, "oauth/oauth_code.txt")
    mp.run()
