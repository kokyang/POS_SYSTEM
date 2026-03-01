# 🛒 NAM CHONG MINI MARKET — POS System

A lightweight, web-based **Point of Sale (POS)** system built for small grocery stores. Runs entirely in the browser — no installation needed on the cashier's side.

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.1-black?logo=flask)
![SQLite](https://img.shields.io/badge/Database-SQLite-blue?logo=sqlite)
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

- **Split-screen POS layout** — order list on the left, controls on the right
- **Barcode scanner support** — plug in any USB barcode scanner; items are looked up automatically
- **Manual entry mode** — type item name + enter price via on-screen numpad
- **On-screen numpad** — large touch-friendly buttons for price and payment input
- **Real-time change calculator** — shows 找零 (change) instantly with quick-cash buttons (RM5 / RM10 / RM20 / RM50 / RM100)
- **Inventory management** — add, edit, restock items with category support
- **Sales reports** — daily reconciliation, top-selling items, monthly revenue charts
- **Receipt printing** — browser print dialog formatted for 80mm thermal printers
- **Keyboard shortcuts** — F2 checkout, F3 clear, F4 barcode mode, F5 manual mode
- **Payment methods** — Cash, Card/TnG, QR Pay (DuitNow)

---

## 🗂️ Project Structure

```
POS_System/
└── grocery-pos-web/
    ├── app.py            # Flask routes & API endpoints
    ├── database.py       # SQLite setup & migrations
    ├── models.py         # Item, Category, Sale models
    ├── templates/
    │   ├── pos.html      # POS terminal (main cashier screen)
    │   ├── inventory.html
    │   ├── reports.html
    │   └── index.html
    └── grocery_store.db  # SQLite database (auto-created)
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- pip

### Installation

```bash
# 1. Clone the repo
git clone https://github.com/kokyang/POS_System.git
cd POS_System/grocery-pos-web

# 2. Create a virtual environment
python3 -m venv venv
source venv/bin/activate        # macOS / Linux
# venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install flask

# 4. Run the app
python app.py
```

### Open in browser

```
http://localhost:8080
```

The database (`grocery_store.db`) is created automatically on first run.

---

## 🖥️ How to Use

### Cashier (POS Terminal)

1. Go to **POS Terminal** from the main menu
2. **Barcode mode** (default):
   - Plug in a USB barcode scanner — it acts as a keyboard
   - Scan any item; the name and price appear instantly
   - Adjust quantity with `−` / `+`, then press **ADD TO ORDER**
   - Or type part of the item name to search
3. **Manual entry mode**:
   - Switch to **Manual Entry** tab
   - Type the item name (optional)
   - Tap the price field, use the **numpad** to enter the price
   - Press **ADD TO ORDER**
4. Select payment method (Cash / Card / QR)
5. For cash — tap the customer's amount or use quick buttons; change is shown automatically
6. Press **CHECKOUT** → receipt preview appears → print or close

### Inventory Management

- Add new items with name, category, price, stock, and barcode
- Restock items directly from the inventory page

### Reports

- Daily reconciliation
- Monthly revenue
- Top-selling items

---

## ⌨️ Keyboard Shortcuts

| Key | Action            |
|-----|-------------------|
| F2  | Checkout          |
| F3  | Clear order       |
| F4  | Switch to Barcode mode |
| F5  | Switch to Manual mode  |
| Esc | Close receipt     |

---

## 🛠️ Tech Stack

| Layer    | Technology                        |
|----------|-----------------------------------|
| Backend  | Python · Flask                    |
| Database | SQLite (via Python `sqlite3`)     |
| Frontend | Vanilla HTML/CSS/JS · Bootstrap Icons |
| Printing | Browser native print (80mm ready) |

---

## 📦 API Endpoints

| Method | Endpoint                        | Description                  |
|--------|---------------------------------|------------------------------|
| GET    | `/api/items`                    | List all inventory items     |
| POST   | `/api/items`                    | Add new item                 |
| PUT    | `/api/items`                    | Update item                  |
| DELETE | `/api/items`                    | Delete item                  |
| GET    | `/api/lookup-barcode/<query>`   | Lookup item by barcode or name |
| POST   | `/api/checkout`                 | Record a sale                |
| GET    | `/api/today-sales`              | Today's sales summary        |
| GET    | `/api/top-selling`              | Top selling items            |

---

## 📄 License

MIT License — free to use and modify.

---

*Built for NAM CHONG MINI MARKET 南昌小超市 🛒*
