# Staff Roles & Permissions Guide

## Overview

The IET Membership System now includes a comprehensive role-based permission system for staff members. Staff/Admin users bypass the application form and are directed to a dedicated staff dashboard.

---

## Staff Roles

### Available Roles:

1. **General Secretary**
   - Can manage certificates
   - Can post announcements
   - Full access to applications

2. **Treasurer**
   - Can confirm/reject payments
   - Can post announcements
   - Full access to applications

3. **Chairperson**
   - Can confirm payments
   - Can manage certificates
   - Can post announcements
   - Full administrative access

4. **Vice Chairperson**
   - Can post announcements
   - Full access to applications

5. **Coordinator** (Multiple allowed)
   - Can post announcements
   - Full access to applications

6. **Administrator**
   - Full system access
   - Can confirm payments
   - Can manage certificates
   - Can post announcements

---

## Permission Matrix

| Role | Confirm Payments | Manage Certificates | Post Announcements | View Applications |
|------|-----------------|--------------------|--------------------|-------------------|
| General Secretary | ❌ | ✅ | ✅ | ✅ |
| Treasurer | ✅ | ❌ | ✅ | ✅ |
| Chairperson | ✅ | ✅ | ✅ | ✅ |
| Vice Chairperson | ❌ | ❌ | ✅ | ✅ |
| Coordinator | ❌ | ❌ | ✅ | ✅ |
| Administrator | ✅ | ✅ | ✅ | ✅ |

---

## Staff Login Flow

### When Staff Logs In:

```
Staff Login → Staff Dashboard (NOT Application Form)
```

**Staff Dashboard Shows:**
- Total applications count
- Pending payments count
- Confirmed payments count
- Pending certificates count
- Quick action buttons (role-based)
- Pending payment confirmations (if authorized)
- Recent applications list

---

## How to Assign Staff Roles

### Via Django Admin Panel:

1. Go to Django Admin (`/admin`)
2. Navigate to **Users**
3. Select the user you want to make staff
4. Check **"Staff status"** checkbox
5. Select appropriate **"Staff role"** from dropdown
6. Save

### Programmatically:

```python
from accounts.models import User, StaffRole

# Make user a treasurer
user = User.objects.get(email='treasurer@example.com')
user.is_staff = True
user.staff_role = StaffRole.TREASURER
user.save()
```

---

## Permission Methods

### In Views:

```python
# Check specific role
if request.user.has_role(StaffRole.TREASURER):
    # Treasurer-specific logic
    pass

# Check payment confirmation permission
if request.user.can_confirm_payments():
    # Show payment confirmation options
    pass

# Check certificate management permission
if request.user.can_manage_certificates():
    # Show certificate management options
    pass

# Check announcement posting permission
if request.user.can_post_announcements():
    # Show announcement creation
    pass
```

### In Templates:

```django
{% if user.can_confirm_payments %}
    <a href="{% url 'payments:confirm' payment.pk %}">Confirm Payment</a>
{% endif %}

{% if user.can_manage_certificates %}
    <a href="{% url 'certificates:mark_ready' app.pk %}">Mark Certificate Ready</a>
{% endif %}
```

---

## Staff Dashboard Features

### Statistics Cards:
- **Total Applications** - All applications in system
- **Pending Payments** - Applications awaiting payment confirmation
- **Confirmed Payments** - Applications with confirmed payments
- **Pending Certificates** - Applications needing certificate processing

### Quick Actions (Role-Based):
- **All Applications** - View all applications (all staff)
- **Pending Payments** - View pending payments (Treasurer, Chairperson, Admin)
- **Manage Certificates** - Certificate management (General Secretary, Chairperson, Admin)
- **Announcements** - Post announcements (all staff)

### Pending Payment Confirmations:
- Only visible to users with payment confirmation permissions
- Shows table of all pending payments
- Quick access to view and confirm/reject

### Recent Applications:
- Shows 5 most recent applications
- Quick view button for each application

---

## URL Structure

### Staff URLs:
- `/applications/staff/dashboard/` - Staff Dashboard (NEW)
- `/applications/staff/` - All Applications List
- `/applications/staff/<id>/` - Application Detail
- `/payments/confirm/<id>/` - Confirm Payment
- `/payments/reject/<id>/` - Reject Payment
- `/certificates/mark_ready/<id>/` - Mark Certificate Ready

---

## Files Created/Modified

### New Files:
1. **`applications/staff_views.py`** - Staff dashboard view
2. **`templates/applications/staff_dashboard.html`** - Staff dashboard template
3. **`STAFF_ROLES_GUIDE.md`** - This documentation

### Modified Files:
1. **`accounts/models.py`** - Added StaffRole enum and staff_role field
2. **`accounts/views.py`** - Updated login redirect for staff
3. **`accounts/admin.py`** - Added staff_role to admin panel
4. **`applications/urls.py`** - Added staff dashboard URL
5. **`templates/base.html`** - Added Dashboard link for staff
6. **`iet_system/settings.py`** - Updated comments

### Migration:
- **`accounts/migrations/0003_user_staff_role.py`** - Added staff_role field

---

## Usage Examples

### Example 1: Assigning Treasurer Role

```python
# In Django shell or management command
from accounts.models import User, StaffRole

treasurer = User.objects.get(email='john@example.com')
treasurer.is_staff = True
treasurer.staff_role = StaffRole.TREASURER
treasurer.save()

print(f"Can confirm payments: {treasurer.can_confirm_payments()}")  # True
print(f"Can manage certificates: {treasurer.can_manage_certificates()}")  # False
```

### Example 2: Checking Permissions in View

```python
from django.contrib.auth.decorators import user_passes_test

@user_passes_test(lambda u: u.can_confirm_payments())
def confirm_payment_view(request, pk):
    # Only accessible by Treasurer, Chairperson, or Admin
    payment = get_object_or_404(Payment, pk=pk)
    # ... confirmation logic
```

### Example 3: Role-Based Template Display

```django
{% if user.staff_role == 'treasurer' %}
    <div class="alert alert-info">
        <strong>Treasurer Dashboard</strong>
        <p>You have {{ pending_payments }} payments to review.</p>
    </div>
{% endif %}
```

---

## Future Enhancements

### Planned Features:
1. **Activity Logs** - Track all staff actions
2. **Role Permissions Editor** - Admin UI to customize permissions
3. **Multiple Coordinators** - Support for multiple coordinator assignments
4. **Department-Based Permissions** - Coordinators assigned to specific departments
5. **Approval Workflows** - Multi-level approval for certain actions
6. **Email Notifications** - Notify staff of pending tasks

---

## Testing Checklist

### For Each Role:

#### General Secretary:
- [ ] Can access staff dashboard
- [ ] Can view all applications
- [ ] Can manage certificates
- [ ] Can post announcements
- [ ] Cannot confirm payments

#### Treasurer:
- [ ] Can access staff dashboard
- [ ] Can view pending payments section
- [ ] Can confirm payments
- [ ] Can reject payments
- [ ] Can post announcements
- [ ] Cannot manage certificates

#### Chairperson:
- [ ] Can access staff dashboard
- [ ] Can confirm payments
- [ ] Can manage certificates
- [ ] Can post announcements
- [ ] Full access to all features

#### Coordinator:
- [ ] Can access staff dashboard
- [ ] Can view all applications
- [ ] Can post announcements
- [ ] Cannot confirm payments
- [ ] Cannot manage certificates

---

## Security Notes

1. **Staff Status Required** - All role permissions require `is_staff=True`
2. **Role Verification** - Always verify role before granting access
3. **Audit Trail** - Consider implementing activity logging
4. **Regular Review** - Periodically review staff roles and permissions

---

## Support

For questions or issues with staff roles:
1. Check this documentation
2. Review the User model in `accounts/models.py`
3. Check permission methods: `can_confirm_payments()`, `can_manage_certificates()`, etc.
4. Contact system administrator

---

**All staff role features are now active and ready to use!** ✅






