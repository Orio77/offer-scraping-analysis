import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import unittest
from datetime import datetime
from EmailFormatService import EmailFormatService
from JobOffer import JobOffer
from logger_config import log

class TestEmailFormatService(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.email_formatter = EmailFormatService()
        log.info("Setting up EmailFormatService test")
    
    def test_format_email_with_empty_offers_list(self):
        """Test formatting email with no offers"""
        log.info("Testing email formatting with empty offers list")
        
        offers = []
        result = self.email_formatter.format_job_offers_email(offers)
        
        self.assertIn("No job offers were found", result)
        self.assertIn("Job Offers Report", result)
        log.info("Empty offers list test passed")
    
    def test_format_email_with_single_complete_offer(self):
        """Test formatting email with one complete job offer"""
        log.info("Testing email formatting with single complete offer")
        
        offer = JobOffer(
            title="Python Developer",
            company="Tech Corp",
            location="Warsaw",
            salary="8000-12000 PLN",
            url="https://example.com/job/1",
            site_id="example_site",
            add_info="Remote work possible"
        )
        offers = [offer]
        
        result = self.email_formatter.format_job_offers_email(offers)
        
        # Check if all fields are present
        self.assertIn("Position: Python Developer", result)
        self.assertIn("Company: Tech Corp", result)
        self.assertIn("Location: Warsaw", result)
        self.assertIn("Salary: 8000-12000 PLN", result)
        self.assertIn("Source: example_site", result)
        self.assertIn("URL: https://example.com/job/1", result)
        self.assertIn("Additional Info: Remote work possible", result)
        self.assertIn("OFFER #1", result)
        self.assertIn("Total offers found: 1", result)
        
        log.info("Single complete offer test passed")
    
    def test_format_email_with_partial_offer(self):
        """Test formatting email with incomplete job offer (missing some fields)"""
        log.info("Testing email formatting with partial offer")
        
        offer = JobOffer(
            title="Java Developer",
            company=None,  # Missing company
            location="Krakow",
            salary=None,   # Missing salary
            url="https://example.com/job/2",
            site_id="another_site",
            add_info=None  # Missing additional info
        )
        offers = [offer]
        
        result = self.email_formatter.format_job_offers_email(offers)
        
        # Check if present fields are shown
        self.assertIn("Position: Java Developer", result)
        self.assertIn("Location: Krakow", result)
        self.assertIn("Source: another_site", result)
        self.assertIn("URL: https://example.com/job/2", result)
        
        # Check if missing fields are NOT shown
        self.assertNotIn("Company:", result)
        self.assertNotIn("Salary:", result)
        self.assertNotIn("Additional Info:", result)
        
        log.info("Partial offer test passed")
    
    def test_format_email_with_multiple_offers(self):
        """Test formatting email with multiple job offers"""
        log.info("Testing email formatting with multiple offers")
        
        offers = [
            JobOffer(
                title="Frontend Developer",
                company="StartupXYZ",
                location="Remote",
                salary="6000-9000 PLN",
                url="https://startup.com/job/1",
                site_id="startup_site",
                add_info="React experience required"
            ),
            JobOffer(
                title="Backend Developer",
                company="BigCorp",
                location="Gdansk",
                salary=None,  # Missing salary
                url="https://bigcorp.com/job/2",
                site_id="corp_site",
                add_info=None
            ),
            JobOffer(
                title="DevOps Engineer",
                company="TechFirm",
                location="Wroclaw",
                salary="10000-15000 PLN",
                url="https://techfirm.com/job/3",
                site_id="startup_site",  # Same site as first offer
                add_info="Docker knowledge needed"
            )
        ]
        
        result = self.email_formatter.format_job_offers_email(offers)
        
        # Check if all offers are present
        self.assertIn("OFFER #1", result)
        self.assertIn("OFFER #2", result)
        self.assertIn("OFFER #3", result)
        
        # Check summary information
        self.assertIn("Total offers found: 3", result)
        self.assertIn("Sites scraped: 2", result)  # startup_site and corp_site
        
        # Check specific offer details
        self.assertIn("Frontend Developer", result)
        self.assertIn("Backend Developer", result)
        self.assertIn("DevOps Engineer", result)
        
        # Check separators
        self.assertEqual(result.count("-" * 50), 3)  # Should have 3 separators
        
        log.info("Multiple offers test passed")
    
    def test_format_email_subject_with_offers(self):
        """Test email subject formatting with offers"""
        log.info("Testing email subject formatting with offers")
        
        offers = [
            JobOffer("Job1", "Company1", "Location1", None, "url1", "site1"),
            JobOffer("Job2", "Company2", "Location2", None, "url2", "site2"),
            JobOffer("Job3", "Company3", "Location3", None, "url3", "site1")  # Same site as first
        ]
        
        subject = self.email_formatter.format_email_subject(offers)
        
        self.assertIn("3 offers from 2 sites", subject)
        self.assertIn("Job Scraper Report", subject)
        self.assertIn(datetime.now().strftime('%Y-%m-%d'), subject)
        
        log.info("Email subject with offers test passed")
    
    def test_format_email_subject_without_offers(self):
        """Test email subject formatting without offers"""
        log.info("Testing email subject formatting without offers")
        
        offers = []
        subject = self.email_formatter.format_email_subject(offers)
        
        self.assertIn("No offers found", subject)
        self.assertIn("Job Scraper Report", subject)
        self.assertIn(datetime.now().strftime('%Y-%m-%d'), subject)
        
        log.info("Email subject without offers test passed")
    
    def test_sites_count_calculation(self):
        """Test that sites count is calculated correctly"""
        log.info("Testing sites count calculation")
        
        offers = [
            JobOffer("Job1", "Company1", "Location1", None, "url1", "site_a"),
            JobOffer("Job2", "Company2", "Location2", None, "url2", "site_a"),  # Same site
            JobOffer("Job3", "Company3", "Location3", None, "url3", "site_b"),
            JobOffer("Job4", "Company4", "Location4", None, "url4", "site_c"),
            JobOffer("Job5", "Company5", "Location5", None, "url5", "site_a")   # Same site again
        ]
        
        result = self.email_formatter.format_job_offers_email(offers)
        
        # Should be 3 unique sites: site_a, site_b, site_c
        self.assertIn("Sites scraped: 3", result)
        self.assertIn("Total offers found: 5", result)
        
        log.info("Sites count calculation test passed")

if __name__ == '__main__':
    log.info("Starting EmailFormatService tests")
    unittest.main(verbosity=2)
    log.info("EmailFormatService tests completed")