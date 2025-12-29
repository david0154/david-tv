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
VERSION = "1.0.2"
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
    "Gujarati": "https://iptv-org.github.io/iptv/languages/guj.m3u",
    "Assamese": "https://iptv-org.github.io/iptv/languages/asm.m3u",
    "Odia": "https://iptv-org.github.io/iptv/languages/ori.m3u",
    "Urdu": "https://iptv-org.github.io/iptv/languages/urd.m3u", 
    "Konkani": "https://iptv-org.github.io/iptv/languages/kok.m3u",
    "Nepali": "https://iptv-org.github.io/iptv/languages/nep.m3u",
    "English": "https://iptv-org.github.io/iptv/languages/eng.m3u",
}

# ================= RESOURCE =================
def resource(p):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, p)
    return os.path.join(os.path.abspath("."), p)

# ================= VLC PLUGIN PATH =================
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

# ================= VLC INSTANCE (FIXED FOR SCREEN RECORDING) =================
# Key fix: Remove --aout=adummy to allow audio to be captured by screen recorders
# Use default audio output which works with virtual audio devices
vlc_args = [
    "--no-video-title-show",
    "--network-caching=1000",
    "--quiet",
    "--no-xlib",
    "--verbose=0"
]

# On Windows, prefer DirectSound for better compatibility
if sys.platform == "win32":
    vlc_args.append("--aout=directsound")

vlc_instance = vlc.Instance(*vlc_args)
player = vlc_instance.media_player_new()

# ================= DEFAULT VOLUME =================
DEFAULT_VOLUME = 75  # Set to 75% as requested

# ================= ROOT =================
root = tk.Tk()
root.title(f"{APP_NAME} {VERSION}")
root.geometry("1200x700")
root.configure(bg="#050505")
root.withdraw()

# Initialize audio with 75% default volume
def init_audio():
    try:
        # Set default volume to 75%
        player.audio_set_volume(DEFAULT_VOLUME)
        print(f"✓ Default volume set to {DEFAULT_VOLUME}%")
        
        # Check if audio output is available
        audio_output = player.audio_output_device_enum()
        
        if audio_output is None:
            print("⚠️ WARNING: No physical audio devices detected!")
            print("Audio will still work for screen recording if virtual audio device is present")
        else:
            print("✓ Audio devices found - audio will play normally")
            try:
                vlc.libvlc_audio_output_device_list_release(audio_output)
            except:
                pass
        
    except Exception as e:
        print(f"Audio init error: {e}")
        # Still set volume even if check fails
        try:
            player.audio_set_volume(DEFAULT_VOLUME)
        except:
            pass

root.after(500, init_audio)

# ================= SPLASH =================
splash = tk.Toplevel(root)
splash.overrideredirect(True)
splash.configure(bg="#000")

img = Image.open(resource("splash.png"))

sw = splash.winfo_screenwidth()
sh = splash.winfo_screenheight()

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

# ================= VLC ATTACH =================
def attach_vlc_safe():
    try:
        root.update_idletasks()
        video.update()
        
        handle = video.winfo_id()
        
        if sys.platform.startswith('linux'):
            player.set_xwindow(handle)
        elif sys.platform == "win32":
            player.set_hwnd(handle)
        elif sys.platform == "darwin":
            player.set_nsobject(handle)
        
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
        # CRITICAL: Restore volume to 75% (or current slider value) after media change
        root.after(100, lambda: player.audio_set_volume(int(volume_slider.get())))
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
        try:
            current = player.audio_get_volume()
            if current < 0:
                current = DEFAULT_VOLUME
            vol = min(100, current + 5)
            player.audio_set_volume(vol)
            volume_slider.set(vol)
            volume_label.config(text=f"🔊 {vol}%")
        except Exception as e:
            print(f"Volume up error: {e}")
    elif e.keysym in ("minus", "underscore", "KP_Subtract"):
        try:
            current = player.audio_get_volume()
            if current < 0:
                current = DEFAULT_VOLUME
            vol = max(0, current - 5)
            player.audio_set_volume(vol)
            volume_slider.set(vol)
            volume_label.config(text=f"🔊 {vol}%")
        except Exception as e:
            print(f"Volume down error: {e}")
    elif e.keysym in ("m", "M"):
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

# ================= AUDIO DEVICE CHECK =================
def check_audio_devices():
    """Check and display available audio devices"""
    try:
        audio_output = player.audio_output_device_enum()
        
        if audio_output is None:
            return ("No physical audio devices detected\n\n"
                   "✓ Audio streams are active and can be captured by screen recorders\n"
                   "✓ Install a virtual audio cable if you need to hear sound\n\n"
                   "Recommended: VB-Audio Virtual Cable or similar")
        
        devices = []
        device = audio_output
        while device:
            try:
                desc = device.contents.description.decode('utf-8')
                devices.append(desc)
            except:
                devices.append("Unknown device")
            device = device.contents.next
        
        try:
            vlc.libvlc_audio_output_device_list_release(audio_output)
        except:
            pass
            
        return "✓ Audio devices found:\n\n" + "\n".join(devices) if devices else "No devices found"
        
    except Exception as e:
        return f"Error checking devices: {e}"

def show_audio_info():
    devices = check_audio_devices()
    messagebox.showinfo("Audio Devices", devices)

# ================= ABOUT =================
def show_about():
    messagebox.showinfo(
        "About DAVID TV",
        f"DAVID TV v{VERSION}\n\nApplication by David\n"
        f"Contact: {CONTACT_EMAIL}\n\n"
        "Powered by Nexuzy Tech Pvt Ltd\n\n"
        "This software uses publicly available IPTV streams.\n"
        "No content is hosted or redistributed.\n\n"
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
        if current_vol >= 0:
            volume_slider.set(current_vol)
            volume_label.config(text=f"🔊 {current_vol}%")
        else:
            # If volume reading fails, set to default
            player.audio_set_volume(DEFAULT_VOLUME)
            volume_slider.set(DEFAULT_VOLUME)
            volume_label.config(text=f"🔊 {DEFAULT_VOLUME}%")
    except:
        pass

volume_frame = tk.Frame(left, bg="#0b0b0b")
volume_frame.pack(fill="x", padx=10, pady=10)

volume_label = tk.Label(volume_frame, text=f"🔊 {DEFAULT_VOLUME}%", fg="#00e5ff", bg="#0b0b0b",
                        font=("Segoe UI", 10, "bold"))
volume_label.pack()

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
volume_slider.set(DEFAULT_VOLUME)  # Set slider to 75%
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

tk.Button(left, text="🔊 Audio Info", command=show_audio_info,
          bg="#000", fg="#00e5ff", relief="flat").pack(pady=4)

tk.Button(left, text="ℹ About", command=show_about,
          bg="#000", fg="#00e5ff", relief="flat").pack(pady=4)

video.bind("<Double-Button-1>", toggle_fullscreen)
root.bind("<Escape>", lambda e: exit_fullscreen())

# ================= START =================
def show_main():
    splash.destroy()
    root.deiconify()
    try:
        icon_path = resource("icon.ico")
        if os.path.exists(icon_path):
            root.iconbitmap(icon_path)
    except Exception as e:
        print(f"Could not set icon: {e}")
    root.after(300, attach_vlc_safe)
    # Ensure volume is set after main window shows
    root.after(500, lambda: player.audio_set_volume(DEFAULT_VOLUME))

root.after(2000, show_main)
apply_language()
root.mainloop()
