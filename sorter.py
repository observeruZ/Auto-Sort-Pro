import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter.font import Font

APP_TITLE = "Auto Sort Pro"
APP_VERSION = "1.0"

class AutoSortApp:
    def __init__(self):
        self.app = tk.Tk()
        self.app.title(f"{APP_TITLE} v{APP_VERSION}")
        self.app.geometry("520x580")
        self.app.resizable(False, False)

        self.is_dark_mode = True
        self.apply_theme()
        self.setup_menu()
        self.setup_ui()

    def apply_theme(self):
        if self.is_dark_mode:
            self.bg_color = "#0f172a"
            self.fg_color = "#e5e7eb"
            self.accent = "#2563eb"
            self.success = "#16a34a"
            self.danger = "#dc2626"
            self.warning = "#f59e0b"
            self.muted = "#94a3b8"
        else:
            self.bg_color = "#f8fafc"
            self.fg_color = "#1e2937"
            self.accent = "#3b82f6"
            self.success = "#22c55e"
            self.danger = "#ef4444"
            self.warning = "#f59e0b"
            self.muted = "#64748b"
        self.app.configure(bg=self.bg_color)

    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        self.apply_theme()
        self.refresh_ui()

    def setup_menu(self):
        menubar = tk.Menu(self.app)
        self.app.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Select Folder", command=self.select_and_sort)
        file_menu.add_command(label="Auto Scan Downloads", command=self.auto_scan_downloads)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.app.quit)

        theme_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Theme", menu=theme_menu)
        theme_menu.add_command(label="Toggle Dark/Light Mode", command=self.toggle_theme)

        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)

    def setup_ui(self):
        header = tk.Frame(self.app, bg=self.bg_color)
        header.pack(fill="x", pady=25)

        title_font = Font(family="Segoe UI", size=24, weight="bold")
        tk.Label(header, text="📁 Auto Sort Pro", font=title_font, bg=self.bg_color, fg=self.fg_color).pack()
        tk.Label(header, text="Organize your files smarter", bg=self.bg_color, fg=self.muted, 
                 font=("Segoe UI", 12)).pack()

        main_frame = tk.Frame(self.app, bg=self.bg_color)
        main_frame.pack(pady=10, padx=50, fill="both", expand=True)

        # Sort Section
        tk.Label(main_frame, text="Sort Files", font=("Segoe UI", 13, "bold"),
                 bg=self.bg_color, fg=self.accent).pack(anchor="w", pady=(15,8))

        self.sort_btn1 = tk.Button(main_frame, text="📁 Select Folder to Sort", width=35, height=2,
                                   bg=self.accent, fg="white", font=("Segoe UI", 10),
                                   command=self.select_and_sort)
        self.sort_btn1.pack(pady=8)

        self.sort_btn2 = tk.Button(main_frame, text="⚡ Auto Scan Downloads", width=35, height=2,
                                   bg=self.success, fg="white", font=("Segoe UI", 10),
                                   command=self.auto_scan_downloads)
        self.sort_btn2.pack(pady=8)

        # Separator
        ttk.Separator(main_frame, orient="horizontal").pack(fill="x", pady=25)

        # Restore Section
        tk.Label(main_frame, text="Restore Files", font=("Segoe UI", 13, "bold"),
                 bg=self.bg_color, fg=self.danger).pack(anchor="w", pady=(10,8))

        tk.Button(main_frame, text="🔄 Unsort Selected Folder", width=35, height=2,
                  bg=self.danger, fg="white", font=("Segoe UI", 10),
                  command=self.select_and_unsort).pack(pady=8)

        tk.Button(main_frame, text="↩️ Restore Downloads", width=35, height=2,
                  bg=self.warning, fg="white", font=("Segoe UI", 10),
                  command=self.restore_downloads).pack(pady=8)

        # Status Area
        status_frame = tk.Frame(self.app, bg=self.bg_color)
        status_frame.pack(pady=20, fill="x", padx=40)

        self.progress = ttk.Progressbar(status_frame, orient="horizontal", length=420, mode="determinate")
        self.progress.pack()

        self.status = tk.Label(self.app, text="Ready • Choose an action", bg=self.bg_color, 
                               fg=self.muted, font=("Segoe UI", 10))
        self.status.pack(pady=12)

        tk.Label(self.app, text=f"Made by Benjie • v{APP_VERSION}", bg=self.bg_color, 
                 fg=self.muted, font=("Segoe UI", 9)).pack(side="bottom", pady=20)

    def refresh_ui(self):
        for widget in self.app.winfo_children():
            widget.destroy()
        self.setup_ui()

    def update_status(self, text: str, progress: int = None):
        self.status.config(text=text)
        if progress is not None:
            self.progress["value"] = progress
        self.app.update_idletasks()

    def show_about(self):
        messagebox.showinfo("About Auto Sort Pro", 
            f"{APP_TITLE} v{APP_VERSION}\n\nSimple yet powerful file organizer.\nMade with ❤️ by Benji")

    # === ACTIONS ===
    def select_and_sort(self):
        folder = filedialog.askdirectory()
        if folder:
            self.update_status("Analyzing folder...", 0)
            total = sort_files(folder)
            self.update_status(f"Done! {total} files sorted", 100)
            messagebox.showinfo("Success", f"{total} files were successfully organized!")

    def auto_scan_downloads(self):
        downloads = get_downloads_folder()
        self.update_status("Scanning Downloads...", 0)
        total = sort_files(downloads)
        self.update_status(f"Done! {total} files sorted", 100)
        messagebox.showinfo("Success", f"{total} files sorted from Downloads!")

    def select_and_unsort(self):
        folder = filedialog.askdirectory()
        if folder:
            self.update_status("Restoring files...", 0)
            total = unsort_files(folder)
            self.update_status("Restore completed", 100)
            messagebox.showinfo("Done", f"{total} files restored.")

    def restore_downloads(self):
        downloads = get_downloads_folder()
        self.update_status("Restoring Downloads...", 0)
        total = unsort_files(downloads)
        self.update_status("Restore completed", 100)
        messagebox.showinfo("Done", f"{total} files restored.")


# ====================== HELPER FUNCTIONS ======================
def get_downloads_folder():
    return os.path.join(os.path.expanduser("~"), "Downloads")

def get_file_category(filename: str) -> str:
    ext = filename.split(".")[-1].lower() if "." in filename else ""
    categories = {
        "mp3": "Music", "jpg": "Photos", "jpeg": "Photos", "png": "Photos", "gif": "Photos",
        "mp4": "Videos", "avi": "Videos", "mkv": "Videos", "mov": "Videos",
        "pdf": "Documents", "doc": "Documents", "docx": "Documents",
        "txt": "Documents", "xlsx": "Documents", "csv": "Documents",
        "zip": "Archives", "rar": "Archives", "7z": "Archives",
    }
    return categories.get(ext, "Others")

def sort_files(folder_path: str):
    if not os.path.exists(folder_path): return 0
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    if not files: return 0

    sorted_folder = os.path.join(folder_path, "Sorted")
    os.makedirs(sorted_folder, exist_ok=True)
    count = 0
    for file in files:
        try:
            category = get_file_category(file)
            target = os.path.join(sorted_folder, category)
            os.makedirs(target, exist_ok=True)
            shutil.move(os.path.join(folder_path, file), os.path.join(target, file))
            count += 1
        except:
            continue
    return count

def unsort_files(folder_path: str):
    sorted_folder = os.path.join(folder_path, "Sorted")
    if not os.path.exists(sorted_folder): return 0
    count = 0
    for root, _, files in os.walk(sorted_folder):
        for file in files:
            try:
                shutil.move(os.path.join(root, file), os.path.join(folder_path, file))
                count += 1
            except:
                continue
    return count


if __name__ == "__main__":
    AutoSortApp().app.mainloop()
