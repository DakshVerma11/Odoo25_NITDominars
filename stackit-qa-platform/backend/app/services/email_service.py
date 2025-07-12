from flask import current_app, render_template
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(recipient, subject, template, **kwargs):
    """
    Send an email using SMTP
    
    Args:
        recipient: Email address of the recipient
        subject: Email subject
        template: HTML template to use for email body
        **kwargs: Variables to pass to the template
    """
    # Skip sending if SMTP is not configured or in testing mode
    if not current_app.config.get('MAIL_SERVER') or current_app.testing:
        current_app.logger.info(f"Email sending skipped: {subject} to {recipient}")
        return True
    
    try:
        # Render template
        html_content = render_template(template, **kwargs)
        
        # Create message
        message = MIMEMultipart('alternative')
        message['Subject'] = subject
        message['From'] = current_app.config['MAIL_DEFAULT_SENDER']
        message['To'] = recipient
        
        # Attach HTML content
        message.attach(MIMEText(html_content, 'html'))
        
        # Connect to SMTP server
        with smtplib.SMTP(
            current_app.config['MAIL_SERVER'], 
            current_app.config['MAIL_PORT']
        ) as server:
            
            # Use TLS if configured
            if current_app.config.get('MAIL_USE_TLS'):
                server.starttls()
            
            # Login if username and password provided
            if current_app.config.get('MAIL_USERNAME') and current_app.config.get('MAIL_PASSWORD'):
                server.login(
                    current_app.config['MAIL_USERNAME'],
                    current_app.config['MAIL_PASSWORD']
                )
            
            # Send email
            server.sendmail(
                current_app.config['MAIL_DEFAULT_SENDER'],
                recipient,
                message.as_string()
            )
        
        current_app.logger.info(f"Email sent successfully: {subject} to {recipient}")
        return True
    
    except Exception as e:
        current_app.logger.error(f"Failed to send email: {str(e)}")
        return False

def send_welcome_email(user):
    """Send welcome email to new user"""
    return send_email(
        recipient=user.email,
        subject="Welcome to StackIt!",
        template="emails/welcome.html",
        user=user
    )

def send_password_reset_email(user, reset_token):
    """Send password reset email"""
    return send_email(
        recipient=user.email,
        subject="Password Reset Request",
        template="emails/password_reset.html",
        user=user,
        reset_token=reset_token
    )

def send_notification_digest(user, notifications):
    """Send digest of unread notifications"""
    return send_email(
        recipient=user.email,
        subject="Your StackIt Notifications",
        template="emails/notification_digest.html",
        user=user,
        notifications=notifications
    )