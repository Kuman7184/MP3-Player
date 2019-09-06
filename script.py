import tkinter
import difflib
import sys
from tkinter import ttk
from tkinter import messagebox
from model import Mp3Player
from model import SongNotFoundError


_DEFAULT_FONT = ('Arial', 15)

class Mp3PlayerApp:
    def __init__(self):
        self._player = Mp3Player('test_music')
        self._root_window = tkinter.Tk()
        self._root_window.title("MP3 Player")
        self._root_window.geometry("500x600")
        self._is_paused = 0
        self._is_stopped = True
        self._shuffle_mode = False
        self._search_note = tkinter.StringVar(value = "Search for song...")
        self._var = tkinter.StringVar(value = "Select a song...")
        self._time_label = tkinter.StringVar(value = str(self._player.get_music_playtime()))
        self._tar = tkinter.StringVar()
        self._create_widgets()
        self._create_playlist()
        self._playlist.focus('I001')
        self._pack_widgets()
        
       

    def _create_widgets(self):
        style = ttk.Style()
        style.configure("BW.TLabel", foreground="black", background="white")

        self._search_bar = ttk.Entry(
            master = self._root_window,
            textvariable = self._search_note)
        
        self._search_bar.bind("<Button-1>", self._delete_default_text)
        self._search_bar.bind("<Return>", self._search_song)
        
        self._display_label = ttk.Label(
            master = self._root_window,
            textvariable = self._var,
            font = _DEFAULT_FONT,
            style = "BW.TLabel",
            anchor = "center")

        self._volume_label = tkinter.Label(
            master = self._root_window,
            text = "Volume",
            font = ('Arial', 12),
            anchor = "center")

        self._volume_control = ttk.Scale(
            master = self._root_window,
            from_ = 0,
            to_ = 100,
            orient = tkinter.HORIZONTAL,
           
            command = self._player.set_curr_vol)

        ttk.Style().configure("TButton", padding=6, relief="flat",
           background="#ccc")
        
        self._play_button = ttk.Button(
                self._root_window, text = "PLAY",
                command = self._play_button_switch,
                style = "TButton")
        
        self._stop_button = ttk.Button(
            master = self._root_window,
            text = 'STOP',
            command = self._stop_selected_song,
            style = "TButton")

        self._next_button = ttk.Button(
            master = self._root_window,
            text = 'NEXT',
            command = self._play_next_song,
            style = "TButton")

        self._end_label = ttk.Label(
            master = self._root_window,
            textvariable = self._tar,
            font = ("Arial", 10))
        
        self._playlist_frame = tkinter.LabelFrame(self._root_window,
            text = 'Playlist',
            font = ('Arial', 10))                                      
                                        
        self._playlist = ttk.Treeview(self._playlist_frame)
        self._playlist["columns"]=("one","two")
        self._playlist.column("#0", width=270, minwidth=270, stretch=tkinter.NO)
        

        self._playlist.heading("#0",text="Song Name",anchor=tkinter.W)
       
                               
##        self._playlist = ttk.Listbox(
##            master = self._playlist_frame,
##            selectmode = tkinter.SINGLE)
        
        self._playlist.bind('<Double-Button-1>', self._play_selected_song)
        
   

    def _create_playlist(self):
        for i in range(len(self._player.get_song_names())):
            self._playlist.insert("", i, text= self._player.get_song_names()[i])
            

    def _pack_widgets(self):
        self._search_bar.pack(pady= 15, fill = 'x')
        self._display_label.pack(pady = 25, fill = 'x')
        self._volume_label.pack(fill = 'x')
        self._volume_control.pack(fill = 'x')
        self._play_button.pack(pady = 25, fill = 'x')
        self._stop_button.pack(pady = 25, fill = 'x')
        self._next_button.pack(pady = 25, fill = 'x')
        self._end_label.pack()
        self._playlist_frame.pack(pady = 20, fill = 'both', expand = "yes")
        self._playlist.pack(fill = 'both', expand = 'yes')
        

    def _play_selected_song(self, event):
        selected_song = self._playlist.focus()
        
        self._is_stopped = False
        self._is_paused = 1
        #song_index = self._player.get_song_name_index(self._playlist.get(tkinter.ACTIVE))
        self._player.update_song_index(self._playlist.item(selected_song)['text'])
        self._player.play_song()
        
        self._var.set("Now playing...\n"+ self._playlist.item(selected_song)['text'])
        #self._var.set("Now playing...\n"+self._playlist.get(tkinter.ACTIVE))
        self._play_button['text'] = 'PAUSE'
        self._tar.set("")

    def _play_next_song(self):
        selected_song = self._playlist.focus()
        try:
            self._player.next_song(self._playlist.item(selected_song)['text'])
            self._playlist.focus(self._playlist.next(selected_song))
            self._var.set("Now playing...\n"+self._playlist.item(self._playlist.next(selected_song))['text'])
        except IndexError:
            self._tar.set("End of playlist!")
            
                      
    def _stop_selected_song(self):
        self._player.stop_song()
        self._play_button['text'] = 'PLAY'
        self._var.set("Select a song...")
        self._is_paused = 0

    def _shuffle_control(self):
        self._shuffle_mode = True
        
    def _play_button_switch(self):
        
        if self._is_paused == 0:
            selected_song = self._playlist.focus()
            
            self._is_stopped = False
            self._is_paused = 1
            self._player.play_song()
            self._var.set("Now playing...\n"+self._playlist.item(selected_song)['text'])
            self._play_button['text'] = 'PAUSE'
        elif self._is_paused == 1:
            self._is_paused = 2
            self._play_button['text'] = 'PLAY'
            self._player.pause_song()

        elif self._is_paused == 2:
            self._is_paused = 1
            self._play_button['text'] = 'PAUSE'
            self._player.unpause_song()

    def _delete_default_text(self, *args):
        self._search_bar.delete(0, tkinter.END)
    def ask_quit(self):
        if messagebox.askokcancel("Quit", "Are you sure you want to quit?"):
            self._root_window.destroy()
            
    def _search_song(self, *args):
        try:
            self._player.search(self._search_bar.get())
            self._is_paused = 1
            self._player.update_song_index(self._search_bar.get())
            self._var.set("Now playing...\n"+self._search_bar.get())
            self._search_note.set("Search for song...")
            self._play_button['text'] = 'PAUSE'
            
        except SongNotFoundError:
            self._search_note.set("Song not in playlist")
            
    def run(self):
        self._root_window.protocol("WM_DELETE_WINDOW", self.ask_quit)
        self._root_window.mainloop()
        
if __name__ == '__main__':
    Mp3PlayerApp().run()
    
    
        
            
     
