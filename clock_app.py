import tkinter as tk
from tkinter import ttk
import time


class ClockTab:
    def __init__(self, parent):
        self.parent = parent
        self.is_24_hour = True
        self.setup_ui()
        self.update_clock()

    def setup_ui(self):
        # Clock display label
        self.clock_label = tk.Label(
            self.parent,
            text="00:00:00",
            font=("Helvetica", 48, "bold"),
            bg="#222222",
            fg="#00ff00"
        )
        self.clock_label.pack(pady=50)

        # Format toggle button
        self.format_button = tk.Button(
            self.parent,
            text="Switch to 12-hour",
            command=self.toggle_format,
            font=("Helvetica", 12),
            bg="#444444",
            fg="#ffffff",
            activebackground="#666666",
            activeforeground="#ffffff",
            relief="flat",
            padx=20,
            pady=10
        )
        self.format_button.pack(pady=20)

    def toggle_format(self):
        self.is_24_hour = not self.is_24_hour
        if self.is_24_hour:
            self.format_button.config(text="Switch to 12-hour")
        else:
            self.format_button.config(text="Switch to 24-hour")

    def update_clock(self):
        current_time = time.localtime()
        hours = current_time.tm_hour
        minutes = current_time.tm_min
        seconds = current_time.tm_sec

        if not self.is_24_hour:
            period = "AM" if hours < 12 else "PM"
            hours = hours % 12
            if hours == 0:
                hours = 12
            time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d} {period}"
        else:
            time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

        self.clock_label.config(text=time_str)
        self.parent.after(1000, self.update_clock)


class StopwatchTab:
    def __init__(self, parent):
        self.parent = parent
        self.start_time = None
        self.elapsed_time = 0
        self.running = False
        self.setup_ui()

    def setup_ui(self):
        # Time display label
        self.time_label = tk.Label(
            self.parent,
            text="00:00:00.000",
            font=("Courier New", 36, "bold"),
            bg="#222222",
            fg="#00ffff"
        )
        self.time_label.pack(pady=50)

        # Button frame
        button_frame = tk.Frame(self.parent, bg="#222222")
        button_frame.pack(pady=20)

        # Start button
        self.start_button = tk.Button(
            button_frame,
            text="Start",
            command=self.start_stopwatch,
            font=("Helvetica", 12),
            bg="#00aa00",
            fg="#ffffff",
            activebackground="#00cc00",
            activeforeground="#ffffff",
            relief="flat",
            width=10,
            padx=10,
            pady=10
        )
        self.start_button.pack(side=tk.LEFT, padx=10)

        # Stop button
        self.stop_button = tk.Button(
            button_frame,
            text="Stop",
            command=self.stop_stopwatch,
            font=("Helvetica", 12),
            bg="#aa0000",
            fg="#ffffff",
            activebackground="#cc0000",
            activeforeground="#ffffff",
            relief="flat",
            width=10,
            padx=10,
            pady=10,
            state=tk.DISABLED
        )
        self.stop_button.pack(side=tk.LEFT, padx=10)

        # Reset button
        self.reset_button = tk.Button(
            button_frame,
            text="Reset",
            command=self.reset_stopwatch,
            font=("Helvetica", 12),
            bg="#444444",
            fg="#ffffff",
            activebackground="#666666",
            activeforeground="#ffffff",
            relief="flat",
            width=10,
            padx=10,
            pady=10
        )
        self.reset_button.pack(side=tk.LEFT, padx=10)

    def start_stopwatch(self):
        if not self.running:
            self.start_time = time.time() - self.elapsed_time
            self.running = True
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.update_stopwatch()

    def stop_stopwatch(self):
        if self.running:
            self.running = False
            self.elapsed_time = time.time() - self.start_time
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)

    def reset_stopwatch(self):
        self.running = False
        self.elapsed_time = 0
        self.start_time = None
        self.time_label.config(text="00:00:00.000")
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def update_stopwatch(self):
        if self.running:
            current_elapsed = time.time() - self.start_time
            self.elapsed_time = current_elapsed
            self.display_time(current_elapsed)
            self.parent.after(10, self.update_stopwatch)

    def display_time(self, elapsed):
        hours = int(elapsed // 3600)
        minutes = int((elapsed % 3600) // 60)
        seconds = int(elapsed % 60)
        milliseconds = int((elapsed % 1) * 1000)
        time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
        self.time_label.config(text=time_str)


class ClockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Clock & Stopwatch App")
        self.root.geometry("500x400")
        self.root.configure(bg="#222222")

        # Configure ttk styles for dark theme
        self.setup_dark_theme()

        # Create notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        # Create tabs
        self.clock_tab = tk.Frame(self.notebook, bg="#222222")
        self.stopwatch_tab = tk.Frame(self.notebook, bg="#222222")

        self.notebook.add(self.clock_tab, text="Clock")
        self.notebook.add(self.stopwatch_tab, text="Stopwatch")

        # Initialize tab content
        ClockTab(self.clock_tab)
        StopwatchTab(self.stopwatch_tab)

    def setup_dark_theme(self):
        style = ttk.Style()
        style.theme_use("clam")

        # Configure notebook style
        style.configure(
            "TNotebook",
            background="#222222",
            borderwidth=0
        )
        style.configure(
            "TNotebook.Tab",
            background="#333333",
            foreground="#ffffff",
            padding=[20, 10],
            font=("Helvetica", 11)
        )
        style.map(
            "TNotebook.Tab",
            background=[("selected", "#555555")],
            foreground=[("selected", "#00ff00")]
        )


def main():
    root = tk.Tk()
    app = ClockApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
