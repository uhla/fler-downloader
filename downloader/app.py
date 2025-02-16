import tkinter as tk

from downloader.main_ui import DownloaderUI

if __name__ == "__main__":
    root = tk.Tk()
    app = DownloaderUI(root)
    root.mainloop()

