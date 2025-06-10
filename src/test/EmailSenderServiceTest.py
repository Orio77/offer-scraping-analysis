import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

import unittest
from src.main.service.EmailSenderService import EmailSenderService
from src.main.model.JobOffer import JobOffer
from src.main.service.EmailFormatService import EmailFormatService
from src.main.config.logger_config import log

class TestEmailSenderService(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.email_sender = EmailSenderService()
        self.email_formatter = EmailFormatService()
        log.info("Setting up EmailSenderService test")
    
    def test_send_simple_email(self):
        """Test sending a simple email with default settings"""
        log.info("Testing simple email sending")
        
        subject = "Test Email from EmailSenderService"
        body = "This is a test email sent from the EmailSenderService unit test."
        
        try:
            results = self.email_sender.send_email(body=body, subject=subject)
            log.info(f"Email sending results: {results}")
            
            # Check that we got results back
            self.assertIsInstance(results, dict)
            
            # If there are configured recipients, check that we got results for them
            if self.email_sender.to_emails:
                self.assertGreater(len(results), 0, "Should have results for configured email addresses")
                for email, success in results.items():
                    log.info(f"Email to {email}: {'SUCCESS' if success else 'FAILED'}")
            else:
                log.warning("No recipient emails configured in .env file")
                
        except Exception as e:
            log.error(f"Exception during email sending test: {e}", exc_info=True)
            self.fail(f"Email sending failed with exception: {e}")
    
    def test_send_job_offers_email(self):
        """Test sending an email with formatted job offers"""
        log.info("Testing job offers email sending")
        
        # Create sample job offers
        offers = [
            JobOffer(
                title="Test Python Developer",
                company="Test Company",
                location="Test City",
                salary="5000-7000 PLN",
                url="https://example.com/job/1",
                site_id="test_site",
                add_info="This is a test job offer"
            ),
            JobOffer(
                title="Test Java Developer",
                company="Another Test Company",
                location="Another Test City",
                salary=None,
                url="https://example.com/job/2",
                site_id="test_site_2",
                add_info=None
            )
        ]
        
        # Format the email content
        email_body = self.email_formatter.format_job_offers_email(offers)
        email_subject = self.email_formatter.format_email_subject(offers)
        
        log.info(f"Generated email subject: {email_subject}")
        log.info(f"Generated email body (first 200 chars): {email_body[:200]}...")
        
        try:
            results = self.email_sender.send_email(body=email_body, subject=email_subject)
            log.info(f"Job offers email sending results: {results}")
            
            # Check that we got results back
            self.assertIsInstance(results, dict)
            
            # If there are configured recipients, check that we got results for them
            if self.email_sender.to_emails:
                self.assertGreater(len(results), 0, "Should have results for configured email addresses")
                for email, success in results.items():
                    log.info(f"Job offers email to {email}: {'SUCCESS' if success else 'FAILED'}")
            else:
                log.warning("No recipient emails configured in .env file")
                
        except Exception as e:
            log.error(f"Exception during job offers email sending test: {e}", exc_info=True)
            self.fail(f"Job offers email sending failed with exception: {e}")
    
    def test_send_email_custom_recipients(self):
        """Test sending email to custom recipients"""
        log.info("Testing email sending with custom recipients")
        
        # Use the same email as configured in .env as a safe test recipient
        if self.email_sender.from_email:
            custom_recipients = [self.email_sender.from_email]
            
            subject = "Test Email with Custom Recipients"
            body = "This is a test email sent to custom recipients."
            
            try:
                results = self.email_sender.send_email(
                    body=body, 
                    subject=subject, 
                    to_emails=custom_recipients
                )
                log.info(f"Custom recipients email sending results: {results}")
                
                # Check that we got results back
                self.assertIsInstance(results, dict)
                self.assertEqual(len(results), 1, "Should have exactly one result for one recipient")
                
                for email, success in results.items():
                    log.info(f"Custom recipient email to {email}: {'SUCCESS' if success else 'FAILED'}")
                    
            except Exception as e:
                log.error(f"Exception during custom recipients email sending test: {e}", exc_info=True)
                self.fail(f"Custom recipients email sending failed with exception: {e}")
        else:
            log.warning("FROM_EMAIL not configured in .env file, skipping custom recipients test")
            self.skipTest("FROM_EMAIL not configured")
    
    def test_send_email_empty_recipients(self):
        """Test behavior when no recipients are provided"""
        log.info("Testing email sending with empty recipients")
        
        subject = "Test Email - Should Not Send"
        body = "This email should not be sent due to empty recipients."
        
        results = self.email_sender.send_email(body=body, subject=subject, to_emails=[])
        log.info(f"Empty recipients email sending results: {results}")
        
        # Should return empty dict when no recipients
        self.assertIsInstance(results, dict)
        self.assertEqual(len(results), 0, "Should return empty results for empty recipients")
    
    def test_email_service_configuration(self):
        """Test that the email service is properly configured"""
        log.info("Testing email service configuration")
        
        # Check that essential configuration is present
        self.assertIsNotNone(self.email_sender.from_email, "FROM_EMAIL should be configured")
        self.assertIsNotNone(self.email_sender.password, "PASSWORD should be configured")
        self.assertIsNotNone(self.email_sender.smtp_server, "SMTP_SERVER should be configured")
        self.assertIsNotNone(self.email_sender.smtp_port, "SMTP_PORT should be configured")
        
        log.info(f"Email service configured with:")
        log.info(f"  FROM_EMAIL: {self.email_sender.from_email}")
        log.info(f"  TO_EMAILS: {self.email_sender.to_emails}")
        log.info(f"  SMTP_SERVER: {self.email_sender.smtp_server}")
        log.info(f"  SMTP_PORT: {self.email_sender.smtp_port}")
        
        # Check that SMTP port is valid
        self.assertIsInstance(self.email_sender.smtp_port, int, "SMTP_PORT should be an integer")
        self.assertGreater(self.email_sender.smtp_port, 0, "SMTP_PORT should be positive")

if __name__ == '__main__':
    log.info("Starting EmailSenderService tests")
    unittest.main(verbosity=2)
    log.info("EmailSenderService tests completed")