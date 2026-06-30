import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter.font import Font

# ========================= CONFIG =========================
APP_TITLE = "Auto Sort Pro v1.0"
APP_VERSION = "1.0"

# Colors
BG_COLOR = "#0f172a"
FG_COLOR = "#e5e7eb"
BTN_COLOR = "#2563eb"
SUCCESS_COLOR = "#16a34a"
DANGER_COLOR = "#dc2626"
WARNING_COLOR = "#f59e0b"
ACCENT_COLOR = "#64748b"

# ========================= HELPERS =========================
def get_downloads_folder():
    """Return the user's Downloads folder path."""
    return os.path.join(os.path.expanduser("~"), "Downloads")


def get_file_category(filename: str) -> str:
    """Return category folder name based on file extension."""
    ext = filename.split(".")[-1].lower() if "." in filename else "unknown"
    
    categories = {
        "mp3": "Music",
        "jpg": "Photos", "jpeg": "Photos", "png": "Photos", "gif": "Photos",
        "mp4": "Videos", "avi": "Videos", "mkv": "Videos", "mov": "Videos",
        "pdf": "Documents", "doc": "Documents", "docx": "Documents",
        "txt": "Documents", "xlsx": "Documents", "csv": "Documents",
        "zip": "Archives", "rar": "Archives", "7z": "Archives",
    }
    
    return categories.get(ext, "Others")


def sort_files(folder_path: str):
    """Sort files in the given folder into category subfolders."""
    if not os.path.exists(folder_path):
        return 0

    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    total_files = len(files)

    if total_files == 0:
        return 0

    sorted_folder = os.path.join(folder_path, "Sorted")
    os.makedirs(sorted_folder, exist_ok=True)

    count = 0

    for file in files:
        file_path = os.path.join(folder_path, file)
        category = get_file_category(file)
        
        target_folder = os.path.join(sorted_folder, category)
        os.makedirs(target_folder, exist_ok=True)

        try:
            shutil.move(file_path, os.path.join(target_folder, file))
            count += 1
        except Exception:
            continue  # Skip files that can't be moved

    return count


def unsort_files(folder_path: str):
    """Move all files from Sorted/ subfolders back to main folder."""
    sorted_folder = os.path.join(folder_path, "Sorted")
    
    if not os.path.exists(sorted_folder):
        return 0

    count = 0

    for root, _, files in os.walk(sorted_folder):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                shutil.move(file_path, os.path.join(folder_path, file))
                count += 1
            except Exception:
                continue

    # Remove empty Sorted folder
    try:
        os.rmdir(sorted_folder)
    except OSError:
        pass  # Folder not empty

    return count


# ========================= UI =========================
class AutoSortApp:
    def __init__(self):
        self.app = tk.Tk()
        self.app.title(APP_TITLE)
        self.app.geometry("460x420")
        self.app.configure(bg=BG_COLOR)
        self.app.resizable(False, False)

        self.setup_ui()

    def setup_ui(self):
        # Title
        title_font = Font(family="Segoe UI", size=18, weight="bold")
        tk.Label(self.app, text="Auto Sort Pro", font=title_font,
                 bg=BG_COLOR, fg=FG_COLOR).pack(pady=20)

        # Buttons
        btn_width = 28
        btn_height = 2

        tk.Button(self.app, text="📁 Select Folder to Sort", width=btn_width, height=btn_height,
                  bg=BTN_COLOR, fg="white", font=("Segoe UI", 10),
                  command=self.select_and_sort).pack(pady=8)

        tk.Button(self.app, text="⚡ Auto Scan Downloads", width=btn_width, height=btn_height,
                  bg=SUCCESS_COLOR, fg="white", font=("Segoe UI", 10),
                  command=self.auto_scan_downloads).pack(pady=8)

        tk.Button(self.app, text="🔄 Unsort Selected Folder", width=btn_width, height=btn_height,
                  bg=DANGER_COLOR, fg="white", font=("Segoe UI", 10),
                  command=self.select_and_unsort).pack(pady=8)

        tk.Button(self.app, text="↩️ Restore Downloads", width=btn_width, height=btn_height,
                  bg=WARNING_COLOR, fg="white", font=("Segoe UI", 10),
                  command=self.restore_downloads).pack(pady=8)

        # Progress Bar
        self.progress = ttk.Progressbar(self.app, orient="horizontal", 
                                       length=380, mode="determinate")
        self.progress.pack(pady=20)

        # Status
        self.status = tk.Label(self.app, text="Ready to organize your files", 
                               bg=BG_COLOR, fg="#94a3b8", font=("Segoe UI", 10))
        self.status.pack(pady=5)

        # Footer
        tk.Label(self.app, text=f"v{APP_VERSION} • Made by Benjie", 
                 bg=BG_COLOR, fg=ACCENT_COLOR, font=("Segoe UI", 9)).pack(side="bottom", pady=15)

    def update_status(self, text: str, progress_value: int = None):
        self.status.config(text=text)
        if progress_value is not None:
            self.progress["value"] = progress_value
        self.app.update_idletasks()

    def select_and_sort(self):
        folder = filedialog.askdirectory()
        if folder:
            self.update_status("Sorting files...", 0)
            total = sort_files(folder)
            self.update_status("Sorting completed!", 100)
            messagebox.showinfo("Success", f"{total} files successfully sorted!")

    def auto_scan_downloads(self):
        downloads = get_downloads_folder()
        self.update_status("Scanning Downloads folder...", 0)
        total = sort_files(downloads)
        self.update_status("Sorting completed!", 100)
        messagebox.showinfo("Success", f"{total} files sorted from Downloads!")

    def select_and_unsort(self):
        folder = filedialog.askdirectory()
        if folder:
            self.update_status("Restoring files...", 0)
            total = unsort_files(folder)
            self.update_status("Files restored!", 100)
            messagebox.showinfo("Done", f"{total} files restored to original location.")

    def restore_downloads(self):
        downloads = get_downloads_folder()
        self.update_status("Restoring Downloads...", 0)
        total = unsort_files(downloads)
        self.update_status("Restore completed!", 100)
        messagebox.showinfo("Done", f"{total} files restored from Downloads!")


# ========================= RUN APP =========================
if __name__ == "__main__":
    app = AutoSortApp()
    app.app.mainloop()
