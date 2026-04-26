# utils/email_config.py

# 📧 Email Configuration for Sending Alerts/Reports

# Sender Gmail address used by the system to send emails
SENDER_EMAIL = "admins_email@gmail.com"

# ⚠️ IMPORTANT SECURITY NOTICE:
# - This must be a 16-character Google App Password (NOT your actual Gmail password)
# - To generate:
#     1. Enable 2-Step Verification on your Google account
#     2. Go to Security → App Passwords
#     3. Generate a password for "Mail"
#
# - NEVER commit real credentials to public repositories
# - Replace this value with your own App Password before running the project
# - If this file is shared, revoke the password immediately and create a new one

SENDER_PASSWORD = "your_16_character_app_password"