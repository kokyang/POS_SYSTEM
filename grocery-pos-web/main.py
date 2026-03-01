"""
NAM CHONG MINI MARKET — POS System
Windows Desktop App Entry Point

Wraps the Flask web app inside a native pywebview window.
Double-click to launch — no browser needed.
"""

import sys
import os
import threading
import time


# ─── Path helpers ─────────────────────────────────────────────────────────────

def resource_path(*parts):
    """
    Resolve paths to bundled resources.
    Works both in development (plain Python) and when frozen by PyInstaller.
    """
    if getattr(sys, 'frozen', False):
        base = sys._MEIPASS          # PyInstaller temp folder
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, *parts)


def data_dir():
    """
    Returns a writable folder for the database and other persistent data.
    Uses ~/Documents/NamChongPOS/ so data survives app updates.
    """
    if getattr(sys, 'frozen', False):
        folder = os.path.join(os.path.expanduser('~'), 'Documents', 'NamChongPOS')
    else:
        folder = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(folder, exist_ok=True)
    return folder


# Tell database.py and app.py where things live before they are imported
os.environ['POS_TEMPLATE_FOLDER'] = resource_path('templates')
os.environ['POS_DATA_DIR']        = data_dir()

# ─── Flask + pywebview ────────────────────────────────────────────────────────

PORT = 8765   # internal port — not exposed to the network


def start_flask():
    from app import app
    app.run(
        host='127.0.0.1',
        port=PORT,
        debug=False,
        use_reloader=False,
        threaded=True,
    )


def main():
    import webview

    # Start Flask in a background daemon thread
    flask_thread = threading.Thread(target=start_flask, daemon=True)
    flask_thread.start()

    # Give Flask a moment to start up before opening the window
    time.sleep(1.2)

    # Open the native window
    webview.create_window(
        title='NAM CHONG MINI MARKET — POS',
        url=f'http://127.0.0.1:{PORT}',
        width=1366,
        height=768,
        resizable=True,
        min_size=(1100, 650),
    )
    webview.start()


if __name__ == '__main__':
    main()
