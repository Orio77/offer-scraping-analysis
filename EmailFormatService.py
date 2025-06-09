from typing import List
from JobOffer import JobOffer
from datetime import datetime

class EmailFormatService:
    def __init__(self):
        pass
    
    def format_job_offers_email(self, offers: List[JobOffer]) -> str:
        return self._format_simple_email(offers)
    
    
    def _format_simple_email(self, offers: List[JobOffer]) -> str:
        """Format a simple email with essential offer information"""
        total_offers = len(offers)
        sites_count = len(set(offer.site_id for offer in offers))
        
        body = f"""Job Offers Report - {datetime.now().strftime('%Y-%m-%d %H:%M')}

        Total new offers found: {total_offers}
        """

        if offers:
            body += f"Sites scraped: {sites_count}\n"
            body += "Offers:\n\n"

        for i, offer in enumerate(offers, 1):
            body += f"OFFER #{i}\n"
            
            if offer.title:
                body += f"Position: {offer.title}\n"
            if offer.company:
                body += f"Company: {offer.company}\n"
            if offer.location:
                body += f"Location: {offer.location}\n"
            if offer.salary:
                body += f"Salary: {offer.salary}\n"
            if offer.site_id:
                body += f"Source: {offer.site_id}\n"
            if offer.url:
                body += f"URL: {offer.url}\n"
            if offer.add_info:
                body += f"Additional Info: {offer.add_info}\n"
            
            body += "\n" + "-" * 50 + "\n\n"
        
        return body
    
    def format_email_subject(self, offers: List[JobOffer]) -> str:
        """Generate email subject based on offers"""
        if not offers:
            return f"Job Scraper Report - No offers found ({datetime.now().strftime('%Y-%m-%d')})"
        
        total_offers = len(offers)
        sites_count = len(set(offer.site_id for offer in offers))
        
        return f"Job Scraper Report - {total_offers} offers from {sites_count} sites ({datetime.now().strftime('%Y-%m-%d')})"