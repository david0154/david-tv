# 📺 DAVID TV - Indian IPTV Player

A beautiful, feature-rich IPTV player for streaming Indian TV channels across multiple languages. Built with Python, Tkinter, and VLC.

![DAVID TV](https://img.shields.io/badge/version-1.0.1-blue)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)
![Python](https://img.shields.io/badge/python-3.8%2B-green)
![License](https://img.shields.io/badge/license-MIT-orange)

## ✨ Features

- 🌐 **Multi-Language Support**: Hindi, Bangla, Tamil, Telugu, Malayalam, Kannada, Marathi, Punjabi, Odia,Nepali, Konkani, Urdu, Assamese, Gujarati, English
- 🔍 **Real-time Search**: Quickly find your favorite channels
- ⭐ **Favorites System**: Save and manage your preferred channels
- 🎚️ **Volume Control**: Slider and keyboard shortcuts
- 🖥️ **Fullscreen Mode**: Immersive viewing experience with auto-hide controls
- ⌨️ **Keyboard Shortcuts**: Full keyboard navigation support
- 🎨 **Modern UI**: Beautiful dark theme with cyan accents
- 💾 **Persistent Settings**: Favorites are saved automatically
- 🚀 **Cross-Platform**: Works on Windows, Linux, and macOS

## 📸 Screenshots

```
┌─────────────────────────────────────────────────────────┐
│  📺 DAVID TV                                  [_][□][×] │
├──────────────┬──────────────────────────────────────────┤
│   🎬 LOGO    │                                          │
│  DAVID TV    │                                          │
│              │         VIDEO PLAYER AREA                │
│ Language ▼   │                                          │
│ Search...    │                                          │
│ ┌──────────┐ │                                          │
│ │⭐Channel1│ │                                          │
│ │ Channel2 │ │                                          │
│ │ Channel3 │ │                                          │
│ └──────────┘ │                                          │
│ 🔊 70%       │                                          │
│ ━━━━━●━━━━   │                                          │
│ 🔇 Mute      │                                          │
│ ⏮ ⏯ ⏭      │                                          │
│ ⭐ Favorite  │                                          │
│ 🖥 Fullscreen│                                          │
│ ℹ About      │                                          │
└──────────────┴──────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- VLC Media Player installed on your system

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/david0154/david-tv.git
   cd david-tv
   ```
   
### 🔹 Step 2: Create a Virtual Environment (Windows)

```bash
python -m venv venv
venv\Scripts\activate
```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python david_tv.py
   ```

## 📦 Building Executables

### Windows

```powershell
# Install PyInstaller
pip install pyinstaller

# Build executable (single line)
pyinstaller --onefile --windowed --icon=icon.ico --add-data "icon.ico;." --add-data "logo.png;." --add-data "splash.png;." --add-data "favorites.json;." --add-binary "C:\Program Files\VideoLAN\VLC\libvlc.dll;." --add-binary "C:\Program Files\VideoLAN\VLC\libvlccore.dll;." --add-data "C:\Program Files\VideoLAN\VLC\plugins;plugins" --hidden-import=vlc david_tv.py

# Or use the spec file
pyinstaller david_tv.spec
```

**Note**: Adjust VLC paths if installed in a different location.

### Linux

```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
pyinstaller --onefile --windowed --icon=icon.ico \
--add-data "icon.ico:." \
--add-data "logo.png:." \
--add-data "splash.png:." \
--add-data "favorites.json:." \
--add-binary "/usr/lib/x86_64-linux-gnu/libvlc.so.5:." \
--add-binary "/usr/lib/x86_64-linux-gnu/libvlccore.so.9:." \
--add-data "/usr/lib/x86_64-linux-gnu/vlc/plugins:plugins" \
--hidden-import=vlc \
david_tv.py
```

**Note**: VLC library paths may vary by distribution. Check with:
```bash
dpkg -L vlc-bin | grep libvlc
```

### macOS

```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
pyinstaller --onefile --windowed --icon=icon.icns \
--add-data "icon.ico:." \
--add-data "logo.png:." \
--add-data "splash.png:." \
--add-data "favorites.json:." \
--add-binary "/Applications/VLC.app/Contents/MacOS/lib/libvlc.dylib:." \
--add-binary "/Applications/VLC.app/Contents/MacOS/lib/libvlccore.dylib:." \
--add-data "/Applications/VLC.app/Contents/MacOS/plugins:plugins" \
--hidden-import=vlc \
david_tv.py
```

## ⌨️ Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Space` | Play/Pause |
| `→` / `↓` | Next Channel |
| `←` / `↑` | Previous Channel |
| `+` / `=` | Volume Up |
| `-` | Volume Down |
| `M` | Mute/Unmute |
| `F11` | Toggle Fullscreen |
| `Esc` | Exit Fullscreen |
| `Double Click` | Toggle Fullscreen |

## 🎯 Usage

1. **Select Language**: Choose from the dropdown menu
2. **Search Channels**: Type in the search box to filter channels
3. **Play Channel**: Click on any channel in the list
4. **Add to Favorites**: Select a channel and click "⭐ Favorite"
5. **Adjust Volume**: Use slider or keyboard shortcuts (`+`, `-`)
6. **Fullscreen**: Click button, press `F11`, or double-click video

## 📋 Requirements

### Python Packages
```
tkinter (usually included with Python)
python-vlc>=3.0.0
Pillow>=9.0.0
requests>=2.27.0
```

### System Requirements
- **VLC Media Player**: Must be installed separately
  - Windows: [Download VLC](https://www.videolan.org/vlc/download-windows.html)
  - Linux: `sudo apt install vlc` (Ubuntu/Debian) or `sudo yum install vlc` (Fedora/RHEL)
  - macOS: `brew install vlc` or [Download VLC](https://www.videolan.org/vlc/download-macosx.html)

## 🗂️ Project Structure

```
david-tv/
├── david_tv.py          # Main application
├── icon.ico             # Application icon
├── logo.png             # App logo (200x70)
├── splash.png           # Splash screen
├── favorites.json       # Saved favorites (auto-generated)
├── requirements.txt     # Python dependencies
├── david_tv.spec        # PyInstaller spec file
└── README.md            # This file
```

## 🔧 Configuration

### Custom IPTV Sources

Edit the `LANGUAGE_PLAYLISTS` dictionary in `david_tv.py`:

```python
LANGUAGE_PLAYLISTS = {
    "Hindi": "https://your-custom-playlist.m3u",
    "Custom": "https://another-playlist.m3u",
}
```

### Change Default Volume

Modify the `init_audio()` function:

```python
def init_audio():
    player.audio_set_volume(50)  # Set to 50%
```

## 🐛 Troubleshooting

### Volume Not Working
- Ensure VLC is properly installed
- Try running from terminal/command prompt to see error messages
- Check system audio settings

### Two Windows Appear (Windows)
- Make sure you're using the fixed code with proper VLC embedding
- Verify `--windowed` flag is used in PyInstaller command

### Channels Not Loading
- Check internet connection
- Some IPTV sources may be temporarily unavailable
- Try switching to a different language category

### Icon Not Showing
- Ensure `icon.ico` is in the same directory
- Use `--add-data "icon.ico;."` in PyInstaller command
- Check icon file is valid `.ico` format

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**David**
- Email: davidk76011@gmail.com
