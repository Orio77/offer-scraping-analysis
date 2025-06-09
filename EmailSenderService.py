import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class EmailSenderService:
    def __init__(self):
        self.from_email = os.getenv('FROM_EMAIL')
        self.password = os.getenv('PASSWORD')
        self.to_emails = [email.strip() for email in os.getenv('TO_EMAILS', '').split(',') if email.strip()]
        self.smtp_server = os.getenv('SMTP_SERVER')
        self.smtp_port = int(os.getenv('SMTP_PORT'))  

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
        if to_emails is None:
            to_emails = self.to_emails
        
        if not to_emails:
            print("No recipient emails provided")
            return {}
        
        if not subject:
            subject = os.getenv('DEFAULT_SUBJECT')
        
        results = {}
        
        for to_email in to_emails:
            try:
                # Create message
                msg = MIMEMultipart()
                msg['From'] = self.from_email
                msg['To'] = to_email
                msg['Subject'] = subject
                
                # Add body to email
                msg.attach(MIMEText(body, 'plain'))
                
                # Create SMTP session
                server = smtplib.SMTP(self.smtp_server, self.smtp_port)
                server.starttls()  # Enable security
                server.login(self.from_email, self.password)
                
                # Send email
                text = msg.as_string()
                server.sendmail(self.from_email, to_email, text)
                server.quit()
                
                print(f"Email sent successfully to {to_email}")
                results[to_email] = True
                
            except Exception as e:
                print(f"Error sending email to {to_email}: {str(e)}")
                results[to_email] = False
        
        return results