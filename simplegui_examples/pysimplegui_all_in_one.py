import PySimpleGUI as sg

layout = [[sg.Text('All graphic widgets in one window!', size=(30, 1), font=("Helvetica", 25), text_color='blue')],
   [sg.Text('Here is some text.... and a place to enter text')],
   [sg.InputText()],
   [sg.Checkbox('My first checkbox!'), sg.Checkbox('My second checkbox!', default=True)],
   [sg.Radio('My first Radio!     ', "RADIO1", default=True), sg.Radio('My second Radio!', "RADIO1")],
   [sg.Multiline(default_text='This is the default Text shoulsd you decide not to type anything',)],
[sg.InputCombo(['Combobox 1', 'Combobox 2'], size=(20, 3)),
 sg.Slider(range=(1, 100), orientation='h', size=(35, 20), default_value=85)],
[sg.Listbox(values=['Listbox 1', 'Listbox 2', 'Listbox 3'], size=(30, 6), bind_return_key=True),
 sg.Slider(range=(1, 100), orientation='v', size=(10, 20), default_value=25),
 sg.Slider(range=(1, 100), orientation='v', size=(10, 20), default_value=75),
 sg.Slider(range=(1, 100), orientation='v', size=(10, 20), default_value=10)],
[sg.Text('_'  * 100, size=(70, 1))],
[sg.Text('Choose Source and Destination Folders', size=(35, 1))],
[sg.Text('Source Folder', size=(15, 1), auto_size_text=False, justification='right'), sg.InputText('Source'),
 sg.FolderBrowse()],
[sg.Text('Destination Folder', size=(15, 1), auto_size_text=False, justification='right'), sg.InputText('Dest'),
 sg.FolderBrowse()],
[sg.Submit(), sg.Cancel(), sg.Button('Customized', button_color=('white', 'green'))]]

song_name = "Song Name"

other_layout = [
            [sg.Text("Music Player", size=(15, 1), font=("Helvetica", 25))],
            [sg.Listbox(values=["Song1", "song2", "Song with a really long name to see how it displays"], size=(15, 20), bind_return_key=True),
             # sg.Image(),
             sg.Listbox(values=["Playlist1", "Playlist2"], size=(15, 20), bind_return_key=True)],
            [sg.Text(song_name, key="Song Name")],
            [sg.Button("Play"), sg.Button("Pause"), sg.Button("Next")]
        ]


# window = sg.Window("title").Layout(layout)
window = sg.Window("title").Layout(other_layout)

while True:
    event, values = window.Read()
    if event is not None:
        print(event, values)
        if event == "Next":
            song_name = "New Song"
            print("Updating song name")
            window.FindElement("Song Name").Update(song_name)
        if type(event) == int:
            print(values[event])
        else:
            print(event)
    if event == "Quit" or values is None:
        break
