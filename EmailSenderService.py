import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from logger_config import log

# Load environment variables
load_dotenv()

class EmailSenderService:
    def __init__(self):
        log.info("Initializing EmailSenderService")
        self.from_email = os.getenv('FROM_EMAIL')
        self.password = os.getenv('GMAIL_PASSWORD')
        self.to_emails = [email.strip() for email in os.getenv('TO_EMAILS', '').split(',') if email.strip()]
        self.smtp_server = os.getenv('SMTP_SERVER')
        self.smtp_port = int(os.getenv('SMTP_PORT'))
        
        log.info(f"Email service configured with SMTP server: {self.smtp_server}:{self.smtp_port}")
        log.info(f"From email: {self.from_email}")
        log.info(f"Number of default recipients: {len(self.to_emails)}")

    def send_email(self, body, subject=None, to_emails=None):
        """
        Send an email via Gmail
        
        Args:
            subject (str): Email subject
            body (str): Email body content
            to_emails (list, optional): List of recipient email addresses. 
                                       If None, uses emails from .env file

        Returns:
            dict: Dictionary with results for each email address
        """
        log.info("Starting email sending process")
        
        if to_emails is None:
            to_emails = self.to_emails
            log.debug("Using default recipients from environment variables")
        else:
            log.debug(f"Using provided recipients: {len(to_emails)} emails")
        
        if not to_emails:
            log.warning("No recipient emails provided")
            print("No recipient emails provided")
            return {}
        
        if not subject:
            subject = os.getenv('DEFAULT_SUBJECT')
            log.debug(f"Using default subject: {subject}")
        else:
            log.debug(f"Using provided subject: {subject}")
        
        log.info(f"Preparing to send emails to {len(to_emails)} recipients")
        results = {}
        
        for to_email in to_emails:
            log.info(f"Attempting to send email to: {to_email}")
            try:
                # Create message
                msg = MIMEMultipart()
                msg['From'] = self.from_email
                msg['To'] = to_email
                msg['Subject'] = subject
                
                # Add body to email
                msg.attach(MIMEText(body, 'plain'))
                log.debug(f"Email message created for {to_email}")
                
                # Create SMTP session
                log.debug(f"Connecting to SMTP server: {self.smtp_server}:{self.smtp_port}")
                server = smtplib.SMTP(self.smtp_server, self.smtp_port)
                server.starttls()  # Enable security
                log.debug("STARTTLS enabled")
                
                server.login(self.from_email, self.password)
                log.debug("SMTP authentication successful")
                
                # Send email
                text = msg.as_string()
                server.sendmail(self.from_email, to_email, text)
                server.quit()
                log.debug("SMTP connection closed")
                
                log.info(f"Email sent successfully to {to_email}")
                print(f"Email sent successfully to {to_email}")
                results[to_email] = True
                
            except Exception as e:
                log.error(f"Error sending email to {to_email}: {str(e)}")
                print(f"Error sending email to {to_email}: {str(e)}")
                results[to_email] = False
        
        successful_sends = sum(1 for success in results.values() if success)
        log.info(f"Email sending completed. {successful_sends}/{len(to_emails)} emails sent successfully")
        
        return results