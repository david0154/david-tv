import os, sys, re, threading, json, ctypes
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import requests
import vlc

# ================= WINDOWS TASKBAR ID =================
try:
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
        "Nexuzy.DavidTV.MediaPlayer"
    )
except:
    pass

# ================= APP INFO =================
APP_NAME = "DAVID TV"
VERSION = "1.0.1"
CONTACT_EMAIL = "davidk76011@gmail.com"

# ================= IPTV SOURCES =================
ALL_INDIA_PLAYLIST = "https://iptv-org.github.io/iptv/countries/in.m3u"
LANGUAGE_PLAYLISTS = {
    "Hindi": "https://iptv-org.github.io/iptv/languages/hin.m3u",
    "Bangla": "https://iptv-org.github.io/iptv/languages/ben.m3u",
    "Tamil": "https://iptv-org.github.io/iptv/languages/tam.m3u",
    "Telugu": "https://iptv-org.github.io/iptv/languages/tel.m3u",
    "Malayalam": "https://iptv-org.github.io/iptv/languages/mal.m3u",
    "Kannada": "https://iptv-org.github.io/iptv/languages/kan.m3u",
    "Marathi": "https://iptv-org.github.io/iptv/languages/mar.m3u",
    "Punjabi": "https://iptv-org.github.io/iptv/languages/pan.m3u",
    "Odia": "https://iptv-org.github.io/iptv/languages/ori.m3u",
    "English": "https://iptv-org.github.io/iptv/languages/eng.m3u",
}

# ================= RESOURCE =================
def resource(p):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, p)
    return os.path.join(os.path.abspath("."), p)

# ================= VLC PLUGIN PATH (CRITICAL FIX) =================
if hasattr(sys, "_MEIPASS"):
    os.environ["VLC_PLUGIN_PATH"] = os.path.join(sys._MEIPASS, "plugins")

# ================= FAVORITES =================
FAV_FILE = resource("favorites.json")
favorites = {}
if os.path.exists(FAV_FILE):
    try:
        favorites = json.load(open(FAV_FILE, "r", encoding="utf-8"))
    except:
        favorites = {}

def save_favs():
    json.dump(favorites, open(FAV_FILE, "w", encoding="utf-8"), indent=2)

# ================= VLC (FIXED - NO EXTRA WINDOW) =================
vlc_instance = vlc.Instance(
    "--no-video-title-show",
    "--network-caching=1000",
    "--quiet",
    "--no-xlib",  # Prevent X11 window on Linux
    "--aout=directsound"  # Force DirectSound for better audio control on Windows
)
player = vlc_instance.media_player_new()

# ================= ROOT =================
root = tk.Tk()
root.title(f"{APP_NAME} {VERSION}")
root.geometry("1200x700")
root.configure(bg="#050505")
root.withdraw()

# Initialize audio properly after root is created
def init_audio():
    try:
        player.audio_set_volume(70)  # Default volume 70%
    except:
        pass

root.after(500, init_audio)

# ================= SPLASH (FIXED – SAFE SIZE) =================
splash = tk.Toplevel(root)
splash.overrideredirect(True)
splash.configure(bg="#000")

img = Image.open(resource("splash.png"))

sw = splash.winfo_screenwidth()
sh = splash.winfo_screenheight()

# Clamp splash size to 70% of screen (SAFE ON ALL DISPLAYS)
max_w = int(sw * 0.7)
max_h = int(sh * 0.7)

img.thumbnail((max_w, max_h), Image.LANCZOS)

ph = ImageTk.PhotoImage(img)
tk.Label(splash, image=ph, bg="#000").pack()

w, h = img.size
x = (sw - w) // 2
y = (sh - h) // 2
splash.geometry(f"{w}x{h}+{x}+{y}")

# ================= FULLSCREEN + AUTO-HIDE =================
is_fullscreen = False
hide_job = None
AUTO_HIDE_DELAY = 3000

def hide_controls():
    global hide_job
    hide_job = None
    if is_fullscreen:
        left.pack_forget()
        root.config(cursor="none")

def show_controls(event=None):
    global hide_job
    if not is_fullscreen:
        if not left.winfo_ismapped():
            left.pack(side="left", fill="y")
        root.config(cursor="")
        return

    if not left.winfo_ismapped():
        left.pack(side="left", fill="y")

    root.config(cursor="")
    if hide_job:
        root.after_cancel(hide_job)
    hide_job = root.after(AUTO_HIDE_DELAY, hide_controls)

def enter_fullscreen():
    global is_fullscreen
    is_fullscreen = True
    root.attributes("-fullscreen", True)
    show_controls()
    root.after(100, attach_vlc_safe)

def exit_fullscreen():
    global is_fullscreen
    is_fullscreen = False
    root.attributes("-fullscreen", False)
    if not left.winfo_ismapped():
        left.pack(side="left", fill="y")
    root.config(cursor="")
    root.after(100, attach_vlc_safe)

def toggle_fullscreen(event=None):
    exit_fullscreen() if is_fullscreen else enter_fullscreen()

root.bind("<Motion>", show_controls)

# ================= UI =================
left = tk.Frame(root, bg="#0b0b0b", width=320,
                highlightbackground="#00e5ff", highlightthickness=2)
left.pack(side="left", fill="y")

right = tk.Frame(root, bg="black")
right.pack(side="right", fill="both", expand=True)

video = tk.Frame(right, bg="black")
video.pack(fill="both", expand=True)

# ================= VLC ATTACH (CRITICAL FIX) =================
def attach_vlc_safe():
    try:
        # Force update to get valid window handle
        root.update_idletasks()
        video.update()
        
        # Get window handle
        handle = video.winfo_id()
        
        # Set window handle based on platform
        if sys.platform.startswith('linux'):
            player.set_xwindow(handle)
        elif sys.platform == "win32":
            player.set_hwnd(handle)
        elif sys.platform == "darwin":
            player.set_nsobject(handle)
        
        # Disable mouse/keyboard input to VLC (keep in tkinter)
        player.video_set_mouse_input(False)
        player.video_set_key_input(False)
        
    except Exception as e:
        print(f"VLC attach error: {e}")

# ================= LEFT CONTENT =================
logo_img = ImageTk.PhotoImage(Image.open(resource("logo.png")).resize((200, 70)))
tk.Label(left, image=logo_img, bg="#0b0b0b").pack(pady=10)

tk.Label(left, text=APP_NAME, fg="#00e5ff", bg="#0b0b0b",
         font=("Segoe UI", 18, "bold")).pack()

lang = tk.StringVar(value="All Indian Channels")
ttk.Combobox(
    left,
    values=["All Indian Channels"] + list(LANGUAGE_PLAYLISTS.keys()),
    textvariable=lang,
    state="readonly"
).pack(fill="x", padx=10, pady=5)

search = tk.Entry(left, bg="#000", fg="#00e5ff", insertbackground="#00e5ff")
search.pack(fill="x", padx=10, pady=5)

listbox = tk.Listbox(
    left, bg="#000", fg="white",
    selectbackground="#00e5ff",
    font=("Segoe UI", 11),
    activestyle="none"
)
listbox.pack(fill="both", expand=True, padx=10, pady=10)

# ================= DATA =================
channels, filtered = [], []
current_index = -1

def refresh_list():
    listbox.delete(0, "end")
    favs = favorites.get(lang.get(), [])
    for c in filtered:
        listbox.insert("end", ("⭐ " if c["url"] in favs else "") + c["name"])

def load_playlist(url):
    temp = []
    try:
        lines = requests.get(url, timeout=20).text.splitlines()
    except:
        return temp
    name = None
    for line in lines:
        if line.startswith("#EXTINF"):
            m = re.search(r",(.+)", line)
            name = m.group(1) if m else "Unknown"
        elif line.startswith("http"):
            temp.append({"name": name, "url": line})
    return temp

def apply_language(*_):
    def task():
        url = ALL_INDIA_PLAYLIST if lang.get() == "All Indian Channels" else LANGUAGE_PLAYLISTS[lang.get()]
        temp = load_playlist(url)
        def ui():
            global channels, filtered
            channels = temp
            filtered = channels[:]
            refresh_list()
        root.after(0, ui)
    threading.Thread(target=task, daemon=True).start()

lang.trace("w", apply_language)

def apply_search(e=None):
    global filtered
    q = search.get().lower()
    filtered = [c for c in channels if q in c["name"].lower()]
    refresh_list()

search.bind("<KeyRelease>", apply_search)

def play_index(i):
    global current_index
    if 0 <= i < len(filtered):
        current_index = i
        media = vlc_instance.media_new(filtered[i]["url"])
        player.set_media(media)
        player.play()
        # Restore volume after media change
        root.after(100, lambda: player.audio_set_volume(int(volume_slider.get())))
        # Re-attach after media change
        root.after(50, attach_vlc_safe)
        root.after(200, update_volume_display)

def on_select(e):
    if listbox.curselection():
        play_index(listbox.curselection()[0])

listbox.bind("<<ListboxSelect>>", on_select)

# ================= KEYBOARD =================
def on_key(e):
    if e.keysym in ("Right", "Down"):
        play_index(min(len(filtered)-1, current_index+1))
    elif e.keysym in ("Left", "Up"):
        play_index(max(0, current_index-1))
    elif e.keysym == "space":
        player.pause()
    elif e.keysym == "F11":
        toggle_fullscreen()
    elif e.keysym in ("plus", "equal", "KP_Add"):
        # Volume up with +, =, or numpad +
        try:
            current = player.audio_get_volume()
            if current < 0:
                current = 70
            vol = min(100, current + 5)
            player.audio_set_volume(vol)
            volume_slider.set(vol)
            volume_label.config(text=f"🔊 {vol}%")
            print(f"Volume UP: {vol}%")
        except Exception as e:
            print(f"Volume up error: {e}")
    elif e.keysym in ("minus", "underscore", "KP_Subtract"):
        # Volume down with -, _, or numpad -
        try:
            current = player.audio_get_volume()
            if current < 0:
                current = 70
            vol = max(0, current - 5)
            player.audio_set_volume(vol)
            volume_slider.set(vol)
            volume_label.config(text=f"🔊 {vol}%")
            print(f"Volume DOWN: {vol}%")
        except Exception as e:
            print(f"Volume down error: {e}")
    elif e.keysym in ("m", "M"):
        # Mute/unmute with M
        toggle_mute()

root.bind("<Key>", on_key)

# ================= FAVORITE =================
def toggle_favorite():
    favorites.setdefault(lang.get(), [])
    sel = listbox.curselection()
    if not sel:
        return
    url = filtered[sel[0]]["url"]
    if url in favorites[lang.get()]:
        favorites[lang.get()].remove(url)
    else:
        favorites[lang.get()].append(url)
    save_favs()
    refresh_list()

# ================= ABOUT =================
def show_about():
    messagebox.showinfo(
        "About DAVID TV",
        "DAVID TV\n\nApplication by David\n"
        f"Contact: {CONTACT_EMAIL}\n\n"
        "Powered by Nexuzy Tech Pvt Ltd This software uses publicly available IPTV streams.No content is hosted or redistributed.\n\n"
        "© Nexuzy Tech Pvt Ltd"
    )

# ================= VOLUME CONTROL =================
def on_volume_change(val):
    try:
        vol = int(float(val))
        player.audio_set_volume(vol)
        volume_label.config(text=f"🔊 {vol}%")
    except Exception as e:
        print(f"Volume error: {e}")

def update_volume_display():
    """Update volume display from actual player volume"""
    try:
        current_vol = player.audio_get_volume()
        if current_vol >= 0:  # Valid volume
            volume_slider.set(current_vol)
            volume_label.config(text=f"🔊 {current_vol}%")
    except:
        pass

volume_frame = tk.Frame(left, bg="#0b0b0b")
volume_frame.pack(fill="x", padx=10, pady=10)

volume_label = tk.Label(volume_frame, text="🔊 70%", fg="#00e5ff", bg="#0b0b0b",
                        font=("Segoe UI", 10, "bold"))
volume_label.pack()

# Custom style for better visibility
style = ttk.Style()
style.theme_use('default')
style.configure("Volume.Horizontal.TScale", background="#0b0b0b")

volume_slider = ttk.Scale(
    volume_frame,
    from_=0,
    to=100,
    orient="horizontal",
    command=on_volume_change,
    style="Volume.Horizontal.TScale"
)
volume_slider.set(70)
volume_slider.pack(fill="x", pady=5)

# Mute button
def toggle_mute():
    try:
        is_muted = player.audio_get_mute()
        player.audio_set_mute(not is_muted)
        is_muted = player.audio_get_mute()
        mute_btn.config(text="🔈 Unmute" if is_muted else "🔇 Mute")
        if is_muted:
            volume_label.config(text="🔇 Muted")
        else:
            update_volume_display()
    except Exception as e:
        print(f"Mute error: {e}")

mute_btn = tk.Button(volume_frame, text="🔇 Mute", command=toggle_mute,
                     bg="#000", fg="#00e5ff", relief="flat", 
                     font=("Segoe UI", 9))
mute_btn.pack(pady=5, fill="x")

# ================= CONTROLS =================
btns = tk.Frame(left, bg="#0b0b0b")
btns.pack(pady=6)

for t, f in [
    ("⏮", lambda: play_index(current_index-1)),
    ("⏯", player.pause),
    ("⏭", lambda: play_index(current_index+1)),
]:
    tk.Button(btns, text=t, command=f,
              bg="#000", fg="#00e5ff", relief="flat").pack(side="left", padx=2)

tk.Button(left, text="⭐ Favorite", command=toggle_favorite,
          bg="#000", fg="#00e5ff", relief="flat").pack(pady=4)

tk.Button(left, text="🖥 Fullscreen", command=toggle_fullscreen,
          bg="#000", fg="#00e5ff", relief="flat").pack(pady=4)

tk.Button(left, text="ℹ About", command=show_about,
          bg="#000", fg="#00e5ff", relief="flat").pack(pady=4)

video.bind("<Double-Button-1>", toggle_fullscreen)
root.bind("<Escape>", lambda e: exit_fullscreen())

# ================= START =================
def show_main():
    splash.destroy()
    root.deiconify()
    # Set icon with proper error handling
    try:
        icon_path = resource("icon.ico")
        if os.path.exists(icon_path):
            root.iconbitmap(icon_path)
        else:
            print(f"Icon not found at: {icon_path}")
    except Exception as e:
        print(f"Could not set icon: {e}")
    # Initial attach with delay
    root.after(300, attach_vlc_safe)

root.after(2000, show_main)
apply_language()
root.mainloop()