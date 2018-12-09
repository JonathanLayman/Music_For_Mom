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

        # GUI initialization
        print("creating window")
        self.song = ""
        self.player_layout = [
            [sg.Text("Music Player")],
            [sg.Text(self.song)],
            [sg.Button("Play"), sg.Button("Stop"), sg.Button("Next")]
        ]
        self.title = "Music Player"
        self.window = sg.Window(self.title).Layout(self.player_layout)

        # VLC initialization
        self.track_file = None
        self.track_list = []
        self.track_number = 0

        # need a better way to do this
        self.test_list()
        self.load_track()

    def test_list(self):
        print("Loading Test method")
        self.get_songs_from_playlist("nin")
        # for item in self.track_list:
        #     print(item)
        self.song = self.track_list[self.track_number]["trackId"]
        self.download_song()

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
                elif event == "Next":
                    self.next()
                else:
                    print(event)
            if event == "Quit" or values is None:
                break


if __name__ == "__main__":
    with open("oauth/device_id.txt", "r") as f:
        device_id = f.read()
    mp = MusicPlayer(device_id, "oauth/oauth_code.txt")
    mp.run()
