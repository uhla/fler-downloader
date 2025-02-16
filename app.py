import tkinter as tk

from downloader.main_ui import DownloaderUI

if __name__ == "__main__":
    root = tk.Tk()
    app = DownloaderUI(root)
    root.mainloop()

    #TODO items:
    # bug when stop is not reset when the export is finished
    # improve messages
    # write docs or help on what are files for and where is it exported
    # store last used user name in prefs and load it

