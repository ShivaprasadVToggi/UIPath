# FAQ Management System Using UiPath Automation and Chatbot

A complete college FAQ management system with three integrated components:

1. **Excel & CSV Data** — `CollegeFAQ.xlsx` and `faq_data.csv` with 14 realistic FAQs across `VisitorFAQ` and `StudentFAQ` categories.
2. **Django Web Application** (`CollegeFAQ/`) — Browse, search, and manage FAQs through a clean web UI; keyword-based chatbot; Django Admin for full CRUD; one-command Excel/CSV import/sync.
3. **UiPath Automation** (`CollegeFAQAutomation/`) — Reads the Excel FAQ sheet, prompts for a keyword via Input Dialog, and displays the matching answer (or a "not found" message).

---

## Repository Structure

```
.
├── data/
│   ├── CollegeFAQ.xlsx          # Excel workbook (Sheet1: ID, Category, Question, Answer)
│   └── faq_data.csv             # Matching CSV with identical rows
├── CollegeFAQ/                  # Django web application
│   ├── manage.py
│   ├── requirements.txt
│   ├── db.sqlite3               # Pre-loaded with FAQs + superuser
│   ├── CollegeFAQ/              # Project settings / URLs
│   └── faq/                     # App: models, views, admin, forms, import command, templates
├── CollegeFAQAutomation/        # UiPath Studio project
│   ├── project.json
│   ├── Main.xaml                # Full automation workflow
│   ├── CollegeFAQ.xlsx          # Copy of data file for the robot
│   └── faq_data.csv             # Copy of CSV for Read CSV demo
└── README.md
```

---

## Part 1 — Excel & CSV Data

- **`CollegeFAQ.xlsx`** — Sheet `Sheet1`, columns: `ID | Category | Question | Answer`.
- **`faq_data.csv`** — Identical 14 rows, UTF-8, comma-separated.

Categories: `VisitorFAQ` (6 entries) and `StudentFAQ` (8 entries). Includes all required questions:
- Where is the college located?
- How can I arrange a meeting with college staff?
- Where can I enquire about hostel facilities?
- What documents are required for admission?
- How can I contact the admission office?
- What are the college office timings?

---

## Part 2 — Django Web Application (CollegeFAQ)

### Setup & Run

```bash
cd CollegeFAQ
pip install -r requirements.txt
python manage.py migrate                  # (db.sqlite3 is already included; this is idempotent)
python manage.py runserver                # starts at http://127.0.0.1:8000/
```

### Admin Login

- **URL:** http://127.0.0.1:8000/admin/
- **Username:** `admin`
- **Password:** `Admin@123`

From Django Admin you can add / change / delete **Groups**, **Users**, and **FAQs**.

### Import / Sync from Excel or CSV

A custom management command pre-loads or syncs the database from the data files:

```bash
# Import (skips duplicates by question text)
python manage.py import_faqs --excel ../data/CollegeFAQ.xlsx

# Import from CSV
python manage.py import_faqs --csv ../data/faq_data.csv

# Full sync (clears all FAQs first, then re-imports)
python manage.py import_faqs --excel ../data/CollegeFAQ.xlsx --sync
```

The database (`db.sqlite3`) is shipped pre-loaded with all 14 FAQs.

### Web Pages

| Page | URL | Features |
|------|-----|----------|
| Home | `/` | Navbar (CollegeFAQ / Home / Manage FAQs / Chatbot / Admin), blue hero banner **"YOUR QUESTIONS, ANSWERED — How can we help you?"**, search box, category dropdown (All FAQs / VisitorFAQ / StudentFAQ), Search & Clear buttons, FAQ list with **View Answer** modal and **Manage FAQs** link. |
| Manage FAQs | `/manage/` | Add a New FAQ form (Question / Answer / Category / Add FAQ button) with empty-field validation; Delete button per FAQ with confirmation. |
| Chatbot | `/chatbot/` | Question input + Ask Question button; case-insensitive keyword matching against FAQ records; matching answer shown in chat area; clear **"answer unavailable"** fallback message. |
| Admin | `/admin/` | Full CRUD for Groups, Users, FAQs. |

---

## Part 3 — UiPath Automation (CollegeFAQAutomation)

### Project Contents

- `project.json` — UiPath project manifest (dependencies: Excel, System, UI Automation, Mail).
- `Main.xaml` — Complete workflow.
- `CollegeFAQ.xlsx`, `faq_data.csv` — Data files used by the robot.

### Workflow (Main.xaml)

**Variables (Main scope):**

| Variable | Type | Default |
|----------|------|---------|
| `answerFound` | Boolean | `False` |
| `dtFAQ` | DataTable | — |
| `searchKeyword` | String | — |

**Sequence:**

1. **Excel Application Scope** on `CollegeFAQ.xlsx` → **Read Range** (Sheet `Sheet1`, Has headers = True) → output `dtFAQ`.
2. **Write Line** — displays `dtFAQ.Rows.Count.ToString` (row count).
3. **Read CSV** (`faq_data.csv`) → **Assign** `csvDemoOutput = String.Join(" | ", ...questions...)` → **Write Line** demo output.
4. **Input Dialog** — Title `College Enquiry System`, Label `Enter keyword, question, VisitorFAQ or StudentFAQ` → output `searchKeyword`.
5. **Assign** — `answerFound = False`.
6. **For Each Row in Data Table** (`dtFAQ`, item name `CurrentRow`):
   - **If** `searchKeyword.Trim.ToLower` matches `CurrentRow("Question")` or `CurrentRow("Category")` (case-insensitive, contains + exact):
     - **Then:** **Message Box** showing `CurrentRow("Answer").ToString` → **Assign** `answerFound = True`.
7. **If `Not answerFound`** → **Message Box** — `"No matching answer found / Invalid Category"`.

### How to Run & Verify in UiPath Studio

> UiPath Studio requires Windows. If you are on macOS/Linux, use a Windows VM or UiPath Cloud (Automation Cloud) — sign in at **https://cloud.uipath.com/**.

1. Install **UiPath Studio** (Community Edition is free) from https://www.uipath.com/developers/studio.
2. Sign in / activate with your UiPath account (Cloud login: https://cloud.uipath.com/).
3. **Open Project** → select the `CollegeFAQAutomation` folder (it auto-detects `project.json`).
4. Wait for NuGet dependencies (`UiPath.Excel.Activities`, `UiPath.System.Activities`, etc.) to restore.
5. Open `Main.xaml` in the Designer. Confirm no validation errors (red exclamation marks).
6. Click **Debug** (or **Run** / F5).
7. Verify in the **Output panel**: you should see the row-count Write Line and the CSV String.Join demo line.
8. When the **Input Dialog** appears, type `college located` (or `VisitorFAQ`, or `hostel`) → the matching answer appears in a Message Box.
9. Run again and type `xyzzy123` → you should see **"No matching answer found / Invalid Category"**.
10. Confirm variables exist in Main scope with the correct types (Variables panel).

### Opening CollegeFAQAutomation in UiPath Studio on Windows (from GitHub)

**Method 1 — Clone Repository inside UiPath Studio (recommended):**

1. Install **UiPath Studio** (Community Edition, free) from https://www.uipath.com/developers/studio.
2. Launch Studio. On the start screen, sign in with your UiPath account (same as https://cloud.uipath.com/ — use Google / Microsoft / email SSO).
3. On the Studio start screen, go to **Team** (left sidebar) → **Git** → **Clone Repository**.
4. Paste the repository URL: `https://github.com/ShivaprasadVToggi/UIPath.git`
5. Choose a local folder (e.g. `C:\Users\You\Documents\UiPath\UIPath`). If prompted for credentials, enter your GitHub username and a **Personal Access Token** (Settings → Developer settings → Personal access tokens → Tokens (classic), scope `repo`) as the password.
6. Studio clones the repo and detects `CollegeFAQAutomation/project.json`. Click **Open Project**.
7. Wait for NuGet packages to restore (UiPath.Excel.Activities, UiPath.System.Activities, UiPath.UIAutomation.Activities). The Output panel shows "Packages restored".
8. Open `Main.xaml` from the Project panel. Confirm no red validation errors.
9. Press **F5** (Debug) to run. The Input Dialog appears — type `college located` or `VisitorFAQ` → answer shows in a Message Box.

**Method 2 — Open project.json directly:**

1. `git clone https://github.com/ShivaprasadVToggi/UIPath.git` (or download ZIP from GitHub).
2. In UiPath Studio: **Open** → browse to `UIPath/CollegeFAQAutomation/project.json` → Open.
3. Studio loads the project; restore packages if prompted.

**Signing into UiPath Automation Cloud (cloud.uipath.com):**

- Cloud portal: https://cloud.uipath.com/ — sign in with the same account used in Studio.
- Once signed in, you can access **Orchestrator** (tenant → Orchestrator) to publish & run robots, and **Studio Web** (browser-based Studio) to edit workflows from any machine.
- To publish this project to Orchestrator: in Studio → **Publish** → choose your Orchestrator tenant as the publish target. The process then appears under Orchestrator → Processes.

### If activities show as "unknown"

The project targets the modern **Windows** framework (.NET 6/8 runtime) compatible with UiPath Studio 24.10 / 26.10+. If any activity is unrecognized, install the missing package via **Manage Packages** (UiPath.Excel.Activities and UiPath.System.Activities are the primary required packages).

---

## Quick Verification Checklist

- [ ] `python manage.py runserver` starts with no errors.
- [ ] Home page loads, hero banner visible, FAQs listed, View Answer modal opens.
- [ ] Search box filters FAQs; Clear button resets.
- [ ] Category dropdown filters by VisitorFAQ / StudentFAQ.
- [ ] Manage page: add FAQ with empty fields shows validation error; valid FAQ appears in list; delete works.
- [ ] Chatbot: known keyword returns an answer; unknown keyword shows "answer unavailable".
- [ ] Admin login at `/admin/` with `admin / Admin@123`; Groups, Users, FAQs all manageable.
- [ ] `python manage.py import_faqs --excel ../data/CollegeFAQ.xlsx --sync` re-imports cleanly.
- [ ] UiPath `Main.xaml` opens in Studio; Debug runs; Input Dialog → Message Box flow works.

---

## Tech Stack

- **Backend:** Python 3.10+, Django 4.2+ (SQLite)
- **Frontend:** Bootstrap 5 (CDN), vanilla JS
- **Automation:** UiPath Studio (Windows Workflow Foundation XAML)
- **Data:** Excel (.xlsx via openpyxl), CSV
