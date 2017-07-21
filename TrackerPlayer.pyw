# owner: Eyal Waserman 2017
# download music from here: http://www.bensound.com/royalty-free-music/
# registry (1): https://www.howtogeek.com/howto/windows-vista/add-any-application-to-the-desktop-right-click-menu-in-vista/
# registry (2): https://docs.python.org/3.0/library/winreg.html
# registry (3): https://stackoverflow.com/questions/15030033/how-do-i-open-windows-registry-with-write-access-in-python
# registry (4): https://stackoverflow.com/questions/10833710/windows-explorer-context-menus-with-sub-menus-using-pywin32

import os
from PlayerGui import PlayerGui
from TrackBoard import TrackBoard
from multiprocessing import Process

class TrackerPlayer:
    # all players we work with
    players = {
        'wmplayer': r"C:\Program Files\Windows Media Player",
        'vlc':      r"C:\Program Files (x86)\VideoLAN\VLC"
    }

    def __init__(self):
        # add all players to PATH
        os.environ["PATH"] += os.pathsep + os.pathsep.join(list(TrackerPlayer.players.values()))

    def start_wmplayer_on_file(self, filename, fullscreen=False):
        fullscreen_str = r' /fullscreen' if fullscreen else ''
        p = Process(target = os.system, args=(r'wmplayer "{}"{}'.format(filename, fullscreen_str),))
        p.start()

    def start_vlc_on_file(self, filename, fullscreen=True):
        fullscreen_str = r'--fullscreen' if fullscreen else ''
        p = Process(target = os.system, args=(r'vlc {1} "{0}"'.format(filename, fullscreen_str),))
        p.start()

    def play_file(self, file: str):
        extensions = {
            '.mp3': lambda: self.start_wmplayer_on_file(filename=file),
            '.mp4': lambda: self.start_vlc_on_file(filename=file)
        }
        for k, v in extensions.items():
            if file.endswith(k):
                v()
                break

if __name__ == "__main__":
    cwd = os.getcwd()
    tb = TrackBoard.look_for_index(cwd)
    tp = TrackerPlayer()
    pg = PlayerGui(tb, tp)