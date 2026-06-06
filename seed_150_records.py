import os
import django
import random
from datetime import date, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'VendorBridge.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import UserProfile
from vendors.models import Vendor, VendorCategory
from rfq.models import RFQ, RFQItem
from quotations.models import Quotation
from approvals.models import Approval
from procurement.models import PurchaseOrder, Invoice

print("Initializing 150-record database seeding (including POs and Invoices)...")

# 1. Create default admin user if not exists
user, created = User.objects.get_or_create(username='admin')
if created:
    user.set_password('password123')
    user.email = 'admin@vendorbridge.com'
    user.is_superuser = True
    user.is_staff = True
    user.save()
    print("Admin user created.")

UserProfile.objects.get_or_create(
    user=user,
    defaults={
        'phone': '9876543210',
        'role': 'Admin',
        'country': 'India'
    }
)

# 2. Categories
categories_data = [
    ('Office Furniture', 'Desks, chairs, conference tables, cabinets'),
    ('IT Equipment', 'Laptops, servers, networking devices, monitors'),
    ('Office Supplies', 'Paper, pens, staplers, printing ink, folders'),
    ('Logistics & Shipping', 'Courier services, freight handling, warehousing'),
    ('Marketing & Print', 'Brochures, banner printing, advertising materials'),
]

categories = []
for name, desc in categories_data:
    cat, _ = VendorCategory.objects.get_or_create(name=name, defaults={'description': desc})
    categories.append(cat)

# Lists for random selections
vendor_names_pool = [
    "Apex Systems", "Zenith Furnishings", "Vertex IT Solutions", "Pro Logistics",
    "Nova Media", "Omni Office Supplies", "Summit Corp", "Quantum Software",
    "Global Logistics", "Matrix Furnitures", "Elite Printing", "Alpha Tech",
    "Prime Distributors", "Infinity Supplies", "Ecolab Materials", "Delta Electronics",
    "Pinnacle Solutions", "Core Hardware", "Intellect Services", "Dynamic Logistics",
    "Empire Office Hub", "Sigma Consultants", "Titan Industrial", "Spectrum Med",
    "Pacific Trade", "Starlight Media", "Vanguard Systems", "Pioneer Kraft",
    "TrueSource Supplies", "Anchor Shipping"
]

cities_pool = [
    ("Mumbai", "Maharashtra", "400001"),
    ("Bengaluru", "Karnataka", "560001"),
    ("New Delhi", "Delhi", "110001"),
    ("Pune", "Maharashtra", "411001"),
    ("Hyderabad", "Telangana", "500001"),
    ("Chennai", "Tamil Nadu", "600001"),
]

rfq_titles_pool = [
    "Ergonomic Desks Procurement", "Developer Laptops Purchase", "Cloud Server Hosting Q3",
    "Annual Stationery Supply", "Promotional Banner Print", "High-Back Office Chairs",
    "Wi-Fi Router Deployment", "Conference Room Projectors", "Courier Services Contract",
    "Brochure Printing Batch A", "Meeting Cabin Tables", "Staff Keyboard & Mouse",
    "Security Firewall Hardware", "Warehouse Pallets Order", "Office Branding Decals",
    "Executive Chair Selection", "SSD Upgrade Drive Pack", "UPS Battery Backup Supply",
    "Visitor Lounge Sofas", "Network Switch 24-Port", "General Cleaning Supplies",
    "Bulk Printing Paper Reams", "Exhibition Stall Print", "Fiber Optic Installation",
    "Customer Support Headsets", "Desktop Monitor Upgrade", "Direct Mail Envelopes",
    "Breakroom Coffee Machine", "Cafeteria Dining Chairs", "Air Purifiers Procurement"
]

approvers_pool = [
    "Rajesh Kumar", "Anil Mehta", "Sanjay Gupta", "Priya Patel",
    "Vikram Malhotra", "Neha Sen", "Ramesh Joshi", "Deepak Verma"
]

# 3. Create 30 Vendors
print("Creating 30 Vendors...")
vendors = []
for i in range(30):
    name = vendor_names_pool[i]
    email = f"sales@{name.lower().replace(' ', '')}.com"
    city, state, pincode = random.choice(cities_pool)
    cat = random.choice(categories)
    
    vendor, _ = Vendor.objects.get_or_create(
        email=email,
        defaults={
            'name': name,
            'company_name': f"{name} Private Limited",
            'phone': str(random.randint(6000000000, 9999999999)),
            'category': cat,
            'status': random.choice(['active', 'active', 'active', 'inactive', 'pending']),
            'gst_number': f"29{random.choice('ABCDE')*5}{random.randint(1000, 9999)}{random.choice('ABCDE')}1Z{random.randint(1,9)}",
            'address_line1': f"Plot #{random.randint(10, 500)}, Industrial Area",
            'city': city,
            'state': state,
            'pincode': pincode,
            'contact_person_name': f"Manager {name.split()[0]}",
            'rating': round(random.uniform(3.2, 4.9), 1),
            'created_by': user
        }
    )
    vendors.append(vendor)

# 4. Create 30 RFQs and RFQItems
print("Creating 30 RFQs...")
rfqs = []
for i in range(30):
    title = rfq_titles_pool[i]
    status = random.choice(['draft', 'open', 'open', 'closed', 'awarded'])
    
    rfq, _ = RFQ.objects.get_or_create(
        title=title,
        defaults={
            'description': f"Requirement details for procurement of {title} to support the regional office expansion.",
            'status': status,
            'deadline': date.today() + timedelta(days=random.randint(5, 45)),
            'created_by': user
        }
    )
    rfqs.append(rfq)
    
    # Create 1 associated item per RFQ
    RFQItem.objects.get_or_create(
        rfq=rfq,
        product_name=f"Standard {title.split()[0]} item",
        defaults={
            'quantity': random.choice([10, 25, 50, 100, 250]),
            'unit': 'units',
            'description': f"Technical specifications matching standard {title} requirements."
        }
    )

# 5. Create 50 Quotations
print("Creating 50 Quotations...")
quotations_created = 0
for i in range(50):
    q_num = f"QT-{1000 + i}"
    vendor = random.choice(vendors)
    rfq = random.choice(rfqs)
    
    # Extract clean category title
    rfq_title_clean = "Office Furniture"
    if "Laptop" in rfq.title or "Server" in rfq.title or "Router" in rfq.title or "Switch" in rfq.title or "Monitor" in rfq.title or "SSD" in rfq.title or "UPS" in rfq.title or "Headset" in rfq.title:
        rfq_title_clean = "IT Equipment"
    elif "Paper" in rfq.title or "Stationery" in rfq.title or "Cleaning" in rfq.title or "Envelope" in rfq.title or "Coffee" in rfq.title:
        rfq_title_clean = "Office Supplies"
    elif "Logistics" in rfq.title or "Courier" in rfq.title or "Warehouse" in rfq.title:
        rfq_title_clean = "Logistics & Shipping"
    elif "Print" in rfq.title or "Banner" in rfq.title or "Brochure" in rfq.title or "Branding" in rfq.title or "Exhibition" in rfq.title:
        rfq_title_clean = "Marketing & Print"

    grand_total = round(random.uniform(12000, 380000), 2)
    gst_percent = random.choice([5, 12, 18, 18, 18])
    
    _, created = Quotation.objects.get_or_create(
        quotation_number=q_num,
        defaults={
            'vendor_name': vendor.name,
            'rfq_title': rfq_title_clean,
            'grand_total': grand_total,
            'gst_percentage': gst_percent,
            'delivery_days': random.randint(3, 20),
            'vendor_rating': vendor.rating,
            'payment_terms': random.choice(['30 Days', '45 Days', '60 Days', 'Immediate']),
            'status': random.choice(['draft', 'submitted', 'submitted', 'submitted', 'approved', 'rejected']),
            'notes': f"Official response quotation from {vendor.name} matching technical compliance constraints."
        }
    )
    if created:
        quotations_created += 1

# 6. Create 40 Approvals
print("Creating 40 Approvals...")
approvals_created = 0
for i in range(40):
    rfq = random.choice(rfqs)
    level = random.choice(['Manager Review', 'Finance Approval', 'Director Sign-off'])
    approver = random.choice(approvers_pool)
    status = random.choice(['Pending', 'Approved', 'Approved', 'Rejected'])
    
    remarks = ""
    if status == 'Approved':
        remarks = random.choice(["Prices verified, fits within budget.", "Approved based on vendor rating.", "Technically compliant and lowest quote."])
    elif status == 'Rejected':
        remarks = random.choice(["Exceeds budget cap.", "Delivery timeline too long.", "Payment terms unacceptable."])
        
    _, created = Approval.objects.get_or_create(
        rfq_title=f"{rfq.title} Procurement",
        level=level,
        approver_name=approver,
        defaults={
            'status': status,
            'remarks': remarks
        }
    )
    if created:
        approvals_created += 1

# 7. Create Purchase Orders
print("Creating 15 Purchase Orders...")
pos_created = 0
quotations_list = list(Quotation.objects.all())
vendors_list = list(Vendor.objects.all())

if quotations_list and vendors_list:
    for i in range(15):
        po_num = f"PO-{1000 + i}"
        quotation = random.choice(quotations_list)
        vendor = random.choice(vendors_list)
        po, created = PurchaseOrder.objects.get_or_create(
            po_number=po_num,
            defaults={
                'vendor': vendor,
                'quotation': quotation,
                'amount': quotation.grand_total,
                'status': random.choice(['Pending', 'Approved', 'Shipped', 'Delivered'])
            }
        )
        if created:
            pos_created += 1

# 8. Create Invoices
print("Creating 10 Invoices...")
invoices_created = 0
pos_list = list(PurchaseOrder.objects.all())
if pos_list:
    for i in range(10):
        inv_num = f"INV-{1000 + i}"
        po = random.choice(pos_list)
        invoice, created = Invoice.objects.get_or_create(
            invoice_number=inv_num,
            defaults={
                'purchase_order': po,
                'total_amount': po.amount,
                'due_date': date.today() + timedelta(days=random.randint(10, 30)),
                'status': random.choice(['Unpaid', 'Paid', 'Overdue'])
            }
        )
        if created:
            invoices_created += 1

print(f"Database successfully populated!")
print(f"Total Created: 30 Vendors, 30 RFQs, {quotations_created} Quotations, {approvals_created} Approvals, {pos_created} POs, {invoices_created} Invoices.")
