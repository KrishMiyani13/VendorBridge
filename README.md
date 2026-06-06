# 🚀 VendorBridge ERP
> A Modern, Premium Procurement & Supplier Relationship Management (SRM) Suite.

VendorBridge is a comprehensive, high-aesthetic enterprise resource planning (ERP) platform built with **Django 6** and **Bootstrap 5**. It is designed to streamline the procurement lifecycle—from vendor onboarding and Request for Quotations (RFQs) to quotation comparisons, approvals, purchase orders, invoices, and dynamic analytics.

---

## 🌟 Key Features

### 1. 📊 Centralized Dashboard & Analytics
- **Dynamic KPI Cards**: Tracks real-time metrics for Vendors, RFQs, Purchase Orders, Invoices, Quotations, and Approvals.
- **Interactive Quick Actions**: One-click navigation to submit quotes, review approvals, or generate invoices.
- **Live Chart.js Visuals**: Dynamic charts under `/analytics/` displaying the status distribution of key procurement assets.

### 2. 👥 Vendor Onboarding & Management
- Structured database profiles for supplier networks.
- Automatic star-based rating aggregation.
- Categorized search and filters (IT Equipment, Office Furniture, etc.).

### 3. 📝 Request for Quotations (RFQ) & Bidding
- Create, manage, and assign RFQs to specific vendors.
- Set bidding deadlines and input detailed product requirements.

### 4. 📄 Quotations Workflow
- **Interactive Submissions**: Dynamic rows addition/deletion, real-time GST tax calculations, and subtotal/grand total computations.
- **Save Drafts**: Save progress locally as a draft before final submission.
- **Comparison Matrix**: Side-by-side criteria evaluation (totals, GST, rating, delivery days, payment terms) to identify the best bids.

### 5. 🛡️ Multi-Stage Approval Workflow
- Linear process timeline visualization: `Submitted ➔ Manager Review ➔ Finance Approval ➔ Generate PO`.
- Role-based validation checks.
- Interactive **Approve** and **Reject** review actions with loggable approver remarks.

### 6. 🛒 Procurement & Invoicing
- Generate official **Purchase Orders (POs)** against selected vendor bids.
- Generate **Supplier Invoices** linked directly to active POs.
- **PDF Invoice Download**: Automatically renders and compiles clean, printable PDF documents using `xhtml2pdf`.

### 7. 🔐 Interactive Registration Wizard
- Sleek 3-step registration wizard (`Personal details ➔ Security ➔ Profile Avatar`) reducing layout clutter.
- Live client-side validations for email formats, username lengths, and 10-digit phone inputs.
- Dynamic password strength meter with animated feedback.
- Drag-and-drop/click profile picture upload preview.

---

## 🛠️ Technology Stack
- **Backend**: Python 3.14+, Django 6.0.6
- **Database**: SQLite3
- **Frontend**: HTML5, Vanilla CSS, Bootstrap 5, FontAwesome, Chart.js, Google Fonts (Inter)
- **Libraries**: `xhtml2pdf` (Invoice PDF conversion)

---

## ⚙️ Installation & Setup

Follow these steps to set up VendorBridge locally:

### 1. Clone the Repository
```bash
git clone https://github.com/KrishMiyani13/VendorBridge.git
cd VendorBridge
```

### 2. Install Dependencies
Make sure you have python and pip installed:
```bash
pip install -r requirements.txt
```

### 3. Apply Database Migrations
Create the SQLite database and sync all model schemas:
```bash
python manage.py migrate
```

### 4. Seed Database (150+ Records)
Populate the database with a pre-configured suite of categories, vendors, RFQs, quotations, approvals, purchase orders, invoices, and a default admin user:
```bash
python seed_150_records.py
```

### 5. Run the Server
```bash
python manage.py runserver
```
Navigate to **http://127.0.0.1:8000/** in your browser.

---

## 🔑 Default Credentials

After running the database seeding script (`seed_150_records.py`), you can immediately log in using:
- **Username**: `admin`
- **Password**: `password123`

---

## 📁 Project Architecture
```text
VendorBridge/
│
├── accounts/          # Authentication, Profile models, and Wizard signup views
├── approvals/         # Multi-level workflow approvals, timeline status template
├── procurement/       # Purchase Orders, Invoices, and PDF compilation views
├── quotations/        # Pricing bids submissions, drafts, and comparison matrix
├── rfq/               # Procurement requirements and bidding windows
├── vendors/           # Supplier records, categorizations, and ratings
├── analytics_app/     # Dynamic Chart.js distribution charts
│
├── static/            # Consolidated custom CSS (style.css) and JS scripts
├── templates/         # Master template layout files (base.html)
└── manage.py          # Django management entrypoint
```
