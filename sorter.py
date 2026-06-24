import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

APP_TITLE = "Auto Sort Pro v1.0"

BG_COLOR = "#0f172a"
FG_COLOR = "#e5e7eb"
BTN_COLOR = "#2563eb"

def get_downloads_folder():
    return os.path.join(os.path.expanduser("~"), "Downloads")

def sort_files(folder_path):
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    total_files = len(files)

    if total_files == 0:
        return 0

    output_folder = os.path.join(folder_path, "Sorted")
    os.makedirs(output_folder, exist_ok=True)

    count = 0

    for file in files:
        file_path = os.path.join(folder_path, file)
        ext = file.split(".")[-1].lower()

        if ext == "mp3":
            category = "Music"
        elif ext in ["jpg", "jpeg", "png"]:
            category = "Photos"
        elif ext in ["mp4", "avi", "mkv"]:
            category = "Videos"
        else:
            category = "Others"

        target_folder = os.path.join(output_folder, category)
        os.makedirs(target_folder, exist_ok=True)

        try:
            shutil.move(file_path, os.path.join(target_folder, file))
            count += 1

            progress = int((count / total_files) * 100)
            progress_bar["value"] = progress
            status_label.config(text=f"Sorting... {progress}%")
            app.update_idletasks()
        except:
            pass

    return count

# 🔄 UNSORT FUNCTION
def unsort_files(folder_path):
    sorted_folder = os.path.join(folder_path, "Sorted")

    if not os.path.exists(sorted_folder):
        return 0

    count = 0

    for root, dirs, files in os.walk(sorted_folder):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                shutil.move(file_path, os.path.join(folder_path, file))
                count += 1
            except:
                pass

    return count

def run_sort(folder):
    progress_bar["value"] = 0
    status_label.config(text="Sorting...")
    app.update_idletasks()

    total = sort_files(folder)

    status_label.config(text="Done!")
    messagebox.showinfo("Success", f"{total} files sorted!")

def run_unsort(folder):
    progress_bar["value"] = 0
    status_label.config(text="Restoring...")
    app.update_idletasks()

    total = unsort_files(folder)

    status_label.config(text="Restored!")
    messagebox.showinfo("Done", f"{total} files restored!")

def select_folder():
    folder = filedialog.askdirectory()
    if folder:
        run_sort(folder)

def auto_scan():
    downloads = get_downloads_folder()
    run_sort(downloads)

def auto_unsort():
    downloads = get_downloads_folder()
    run_unsort(downloads)

# UI
app = tk.Tk()
app.title(APP_TITLE)
app.geometry("420x340")
app.configure(bg=BG_COLOR)

title_label = tk.Label(app, text="Auto Sort Pro",
                       font=("Segoe UI", 16),
                       bg=BG_COLOR, fg=FG_COLOR)
title_label.pack(pady=15)

# Buttons
tk.Button(app, text="Select Folder", width=22, height=2,
          bg=BTN_COLOR, fg="white",
          command=select_folder).pack(pady=5)

tk.Button(app, text="Auto Scan Downloads", width=22, height=2,
          bg="#16a34a", fg="white",
          command=auto_scan).pack(pady=5)

# 🔄 Unsort buttons
tk.Button(app, text="Unsort Selected Folder", width=22, height=2,
          bg="#dc2626", fg="white",
          command=lambda: run_unsort(filedialog.askdirectory())).pack(pady=5)

tk.Button(app, text="Restore Downloads", width=22, height=2,
          bg="#f59e0b", fg="white",
          command=auto_unsort).pack(pady=5)

progress_bar = ttk.Progressbar(app, orient="horizontal", length=300, mode="determinate")
progress_bar.pack(pady=15)

status_label = tk.Label(app, text="Status: Waiting",
                        bg=BG_COLOR, fg="#9ca3af")
status_label.pack(pady=10)

tk.Label(app, text="by Benjie", bg=BG_COLOR, fg="#6b7280").pack()

app.mainloop()