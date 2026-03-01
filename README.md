# 🛒 NAM CHONG MINI MARKET — POS System

A lightweight **Point of Sale (POS)** system built for small grocery stores. Runs as a **native Windows desktop app** or in any web browser — no extra software needed on the cashier's side.

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.1-black?logo=flask)
![SQLite](https://img.shields.io/badge/Database-SQLite-blue?logo=sqlite)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📸 Screenshots

### POS Terminal
> Split-screen layout — order list on the left, numpad + input on the right.

```
┌─────────────────────────────┬──────────────────────────┐
│  🧾 Current Order           │  [Barcode Scan] [Manual] │
│ ─────────────────────────── │                          │
│  # │ Item       │ Qty │ RM  │  ┌──────────────────┐   │
│  1 │ Gardenia   │  2  │3.00 │  │  Scan barcode…   │   │
│  2 │ Milo 3-in1 │  1  │5.50 │  └──────────────────┘   │
│  3 │ Item (Manu)│  1  │2.00 │                          │
│                             │  [7][8][9]               │
│                             │  [4][5][6]               │
│  Order Total                │  [1][2][3]               │
│  RM 10.50                   │  [.][0][⌫]               │
│                             │                          │
│                             │  QTY: [-] 1 [+]  [ADD]  │
│                             │  💵 Cash                 │
│                             │  Customer Pays: 20.00    │
│                             │  Change 找零:  RM 9.50   │
│                             │  [✓ CHECKOUT]  [CLEAR]   │
└─────────────────────────────┴──────────────────────────┘
```

> 📷 *Replace this section with actual screenshots after launching the app.*

---

## ✨ Features

- **Windows desktop app** — runs as a native `.exe`, no browser needed
- **Split-screen POS layout** — order list on the left, controls on the right
- **Barcode scanner support** — plug in any USB barcode scanner; items are looked up automatically
- **Manual entry mode** — type item name + enter price via on-screen numpad
- **On-screen numpad** — large touch-friendly buttons for price and payment input
- **Real-time change calculator** — shows 找零 (change) instantly with quick-cash buttons (RM5 / RM10 / RM20 / RM50 / RM100)
- **Inventory management** — add, edit, restock items with category support
- **Sales reports** — daily reconciliation, top-selling items, monthly revenue charts
- **Receipt printing** — formatted for 80mm thermal printers
- **Keyboard shortcuts** — F2 checkout, F3 clear, F4 barcode mode, F5 manual mode
- **Payment methods** — Cash, Card/TnG, QR Pay (DuitNow)

---

## 🗂️ Project Structure

```
POS_System/
└── grocery-pos-web/
    ├── main.py           # Windows desktop app entry point (pywebview)
    ├── app.py            # Flask routes & API endpoints
    ├── database.py       # SQLite setup & migrations
    ├── models.py         # Item, Category, Sale models
    ├── requirements.txt  # Python dependencies
    ├── build.bat         # One-click Windows .exe builder
    └── templates/
        ├── pos.html      # POS terminal (main cashier screen)
        ├── inventory.html
        ├── reports.html
        └── index.html
```

> **Data** is saved to `~/Documents/NamChongPOS/grocery_store.db` when running as a `.exe` — it persists across app updates.

---

## 🖥️ Option A — Windows Desktop App (recommended)

No browser needed. Works like a normal Windows program.

### Step 1 — Install Python

Download and install Python 3.9+ from [python.org](https://www.python.org/downloads/).
Make sure to tick **"Add Python to PATH"** during installation.

### Step 2 — Build the .exe

```cmd
git clone https://github.com/kokyang/POS_System.git
cd POS_System\grocery-pos-web

REM Double-click build.bat, or run it in CMD:
build.bat
```

This will install all dependencies and produce:

```
dist\NamChongPOS\NamChongPOS.exe
```

### Step 3 — Run

Double-click `NamChongPOS.exe`. That's it — the app opens in its own window.

> To share with others, copy the entire `dist\NamChongPOS\` folder to their PC and run the `.exe` inside.

---

## 🌐 Option B — Web Browser (development / server mode)

```bash
# 1. Clone the repo
git clone https://github.com/kokyang/POS_System.git
cd POS_System/grocery-pos-web

# 2. Create a virtual environment
python3 -m venv venv
source venv/bin/activate        # macOS / Linux
# venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run
python app.py
```

Then open `http://localhost:8080` in your browser.

---

## 🖱️ How to Use

### Cashier (POS Terminal)

1. Open the app → click **POS Terminal**
2. **Barcode mode** (default):
   - Plug in a USB barcode scanner
   - Scan any item → name and price appear instantly
   - Adjust quantity with `−` / `+`, then press **ADD TO ORDER**
   - Or just type part of the item name to search
3. **Manual entry mode**:
   - Switch to the **Manual Entry** tab
   - Type the item name (optional)
   - Tap the price field → use the **numpad** to enter the price
   - Press **ADD TO ORDER**
4. Select payment method (Cash / Card / QR)
5. For cash — tap a quick-amount button or use the numpad; change is shown automatically
6. Press **CHECKOUT** → receipt preview appears → print or close

### Inventory Management

- Add items with name, category, price, stock quantity, and barcode
- Restock items directly from the inventory page
- Barcodes link physical scanner input to inventory records

### Reports

- Daily reconciliation
- Monthly revenue breakdown
- Top-selling items analysis

---

## ⌨️ Keyboard Shortcuts

| Key | Action |
|-----|--------|
| F2  | Checkout |
| F3  | Clear order |
| F4  | Switch to Barcode mode |
| F5  | Switch to Manual Entry mode |
| Esc | Close receipt |

---

## 🛠️ Tech Stack

| Layer          | Technology                            |
|----------------|---------------------------------------|
| Backend        | Python · Flask                        |
| Database       | SQLite (via Python `sqlite3`)         |
| Frontend       | Vanilla HTML / CSS / JS · Bootstrap Icons |
| Desktop window | pywebview (Edge WebView2 on Windows)  |
| Packaging      | PyInstaller                           |
| Printing       | Browser/system print (80mm ready)     |

---

## 📦 API Endpoints

| Method | Endpoint                      | Description                    |
|--------|-------------------------------|--------------------------------|
| GET    | `/api/items`                  | List all inventory items       |
| POST   | `/api/items`                  | Add new item                   |
| PUT    | `/api/items`                  | Update item                    |
| DELETE | `/api/items`                  | Delete item                    |
| GET    | `/api/lookup-barcode/<query>` | Lookup item by barcode or name |
| POST   | `/api/checkout`               | Record a sale                  |
| GET    | `/api/today-sales`            | Today's sales summary          |
| GET    | `/api/top-selling`            | Top selling items              |
| GET    | `/api/daily-reconciliation`   | Daily reconciliation report    |

---

## 📄 License

MIT License — free to use and modify.

---

*Built for NAM CHONG MINI MARKET 南昌小超市 🛒*
