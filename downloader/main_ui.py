import sys


import tkinter as tk
import threading
from cgitb import reset
from tkinter import scrolledtext, messagebox
from downloader.fler_downloader import Downloader
class DownloaderUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Fler catalog")
        self.root.geometry("800x500")

        self.stop_event = threading.Event()
        self.thread = None  # Store the running thread

        # Username field
        tk.Label(root, text="Username:").pack()
        self.username_entry = tk.Entry(root)
        self.username_entry.pack()

        # Password field
        tk.Label(root, text="Password:").pack()
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack()

        # Run Button
        self.run_button = tk.Button(root, text="Run", command=self.run_script)
        self.run_button.pack(pady=5)

        # Stop Button (Initially disabled)
        self.stop_button = tk.Button(root, text="Stop", command=self.stop_script, state=tk.DISABLED)
        self.stop_button.pack(pady=5)

        # Output Text Box
        self.output_text = scrolledtext.ScrolledText(root)
        self.output_text.pack()

        sys.stdout = RedirectText(self.output_text)
        # sys.stderr = RedirectText(self.output_text)


    def log(self, message):
        """Safely update the output text box from any thread."""
        self.root.after(0, lambda: self.output_text.insert(tk.END, message + "\n"))
        self.root.after(0, self.output_text.see, tk.END)  # Auto-scroll

    def run_script(self):
        """Starts the script in a new thread and manages UI state."""
        if self.thread and self.thread.is_alive():
            self.log("Script is already running!")
            return

        self.stop_event.clear()  # Reset stop event

        username = self.username_entry.get()
        password = self.password_entry.get()

        self.run_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        self.thread = threading.Thread(target=self.start_execution, args=[username, password,self.stop_event], daemon=True)
        self.thread.start()

    def start_execution(self, username, password, stop_event):
        try:
            Downloader(username, password, stop_event).download_and_export()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.reset_ui()


    def stop_script(self):
        """Stops the running script."""
        self.stop_event.set()
        self.thread.join(0)
        self.reset_ui()

    def reset_ui(self):
        self.run_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

class RedirectText:
    """Redirects print output to the UI text widget."""
    def __init__(self, widget):
        self.widget = widget

    def write(self, text):
        self.widget.insert(tk.END, text)
        self.widget.see(tk.END)  # Auto-scroll to the latest message

    def flush(self):
        pass  # Required for compatibility

# TODO refactor to own file
