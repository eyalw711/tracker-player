# owner: Eyal Waserman 2017
import ctypes
import os
from os.path import isfile, join
import pickle
import sys

class TrackBoard:
    filename = ".tb"
    extensions = ['.mp3', '.mp4']

    def __init__(self, dir_path):
        self.dir_path = dir_path
        self.entries = [[f, False] for f in os.listdir(self.dir_path)
                      if (isfile(join(self.dir_path, f)) and f.endswith(tuple(TrackBoard.extensions)))]
        self.entries.sort(key=lambda x: str.lower(x[0]))

    def update_watched_file(self, filename):
        for e in self.entries:
            f, _ = e
            if f == filename:
                e[1] = True
                break
        self.save()

    def update_files_on_load(self):
        updated_files = [f for f in os.listdir(self.dir_path)
                      if (isfile(join(self.dir_path, f)) and f.endswith(tuple(TrackBoard.extensions)))]

        missing_entries = [[file, False] for file in updated_files if
                         not any(tbentry[0] == file for tbentry in self.entries)]
        new_entries = [[f, s] for [f, s] in self.entries if f in updated_files]
        self.entries = new_entries + missing_entries
        self.entries.sort(key=lambda x: str.lower(x[0]))

    def save(self):
        filepath = os.path.join(self.dir_path, TrackBoard.filename)
        with open(filepath, 'wb') as trackboard_pickle:
            try:
                trackboard_pickle.truncate()
                pickle.dump(self, trackboard_pickle)
            except Exception as e:
                if os.name == 'nt':
                    ctypes.windll.user32.MessageBoxW(0, u"Error", u"Error", 0)
                else:
                    print(e)
                    exit()

        # make hidden - doesn't work well with writing!
        # if os.name == 'nt':
        #     FILE_ATTRIBUTE_HIDDEN = 0x02
        #     ret = ctypes.windll.kernel32.SetFileAttributesW(r'{}'.format(filepath), FILE_ATTRIBUTE_HIDDEN)
        #     if not ret:
        #         ctypes.windll.user32.MessageBoxW(0, u"Error", u"Error", 0)


    @staticmethod
    def look_for_index(dirpath):
        try:
            with open(os.path.join(dirpath, TrackBoard.filename), "rb") as trackboard_pickle:
                try:
                    trackboard = pickle.load(trackboard_pickle)
                    trackboard.update_files_on_load()
                except Exception as e:
                    print(e)
                    raise FileNotFoundError
        except FileNotFoundError:
            trackboard = TrackBoard(dirpath)
        try:
            trackboard.save()
        except Exception as e:
            print(e)
        return trackboard
