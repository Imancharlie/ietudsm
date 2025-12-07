# Quick Start Guide

## Initial Setup (First Time)

1. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Create a superuser (admin account)**
   ```bash
   python manage.py createsuperuser
   ```
   Enter email, username, and password when prompted.

4. **Start the development server**
   ```bash
   python manage.py runserver
   ```

5. **Access the application**
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Configuration

### Update Settings

Edit `iet_system/settings.py`:

1. **Registration Fee**
   ```python
   REGISTRATION_FEE = 5000  # Change to your amount
   ```

2. **WhatsApp Group Link**
   ```python
   WHATSAPP_GROUP_LINK = "https://chat.whatsapp.com/your-actual-link"
   ```

3. **Secret Key** (IMPORTANT for production)
   ```python
   SECRET_KEY = 'your-secret-key-here'  # Generate a new one!
   ```

## User Flow Testing

### Test as Applicant

1. Go to http://127.0.0.1:8000/
2. Click "Apply for Membership"
3. Sign up with email and password
4. Fill out the application form
5. Note the payment reference number
6. Submit the application
7. Check application status

### Test as Staff

1. Login with your superuser account
2. Go to Applications
3. View an application
4. Confirm payment (if not confirmed)
5. Export form (requires template - see TEMPLATE_INSTRUCTIONS.md)
6. Update status to "Certificate Processing"
7. Mark certificate as ready

## Creating the Export Template

See `TEMPLATE_INSTRUCTIONS.md` for detailed instructions on creating the Word template for form exports.

## Common Commands

```bash
# Create new migrations after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver

# Access Django shell
python manage.py shell

# Collect static files (for production)
python manage.py collectstatic
```

## Troubleshooting

### Migration Issues
```bash
python manage.py makemigrations --name your_migration_name
python manage.py migrate
```

### Reset Database (Development Only!)
```bash
# Delete db.sqlite3
# Then run migrations again
python manage.py migrate
```

### Template Not Found
- Ensure template files are in the `templates/` directory
- Check `TEMPLATES` setting in `settings.py`

### Static Files Not Loading
- Run `python manage.py collectstatic`
- Check `STATIC_URL` and `STATIC_ROOT` in settings

## Next Steps

1. Customize the templates to match your branding
2. Create the Word export template
3. Set up email notifications (optional)
4. Configure for production deployment
5. Set up proper database (PostgreSQL recommended)

## Support

For issues, check:
- Django documentation: https://docs.djangoproject.com/
- Project README.md for detailed information




