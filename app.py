import tkinter as tk

from downloader.main_ui import DownloaderUI

if __name__ == "__main__":
    root = tk.Tk()
    app = DownloaderUI(root)
    root.mainloop()

    #TODO items (ASAP):
    # - bug when stop is not reset when the export is finished
    # - improve messages
    # - write docs or help on what are files for and where is it exported
    # - what will happen to xls when the product is not on fler anymore? will it get removed? !it should!
    # - store last used user name in prefs and load it on start

    # ----------------
    #TODO Future ideas:
    # - sort by custom category in final output
    # - Possibly fetch main and then fetch variants
    #   - matching variants through master id and not title -> https://www.fler.cz/uzivatel/nastroje/flerapi?view=docs&url=/api/rest/seller/products/list
    # - configurable image fetch (would use the ones from configuration) to speed things up (would use images from xls)
    # - keywords_tech (technika/remeslo)


