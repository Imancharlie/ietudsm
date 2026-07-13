# IET UDSM Membership System - Deployment Guide

## Prerequisites
- Ubuntu VPS (20.04 LTS or later recommended)
- Python 3.8+
- PostgreSQL (recommended for production) or SQLite
- Nginx
- Domain name with SSL certificate

## Step 1: Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3-pip python3-venv postgresql postgresql-contrib nginx -y

# Create project directory
sudo mkdir -p /var/www/ietudsm
sudo chown $USER:$USER /var/www/ietudsm
cd /var/www/ietudsm
```

## Step 2: Application Setup

```bash
# Clone or upload your project
# git clone <your-repo> .

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env
nano .env  # Edit with your production settings
```

## Step 3: Environment Configuration

Edit `.env` file with production settings:

```env
DEBUG=False
SECRET_KEY=your-very-secure-random-secret-key-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Database (PostgreSQL recommended)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=ietudsm
DB_USER=ietudsm
DB_PASSWORD=your-secure-db-password
DB_HOST=localhost
DB_PORT=5432
```

## Step 4: Database Setup (PostgreSQL)

```bash
# Create database and user
sudo -u postgres psql

CREATE DATABASE ietudsm;
CREATE USER ietudsm WITH PASSWORD 'your-secure-db-password';
ALTER ROLE ietudsm SET client_encoding TO 'utf8';
ALTER ROLE ietudsm SET default_transaction_isolation TO 'read committed';
ALTER ROLE ietudsm SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE ietudsm TO ietudsm;
\q
```

Update `settings.py` to use PostgreSQL:

```python
DATABASES = {
    'default': {
        'ENGINE': env('DB_ENGINE', default='django.db.backends.sqlite3'),
        'NAME': env('DB_NAME', default=BASE_DIR / 'db.sqlite3'),
        'USER': env('DB_USER', default=''),
        'PASSWORD': env('DB_PASSWORD', default=''),
        'HOST': env('DB_HOST', default='localhost'),
        'PORT': env('DB_PORT', default='5432'),
    }
}
```

## Step 5: Django Setup

```bash
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput

# Create necessary directories
mkdir -p logs media tmp_exports
```

## Step 6: Gunicorn Setup

```bash
# Install Gunicorn
pip install gunicorn

# Test Gunicorn
gunicorn --bind 0.0.0.0:8000 iet_system.wsgi:application
```

Create Gunicorn systemd service:

```bash
sudo nano /etc/systemd/system/ietudsm.service
```

Add this content:

```ini
[Unit]
Description=gunicorn daemon for ietudsm
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/ietudsm
ExecStart=/var/www/ietudsm/venv/bin/gunicorn \
          --access-logfile - \
          --error-logfile - \
          --workers 3 \
          --bind unix:/var/www/ietudsm/ietudsm.sock \
          iet_system.wsgi:application

[Install]
WantedBy=multi-user.target
```

Start and enable the service:

```bash
sudo systemctl start ietudsm
sudo systemctl enable ietudsm
sudo systemctl status ietudsm
```

## Step 7: Nginx Configuration

```bash
sudo nano /etc/nginx/sites-available/ietudsm
```

Add this configuration:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/ietudsm/ietudsm.sock;
    }

    location /static/ {
        alias /var/www/ietudsm/staticfiles/;
    }

    location /media/ {
        alias /var/www/ietudsm/media/;
    }
}
```

Enable the site:

```bash
sudo ln -s /etc/nginx/sites-available/ietudsm /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

## Step 8: SSL Certificate (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

## Step 9: Security Hardening

```bash
# Set proper permissions
sudo chown -R www-data:www-data /var/www/ietudsm
sudo chmod -R 755 /var/www/ietudsm
sudo chmod 600 /var/www/ietudsm/.env

# Configure firewall
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

## Step 10: Backup Setup

Create backup script:

```bash
sudo nano /usr/local/bin/ietudsm-backup.sh
```

```bash
#!/bin/bash
BACKUP_DIR="/var/backups/ietudsm"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR

# Backup database
pg_dump -U ietudsm ietudsm > $BACKUP_DIR/db_backup_$DATE.sql

# Backup media files
tar -czf $BACKUP_DIR/media_backup_$DATE.tar.gz /var/www/ietudsm/media

# Keep only last 7 days of backups
find $BACKUP_DIR -type f -mtime +7 -delete
```

Make it executable and add to cron:

```bash
sudo chmod +x /usr/local/bin/ietudsm-backup.sh
sudo crontab -e
```

Add this line for daily backup at 2 AM:

```
0 2 * * * /usr/local/bin/ietudsm-backup.sh
```

## Step 11: Monitoring

Install monitoring tools:

```bash
sudo apt install htop -y
```

Check logs:

```bash
sudo tail -f /var/www/ietudsm/logs/django.log
sudo journalctl -u ietudsm -f
sudo tail -f /var/log/nginx/error.log
```

## Database Backup via Admin Panel

Staff users can download database backups via:
- URL: `/admin/backup-db/`
- Requires: Staff privileges
- Downloads: SQLite database with timestamp

## Maintenance Commands

```bash
# Update code
cd /var/www/ietudsm
git pull
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart ietudsm

# Check logs
sudo tail -f /var/www/ietudsm/logs/django.log

# Restart services
sudo systemctl restart ietudsm
sudo systemctl restart nginx
```

## Troubleshooting

### Application not loading
```bash
sudo systemctl status ietudsm
sudo journalctl -u ietudsm -n 50
```

### Static files not serving
```bash
sudo chown -R www-data:www-data /var/www/ietudsm/staticfiles
python manage.py collectstatic --noinput
```

### Database connection errors
```bash
sudo -u postgres psql
# Check if database and user exist
\l
\du
```

### Permission errors
```bash
sudo chown -R www-data:www-data /var/www/ietudsm
sudo chmod -R 755 /var/www/ietudsm
```

## Production Checklist

- [ ] DEBUG=False in .env
- [ ] SECRET_KEY changed from default
- [ ] ALLOWED_HOSTS set correctly
- [ ] SSL certificate installed
- [ ] Database backups configured
- [ ] Firewall configured
- [ ] Static files collected
- [ ] Media files permissions set
- [ ] Logging configured
- [ ] Gunicorn service running
- [ ] Nginx configured and running
- [ ] CSRF_TRUSTED_ORIGINS set
- [ ] Superuser account created
