import os
import django
from datetime import date, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'VendorBridge.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import UserProfile
from vendors.models import Vendor, VendorCategory
from rfq.models import RFQ, RFQItem
from quotations.models import Quotation
from approvals.models import Approval

print("Seeding dummy data...")

# 1. Create User
user, created = User.objects.get_or_create(username='admin')
if created:
    user.set_password('password123')
    user.email = 'admin@vendorbridge.com'
    user.is_superuser = True
    user.is_staff = True
    user.save()
    print("Superuser 'admin' created with password 'password123'")

profile, created = UserProfile.objects.get_or_create(
    user=user,
    defaults={
        'phone': '9876543210',
        'role': 'Admin',
        'country': 'India'
    }
)
if created:
    print("UserProfile created for admin")

# 2. Vendor Categories & Vendors
cat_it, _ = VendorCategory.objects.get_or_create(name='IT Equipment', defaults={'description': 'Hardware and software'})
cat_furn, _ = VendorCategory.objects.get_or_create(name='Office Furniture', defaults={'description': 'Desks, chairs, etc.'})

vendor_a, _ = Vendor.objects.get_or_create(
    email='info@apexcorp.com',
    defaults={
        'name': 'Apex Corp',
        'company_name': 'Apex Corporation Ltd',
        'phone': '1234567890',
        'category': cat_furn,
        'status': 'active',
        'gst_number': '29AAAAA1111A1Z1',
        'address_line1': '123 Corporate Way',
        'city': 'Mumbai',
        'state': 'Maharashtra',
        'pincode': '400001',
        'contact_person_name': 'Rajesh Sharma',
        'rating': 4.2,
        'created_by': user
    }
)

vendor_b, _ = Vendor.objects.get_or_create(
    email='sales@zenith.com',
    defaults={
        'name': 'Zenith Office Systems',
        'company_name': 'Zenith Ltd',
        'phone': '9876543210',
        'category': cat_furn,
        'status': 'active',
        'gst_number': '29BBBBB2222B2Z2',
        'address_line1': '456 Tech Park',
        'city': 'Bengaluru',
        'state': 'Karnataka',
        'pincode': '560001',
        'contact_person_name': 'Ananya Sen',
        'rating': 4.8,
        'created_by': user
    }
)

# 3. RFQs
rfq_1, _ = RFQ.objects.get_or_create(
    title='Office Furniture Q2',
    defaults={
        'description': 'Procurement of desks and ergonomic chairs for the new block.',
        'status': 'open',
        'deadline': date.today() + timedelta(days=15),
        'created_by': user
    }
)

RFQItem.objects.get_or_create(
    rfq=rfq_1,
    product_name='Ergonomic Chair',
    defaults={
        'quantity': 50.0,
        'unit': 'units',
        'description': 'High-back mesh ergonomic office chairs with lumbar support.'
    }
)

# 4. Quotations
Quotation.objects.get_or_create(
    quotation_number='QT-1001',
    defaults={
        'vendor_name': 'Apex Corp',
        'rfq_title': 'Office Furniture',
        'grand_total': 210000.00,
        'gst_percentage': 18.0,
        'delivery_days': 14,
        'vendor_rating': 4.2,
        'payment_terms': '45 Days',
        'status': 'submitted',
        'notes': 'Apex Corp quote with standard warranty of 2 years.'
    }
)

Quotation.objects.get_or_create(
    quotation_number='QT-1002',
    defaults={
        'vendor_name': 'Zenith Office Systems',
        'rfq_title': 'Office Furniture',
        'grand_total': 185000.00,
        'gst_percentage': 18.0,
        'delivery_days': 10,
        'vendor_rating': 4.8,
        'payment_terms': '30 Days',
        'status': 'submitted',
        'notes': 'Zenith quote with special discount. Delivery within 10 days.'
    }
)

Quotation.objects.get_or_create(
    quotation_number='QT-1003',
    defaults={
        'vendor_name': 'Global Office Hub',
        'rfq_title': 'Office Furniture',
        'grand_total': 195000.00,
        'gst_percentage': 18.0,
        'delivery_days': 12,
        'vendor_rating': 4.0,
        'payment_terms': '30 Days',
        'status': 'draft',
        'notes': 'Draft proposal. Final details to be confirmed.'
    }
)

# 5. Approvals
Approval.objects.get_or_create(
    rfq_title='Office Furniture Procurement Q2',
    level='Manager Review',
    defaults={
        'approver_name': 'Rajesh Kumar',
        'status': 'Approved',
        'remarks': 'Pricing seems competitive and vendor has good rating.'
    }
)

Approval.objects.get_or_create(
    rfq_title='IT Hardware Expansion Q3',
    level='Finance Approval',
    defaults={
        'approver_name': 'Anil Mehta',
        'status': 'Pending',
        'remarks': ''
    }
)

print("Dummy data seeding complete!")
