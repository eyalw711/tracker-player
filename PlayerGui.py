import os
import tkinter as tk
from tkinter import font
from TrackBoard import TrackBoard
from functools import partial


class PlayerGui:
    def __init__(self, tb: TrackBoard, tp):
        self.trackboard = tb
        self.player = tp

        root = tk.Tk()
        title = root.title("Watcher Player")
        menu = tk.Menu(root)
        root.config(menu=menu)
        file = tk.Menu(menu)
        file.add_command(label='Exit', command=lambda: exit())
        menu.add_cascade(label='File', menu=file)

        unwatched_label = tk.Label(root, text="Unwatched Media")
        unwatched_label.pack(fill=tk.X, padx=10)

        unwatched_files = [filename for (filename, watch_status) in tb.entries if watch_status is False]
        self.unwatched_lb = PlayerGui.Listbox(root, selectmode=tk.SINGLE)
        for file in unwatched_files:
            self.unwatched_lb.insert(tk.END, file)
        self.unwatched_lb.pack()

        watched_label = tk.Label(root, text="Watched Media")
        watched_label.pack(fill=tk.X, padx=10)

        watched_files = [filename for (filename, watch_status) in tb.entries if watch_status is True]
        self.watched_lb = PlayerGui.Listbox(root, selectmode=tk.SINGLE)

        for file in watched_files:
            self.watched_lb.insert(tk.END, file)
        self.watched_lb.pack()

        PlayerGui.Listbox.auto_width_listboxes([self.unwatched_lb, self.watched_lb], 250)
        self.unwatched_lb.bind('<<ListboxSelect>>', partial(PlayerGui.onselect, otherlb=self.watched_lb))
        self.watched_lb.bind('<<ListboxSelect>>', partial(PlayerGui.onselect, otherlb=self.unwatched_lb))

        button = tk.Button(root, text="Watch", command=lambda: self.play_selection())
        button.pack()

        root.mainloop()

    @staticmethod
    def onselect(evt, otherlb):
        w = evt.widget
        otherlb.selection_clear(0, tk.END)
        if len(w.curselection()) == 0:
            print("Empty List")
            return
        index = int(w.curselection()[0])
        value = w.get(index)
        print('You selected item %d: "%s"' % (index, value))

    def play_selection(self):
        # find selected item
        for lb in [self.unwatched_lb, self.watched_lb]:
            curselected = lb.curselection()
            if len(curselected) == 0:
                continue

            new_watched_file = lb.get(curselected[0])
            # self.player.start_wmplayer_on_file(os.path.join(os.getcwd(), new_watched_file))
            self.player.play_file(os.path.join(os.getcwd(), new_watched_file))
            if lb is self.unwatched_lb:
                lb.delete(curselected[0])
                self.watched_lb.insert(tk.END, new_watched_file)
                self.trackboard.update_watched_file(new_watched_file)

    # sub class
    class Listbox(tk.Listbox):

        @staticmethod
        def auto_width_listboxes(list_boxes, maxwidth):
            pixels = 0
            width = 0
            for lb in list_boxes:
                f = font.Font(font=lb.cget("font"))
                try:
                    this_lb_pixels = max(f.measure(item) for item in lb.get(0, "end")) + 10
                except ValueError:
                    this_lb_pixels = 50
                width = max(width, int(lb.cget("width")))
                pixels = max(pixels, this_lb_pixels)

            for w in range(0, maxwidth + 1, 5):
                if all(lb.winfo_reqwidth() >= pixels for lb in list_boxes):
                    break
                for lb in list_boxes:
                    lb.config(width=width + w)