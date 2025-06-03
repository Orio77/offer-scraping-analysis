import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional, Any
from JobOffer import JobOffer
from logger_config import log 
from urllib.parse import urljoin, urlparse

class ScraperService:
    def __init__(self, sites_config: List[Dict[str, Any]]):
        if not sites_config:
            log.warning("ScraperService initialized with no site configurations.")
        self.sites_config = sites_config
        log.info(f"ScraperService initialized with {len(sites_config)} site configurations.")

    def _get_element_text(self, parent_element: BeautifulSoup, selector: str) -> Optional[str]:
        element = parent_element.select_one(selector)
        if element:
            return element.get_text(strip=True)
        log.debug(f"Element not found with selector '{selector}' in parent.")
        return None

    def _get_element_href(self, parent_element: BeautifulSoup, selector: str, base_url: Optional[str] = None) -> Optional[str]:
        element = parent_element.select_one(selector)
        if element and element.has_attr('href'):
            href = element['href']
            if base_url and not href.startswith(('http://', 'https://')):
                return urljoin(base_url, href)
            return href
        log.debug(f"Href not found for selector '{selector}' or element missing 'href' attribute.")
        return None

    def scrape_site(self, site_config: Dict[str, Any]) -> List[JobOffer]:
        site_id = site_config.get('id', 'UnknownSite') # Use .get for safer access
        url = site_config.get('url')
        selectors = site_config.get('selectors')

        if not url or not selectors:
            log.error(f"Missing 'url' or 'selectors' in site config for site_id '{site_id}'. Skipping.")
            return []
        
        log.info(f"Starting to scrape site: '{site_id}' from URL: {url}")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status() 
            log.debug(f"Successfully fetched URL: {url} with status code {response.status_code}")
        except requests.RequestException as e:
            log.error(f"Error fetching {url} for site '{site_id}': {e}", exc_info=True)
            return []

        soup = BeautifulSoup(response.content, 'html.parser')
        job_offers: List[JobOffer] = []

        offer_box_selector = selectors.get('offerBox')
        if not offer_box_selector:
            log.warning(f"No 'offerBox' selector defined for site '{site_id}'. Cannot find offer items.")
            return []

        offer_boxes = soup.select(offer_box_selector)
        if not offer_boxes:
            log.warning(f"No offer boxes found for site '{site_id}' with selector '{offer_box_selector}'. Check selectors or website structure.")
            log.debug(f"HTML snippet for {site_id} (first 2000 chars): {soup.prettify()[:2000]}") 
            return []
            
        log.info(f"Found {len(offer_boxes)} potential offer items on '{site_id}'.")

        title_selector = selectors.get('title')
        url_selector = selectors.get('url')

        if not title_selector or not url_selector:
            log.error(f"Core selectors 'title' or 'url' are missing for site_id '{site_id}'. Cannot process offers.")
            return []

        for i, box in enumerate(offer_boxes):
            log.debug(f"Processing item {i+1}/{len(offer_boxes)} for site '{site_id}'.")
            title = self._get_element_text(box, title_selector)
            company = self._get_element_text(box, selectors.get('company'))
            location = self._get_element_text(box, selectors.get('location'))
            salary = self._get_element_text(box, selectors.get('salary'))
            
            parsed_url = urlparse(url)
            base_url_for_links = f"{parsed_url.scheme}://{parsed_url.netloc}"
            
            offer_url = self._get_element_href(box, url_selector, base_url_for_links)
            
            add_info = None
            add_info_selector = selectors.get('addInfo')
            if add_info_selector: 
                add_info_element = box.select_one(add_info_selector)
                if add_info_element:
                    items = [li.get_text(strip=True) for li in add_info_element.find_all('li')]
                    add_info = ", ".join(items) if items else add_info_element.get_text(strip=True)
                    log.debug(f"Extracted add_info for item {i+1} on '{site_id}': {add_info[:100]}...") 
                else:
                    log.debug(f"addInfo element not found for item {i+1} on '{site_id}' with selector '{add_info_selector}'.")
            else:
                log.debug(f"'addInfo' selector not configured or empty for site '{site_id}'.")


            if title and offer_url:
                job_offers.append(JobOffer(
                    title=title,
                    company=company,
                    location=location,
                    salary=salary,
                    url=offer_url,
                    site_id=site_id,
                    add_info=add_info
                ))
                log.debug(f"Successfully parsed job offer on '{site_id}': Title='{title}', URL='{offer_url}'")
            else:
                log.warning(f"Skipping an item on '{site_id}' due to missing title or URL. Title: '{title}', URL: '{offer_url}'. Box snippet: {str(box)[:200]}")


        log.info(f"Finished scraping site '{site_id}'. Found {len(job_offers)} valid job offers.")
        return job_offers

    def scrape_all_sites(self) -> List[JobOffer]:
        all_offers: List[JobOffer] = []
        log.info("Starting to scrape all configured sites.")
        if not self.sites_config:
            log.warning("No sites configured to scrape.")
            return []
            
        for site_config in self.sites_config:
            log.info(f"Initiating scrape for site ID: {site_config.get('id', 'Unknown site')}")
            offers = self.scrape_site(site_config)
            all_offers.extend(offers)
            log.info(f"Completed scraping for site ID: {site_config.get('id', 'Unknown site')}. Found {len(offers)} offers.")
        log.info(f"Finished scraping all sites. Total offers found: {len(all_offers)}.")
        return all_offers