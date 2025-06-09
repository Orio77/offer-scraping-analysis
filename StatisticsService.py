from typing import Dict, List, Optional
from collections import Counter, defaultdict
import re
from SupabaseService import DatabaseConfig
from logger_config import log 

class StatisticsService:
    """Service for generating statistics from job offer data"""
    
    def __init__(self, data_provider=None):
        self.data_provider = data_provider or DatabaseConfig()
        log.info("StatisticsService initialized")
    
    def get_position_type_counts(self, position_keywords: Optional[Dict[str, List[str]]] = None) -> Dict[str, int]:
        # Default Polish position keywords if none provided
        if position_keywords is None:
            position_keywords = {
                "Sprzedawca/Konsultant": [
                    "sprzedawca", "sprzedawczyni", "konsultant", "doradca", "handlowiec",
                    "ambasador", "marki", "doradca klienta", "obsługa klienta"
                ],
                "Recepcjonista": [
                    "recepcjonista", "recepcjonistka", "recepcji", "recepcja"
                ],
                "Gastronomia": [
                    "kelner", "kelnerka", "barista", "barman", "sushi", "kucharz",
                    "restauracji", "kawiarnia", "lodziarnio", "bistro", "burgers"
                ],
                "Medyczny": [
                    "rejestrator medyczny", "rejestratorka medyczna", "medyczny", "medyczna",
                    "fizjoterapia", "sanepid"
                ],
                "Asystent/Pomoc": [
                    "asystent", "asystentka", "pomoc", "pomocnik", "pomocnica",
                    "asystent nauczyciela", "gym assistant"
                ],
                "Księgowość/Biuro": [
                    "księgowy", "księgowa", "biurowa", "biuro", "biurowy"
                ],
                "Transport/Dostawa": [
                    "dostawca", "kierowca", "podjazdowy", "transport", "dostawa"
                ],
                "Lektor/Nauczyciel": [
                    "lektor", "lektorka", "nauczyciel", "nauczycielka", "językowa"
                ],
                "Specjalista": [
                    "specjalista", "specialist", "depilacji", "wynajmu"
                ],
                "Produkcja": [
                    "produkcja", "pracownik produkcji", "production"
                ]
            }
        
        log.info(f"Starting position type analysis with {len(position_keywords)} position categories")
        log.debug(f"Position keywords: {position_keywords}")
        
        try:
            job_offers = self.data_provider.read_data()
            log.info(f"Retrieved {len(job_offers)} job offers from database")
        except Exception as e:
            log.error(f"Failed to retrieve job offers: {e}")
            raise
            
        position_counts = defaultdict(int)
        processed_offers = 0
        
        for offer in job_offers:
            # Handle None titles by categorizing as "Other"
            if not offer.title:
                position_counts["Inne"] += 1
                log.debug(f"Offer with empty title categorized as 'Inne' (ID: {getattr(offer, 'id', 'unknown')})")
                continue
                
            title_lower = offer.title.lower()
            log.debug(f"Processing offer title: '{offer.title}'")
            
            # Classify each offer based on keywords in the title
            classified = False
            for position_type, keywords in position_keywords.items():
                if any(keyword.lower() in title_lower for keyword in keywords):
                    position_counts[position_type] += 1
                    log.debug(f"Offer '{offer.title}' classified as '{position_type}'")
                    classified = True
                    break
            
            # If no match found, categorize as "Inne" (Other in Polish)
            if not classified:
                position_counts["Inne"] += 1
                log.debug(f"Offer '{offer.title}' could not be classified, categorized as 'Inne'")
            
            processed_offers += 1
        
        result = dict(position_counts)
        log.info(f"Position type analysis completed. Processed: {processed_offers} offers")
        log.info(f"Position distribution: {result}")
        
        return result
    
    def get_salary_statistics(self) -> Dict[str, any]:
        """Analyze salary data from Polish job offers"""
        log.info("Starting salary statistics analysis")
        
        try:
            job_offers = self.data_provider.read_data()
            log.info(f"Retrieved {len(job_offers)} job offers from database")
        except Exception as e:
            log.error(f"Failed to retrieve job offers: {e}")
            raise
        
        salary_data = []
        salary_ranges = []
        no_salary_count = 0
        
        for offer in job_offers:
            if not offer.salary or offer.salary.strip() == "":
                no_salary_count += 1
                continue
            
            # Parse Polish salary formats
            salary_text = offer.salary.lower()
            
            # Extract numbers from salary text
            numbers = re.findall(r'\d+(?:[,\.]\d+)?', salary_text)
            
            if len(numbers) >= 2:
                # Range format (e.g., "30,50 - 33 zł / godz. brutto")
                try:
                    min_salary = float(numbers[0].replace(',', '.'))
                    max_salary = float(numbers[1].replace(',', '.'))
                    avg_salary = (min_salary + max_salary) / 2
                    salary_data.append(avg_salary)
                    salary_ranges.append((min_salary, max_salary))
                except ValueError:
                    continue
            elif len(numbers) == 1:
                # Single value
                try:
                    salary_value = float(numbers[0].replace(',', '.'))
                    salary_data.append(salary_value)
                    salary_ranges.append((salary_value, salary_value))
                except ValueError:
                    continue
        
        if not salary_data:
            log.warning("No valid salary data found")
            return {
                "total_offers": len(job_offers),
                "offers_with_salary": 0,
                "offers_without_salary": no_salary_count,
                "average_salary": 0,
                "min_salary": 0,
                "max_salary": 0,
                "median_salary": 0
            }
        
        salary_data.sort()
        n = len(salary_data)
        median = salary_data[n//2] if n % 2 == 1 else (salary_data[n//2-1] + salary_data[n//2]) / 2
        
        result = {
            "total_offers": len(job_offers),
            "offers_with_salary": len(salary_data),
            "offers_without_salary": no_salary_count,
            "average_salary": round(sum(salary_data) / len(salary_data), 2),
            "min_salary": min(salary_data),
            "max_salary": max(salary_data),
            "median_salary": round(median, 2)
        }
        
        log.info(f"Salary analysis completed: {result}")
        return result