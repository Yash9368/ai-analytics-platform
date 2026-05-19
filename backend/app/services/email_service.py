import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from app.config.settings import settings

logger = logging.getLogger(__name__)

class EmailService:
    """
    Automated SMTP mailing services for AI Analytics Platform.
    Provides premium HTML-formatted email confirmations for customers and instant notifications for admins.
    """

    @staticmethod
    def _send_smtp_email(to_email: str, subject: str, html_content: str) -> bool:
        """Helper to establish SMTP connection and send email securely."""
        # Check if email settings are missing or incomplete
        if not settings.SMTP_USER or not settings.SMTP_PASSWORD:
            logger.warning("SMTP credentials are not configured. Skipping automated email delivery.")
            return False

        from_email = settings.SMTP_FROM_EMAIL or settings.SMTP_USER
        from_name = settings.SMTP_FROM_NAME

        try:
            # Create message container
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = f"{from_name} <{from_email}>"
            msg["To"] = to_email

            # Attach HTML payload
            msg.attach(MIMEText(html_content, "html"))

            # Initialize SMTP connection (supports standard port 587 with STARTTLS or 465 SSL fallback)
            logger.info(f"Connecting to SMTP server {settings.SMTP_HOST}:{settings.SMTP_PORT}...")
            
            if settings.SMTP_PORT == 465:
                server = smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT, timeout=10)
            else:
                server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=10)
                server.ehlo()
                server.starttls()
                server.ehlo()

            # Login and send
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.sendmail(from_email, to_email, msg.as_string())
            server.quit()
            
            logger.info(f"🟢 Automated email successfully dispatched to {to_email} with subject: '{subject}'")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to dispatch email via SMTP to {to_email}: {str(e)}")
            return False

    @classmethod
    def send_lead_confirmation(cls, customer_name: str, customer_email: str, company: str, phone: str, message: str) -> bool:
        """Sends a premium, branded HTML confirmation email to the lead/customer."""
        subject = "Your Demo Session is Confirmed! | AI Analytics Platform"
        
        # Premium dark-mode HTML template with smooth gradients, modern Outfit/Inter font vibes, and glassmorphism cards.
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Demo Request Confirmation</title>
            <style>
                body {{
                    margin: 0;
                    padding: 0;
                    background-color: #030303;
                    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
                    color: #e4e4e7;
                }}
                .wrapper {{
                    width: 100%;
                    background-color: #030303;
                    padding: 40px 0;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    background: linear-gradient(145deg, #0b0b0f 0%, #12121a 100%);
                    border: 1px solid rgba(255, 255, 255, 0.05);
                    border-radius: 20px;
                    overflow: hidden;
                    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
                }}
                .header {{
                    padding: 40px 30px 20px 30px;
                    text-align: center;
                    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
                    background: linear-gradient(to right, rgba(59, 130, 246, 0.1), rgba(139, 92, 246, 0.1));
                }}
                .logo-text {{
                    font-size: 26px;
                    font-weight: 800;
                    letter-spacing: -0.5px;
                    color: #ffffff;
                    margin: 0 0 10px 0;
                }}
                .logo-accent {{
                    background: linear-gradient(to right, #3b82f6, #8b5cf6);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                }}
                .subtitle {{
                    font-size: 14px;
                    color: #a1a1aa;
                    text-transform: uppercase;
                    letter-spacing: 2px;
                    font-weight: bold;
                    margin: 0;
                }}
                .content {{
                    padding: 40px 30px;
                }}
                h1 {{
                    font-size: 22px;
                    font-weight: 700;
                    color: #ffffff;
                    margin: 0 0 20px 0;
                }}
                p {{
                    font-size: 15px;
                    line-height: 1.6;
                    color: #a1a1aa;
                    margin: 0 0 24px 0;
                }}
                .lead-card {{
                    background: rgba(255, 255, 255, 0.02);
                    border: 1px solid rgba(255, 255, 255, 0.05);
                    border-radius: 14px;
                    padding: 24px;
                    margin: 30px 0;
                }}
                .card-title {{
                    font-size: 12px;
                    text-transform: uppercase;
                    font-weight: bold;
                    color: #3b82f6;
                    letter-spacing: 1.5px;
                    margin: 0 0 15px 0;
                }}
                .detail-row {{
                    display: flex;
                    margin-bottom: 12px;
                    font-size: 14px;
                }}
                .detail-label {{
                    width: 120px;
                    font-weight: bold;
                    color: #71717a;
                }}
                .detail-val {{
                    color: #e4e4e7;
                    flex: 1;
                }}
                .msg-box {{
                    background: rgba(0, 0, 0, 0.3);
                    border: 1px solid rgba(255, 255, 255, 0.03);
                    border-radius: 8px;
                    padding: 15px;
                    margin-top: 15px;
                    font-style: italic;
                    color: #d4d4d8;
                    font-size: 14px;
                    line-height: 1.5;
                }}
                .action-button {{
                    display: inline-block;
                    background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%);
                    color: #ffffff !important;
                    text-decoration: none;
                    font-weight: bold;
                    font-size: 14px;
                    padding: 14px 30px;
                    border-radius: 12px;
                    text-align: center;
                    transition: transform 0.2s ease;
                    margin-top: 10px;
                }}
                .footer {{
                    padding: 30px;
                    text-align: center;
                    font-size: 12px;
                    color: #71717a;
                    border-top: 1px solid rgba(255, 255, 255, 0.05);
                }}
                .footer a {{
                    color: #3b82f6;
                    text-decoration: none;
                }}
            </style>
        </head>
        <body>
            <div class="wrapper">
                <div class="container">
                    <div class="header">
                        <div class="logo-text">AI Analytics <span class="logo-accent">Platform</span></div>
                        <div class="subtitle">Google Analytics 4 Intelligence</div>
                    </div>
                    <div class="content">
                        <h1>Hi {customer_name},</h1>
                        <p>Thank you for booking a demo! Our team of analytics integration specialists is excited to connect with you. We are currently reviewing your custom goals and requirements to tailor a system specific to your business needs.</p>
                        
                        <p>Here is a summary of the details you submitted:</p>
                        
                        <div class="lead-card">
                            <div class="card-title">Demo Registration Details</div>
                            <div class="detail-row">
                                <span class="detail-label">Name:</span>
                                <span class="detail-val">{customer_name}</span>
                            </div>
                            <div class="detail-row">
                                <span class="detail-label">Company:</span>
                                <span class="detail-val">{company}</span>
                            </div>
                            <div class="detail-row">
                                <span class="detail-label">Email:</span>
                                <span class="detail-val">{customer_email}</span>
                            </div>
                            <div class="detail-row">
                                <span class="detail-label">Phone:</span>
                                <span class="detail-val">{phone}</span>
                            </div>
                            <div class="detail-row" style="margin-bottom: 0;">
                                <span class="detail-label">Message:</span>
                            </div>
                            <div class="msg-box">"{message}"</div>
                        </div>

                        <p><strong>What's Next?</strong><br>
                        One of our technical experts will reach out to you within the next 24 hours to schedule a convenient calendar slot for your live GA4 walkthrough and performance visualization.</p>
                        
                        <div style="text-align: center; margin-top: 30px;">
                            <a href="{settings.FRONTEND_URL}" class="action-button">Explore Dashboard</a>
                        </div>
                    </div>
                    <div class="footer">
                        &copy; 2026 AI Analytics Platform. All rights reserved.<br>
                        Powered by Google Analytics 4 Data API & Advanced Analytics Services.
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        return cls._send_smtp_email(customer_email, subject, html_content)

    @classmethod
    def send_admin_notification(cls, lead_id: str, lead_name: str, lead_email: str, company: str, phone: str, message: str) -> bool:
        """Sends an instant, actionable HTML notification email to the admin team."""
        admin_email = settings.ADMIN_EMAIL or settings.SMTP_USER
        if not admin_email:
            logger.warning("ADMIN_EMAIL is not configured. Falling back to SMTP_USER.")
            return False

        subject = f"🚨 NEW DEMO REQUEST: {lead_name} ({company})"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>New Lead Captured</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    color: #333333;
                    background-color: #f4f4f7;
                    padding: 20px;
                }}
                .card {{
                    max-width: 600px;
                    margin: 0 auto;
                    background: #ffffff;
                    border: 1px solid #e1e1e8;
                    border-radius: 12px;
                    overflow: hidden;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
                }}
                .header {{
                    background-color: #2563eb;
                    color: #ffffff;
                    padding: 24px;
                    font-size: 20px;
                    font-weight: bold;
                }}
                .section {{
                    padding: 24px;
                }}
                .lead-table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-bottom: 20px;
                }}
                .lead-table td {{
                    padding: 10px 0;
                    border-bottom: 1px solid #f3f4f6;
                    font-size: 14px;
                }}
                .lead-table td.label {{
                    font-weight: bold;
                    color: #6b7280;
                    width: 140px;
                }}
                .lead-table td.value {{
                    color: #111827;
                }}
                .msg-block {{
                    background-color: #f9fafb;
                    border-left: 4px solid #2563eb;
                    padding: 15px;
                    font-style: italic;
                    color: #4b5563;
                    font-size: 14px;
                    line-height: 1.5;
                    border-radius: 0 8px 8px 0;
                }}
                .footer {{
                    background-color: #f9fafb;
                    text-align: center;
                    padding: 15px;
                    font-size: 12px;
                    color: #9ca3af;
                    border-top: 1px solid #f3f4f6;
                }}
                .btn-row {{
                    margin-top: 20px;
                    display: flex;
                    gap: 15px;
                }}
                .btn {{
                    display: inline-block;
                    padding: 10px 20px;
                    color: #ffffff !important;
                    text-decoration: none;
                    font-weight: bold;
                    font-size: 13px;
                    border-radius: 6px;
                }}
                .btn-primary {{
                    background-color: #2563eb;
                }}
                .btn-secondary {{
                    background-color: #4b5563;
                }}
            </style>
        </head>
        <body>
            <div class="card">
                <div class="header">
                    New Demo Request captured!
                </div>
                <div class="section">
                    <p style="font-size: 14px; color: #4b5563; margin-top: 0;">A new high-value lead has completed the contact form on your AI Analytics Platform landing page:</p>
                    
                    <table class="lead-table">
                        <tr>
                            <td class="label">Lead ID</td>
                            <td class="value" style="font-family: monospace; font-weight: bold; color: #2563eb;">{lead_id}</td>
                        </tr>
                        <tr>
                            <td class="label">Full Name</td>
                            <td class="value" style="font-weight: bold;">{lead_name}</td>
                        </tr>
                        <tr>
                            <td class="label">Company Name</td>
                            <td class="value">{company}</td>
                        </tr>
                        <tr>
                            <td class="label">Email Address</td>
                            <td class="value"><a href="mailto:{lead_email}">{lead_email}</a></td>
                        </tr>
                        <tr>
                            <td class="label">Phone Number</td>
                            <td class="value"><a href="tel:{phone}">{phone}</a></td>
                        </tr>
                    </table>
                    
                    <p style="font-weight: bold; font-size: 13px; color: #4b5563; margin-bottom: 8px;">Custom Requirements / Message:</p>
                    <div class="msg-block">
                        "{message}"
                    </div>
                    
                    <div class="btn-row">
                        <a href="mailto:{lead_email}?subject=Regarding your AI Analytics Demo Request&body=Hi {lead_name}," class="btn btn-primary">Email Customer</a>
                        <a href="{settings.FRONTEND_URL}/admin" class="btn btn-secondary">Open Leads Hub</a>
                    </div>
                </div>
                <div class="footer">
                    Automatic Notification sent from AI Analytics Platform backend.
                </div>
            </div>
        </body>
        </html>
        """
        return cls._send_smtp_email(admin_email, subject, html_content)
