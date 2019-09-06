import pygame
import random
from pathlib import Path

class SongNotFoundError(Exception):
    pass

class Mp3Player:
    def __init__(self, song_path):
        pygame.mixer.init()
        self.song_index = 0
        self.song_list = sorted(Path(song_path).glob('*mp3'))
        self.song_names = [i.stem for i in self.song_list]
        self._song_volume = 0
        self.set_curr_vol(self._song_volume)
       

    def play_song(self):
        pygame.mixer.music.load(str(self.song_list[self.song_index]))
        pygame.mixer.music.play()

        
    def stop_song(self):
        pygame.mixer.music.stop()
        
    def get_current_song(self):
        return self.song_list[self.song_index].stem

    def next_song(self, curr_song):
        if self.song_index == len(self.song_names) - 1:
            raise IndexError
        self.update_song_index(curr_song)
        self.song_index  += 1
        self.play_song()

    def pause_song(self):
        pygame.mixer.music.pause()

    def unpause_song(self):
        pygame.mixer.music.unpause()

    def set_curr_vol(self, current_vol):
        pygame.mixer.music.set_volume(int(float(current_vol))/100)

    def shuffle_songs(self):
        random.shuffle(self.song_list)
        self.song_index = random.randint(0, len(self.song_list) - 1)
        self.song_names = [i.stem for i in self.song_list]
        self.play_song()
        
    def search(self, song):
        if song in self.song_names:
            self.song_index = self.song_names.index(song)
            self.play_song()
        else:
            raise SongNotFoundError

    def update_song_index(self, curr_song):
        self.song_index = self.song_names.index(curr_song)

    def get_song_names(self):
        return self.song_names
            
    def get_num_songs(self):
        return len(self.song_list)

    def get_song_index(self):
        return self.song_index

    def get_song_name_index(self, song):
        return self.song_names.index(song)

    def get_curr_song(self):
        return self.song_names[self.song_index]
    

    def is_playing(self):
        return pygame.mixer.music.get_busy()

    def get_music_playtime(self):
        return pygame.mixer.music.get_pos()

    
        


        

