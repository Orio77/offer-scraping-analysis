import unittest
from unittest.mock import MagicMock
import sys
import os

# Add parent directory to path to import project modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.main.service.StatisticsService import StatisticsService
from src.main.model.JobOffer import JobOffer

class TestStatisticsService(unittest.TestCase):
    def setUp(self):
        # Create mock Polish job offers based on the CSV data
        self.mock_offers = [
            JobOffer(
                title="Ambasador Marki IQOS",
                company="Test Company",
                location="Wrocław, Stare Miasto",
                salary="33 - 53 zł / godz. brutto",
                url="https://example.com/1",
                site_id="olx.pl"
            ),
            JobOffer(
                title="Doradca Klienta kaes. Wrocław",
                company="Test Company",
                location="Wrocław, Psie Pole",
                salary="",
                url="https://example.com/2",
                site_id="olx.pl"
            ),
            JobOffer(
                title="Kelnerka / Kelner",
                company="Test Restaurant",
                location="Wrocław, Stare Miasto",
                salary="30,50 - 30,60 zł / godz. brutto",
                url="https://example.com/3",
                site_id="olx.pl"
            ),
            JobOffer(
                title="Recepcjonista/recepcjonistka",
                company="Test Hotel",
                location="Wrocław, Stare Miasto",
                salary="31 zł / godz. brutto",
                url="https://example.com/4",
                site_id="olx.pl"
            ),
            JobOffer(
                title="Rejestrator medyczny / Rejestratorka medyczna",
                company="Test Clinic",
                location="Wrocław, Fabryczna",
                salary="30,50 - 35 zł / godz. brutto",
                url="https://example.com/5",
                site_id="olx.pl"
            ),
            JobOffer(
                title=None,  # Empty title to test handling
                company="Test Company",
                location="Wrocław",
                salary="30 zł / godz. brutto",
                url="https://example.com/6",
                site_id="olx.pl"
            )
        ]
        
        # Create service with mock data provider
        mock_provider = MagicMock()
        mock_provider.read_data.return_value = self.mock_offers
        self.service = StatisticsService(mock_provider)
        
    def test_get_position_type_counts_default_polish_keywords(self):
        """Test position type categorization with default Polish keywords"""
        result = self.service.get_position_type_counts()
        
        # Check expected categorizations based on mock data
        self.assertEqual(result.get("Sprzedawca/Konsultant", 0), 2)  # Ambasador + Doradca
        self.assertEqual(result.get("Gastronomia", 0), 1)  # Kelner/Kelnerka
        self.assertEqual(result.get("Recepcjonista", 0), 1)  # Recepcjonista
        self.assertEqual(result.get("Medyczny", 0), 1)  # Rejestrator medyczny
        self.assertEqual(result.get("Inne", 0), 1)  # None title
        
    def test_get_position_type_counts_custom_keywords(self):
        """Test position type categorization with custom keywords"""
        custom_keywords = {
            "Obsługa": ["doradca", "ambasador"],
            "Restauracja": ["kelner", "kelnerka"],
            "Hotel": ["recepcjonista"]
        }
        
        result = self.service.get_position_type_counts(custom_keywords)
        
        # Check custom categorizations
        self.assertEqual(result.get("Obsługa", 0), 2)  # Ambasador + Doradca
        self.assertEqual(result.get("Restauracja", 0), 1)  # Kelner/Kelnerka
        self.assertEqual(result.get("Hotel", 0), 1)  # Recepcjonista
        self.assertEqual(result.get("Inne", 0), 2)  # Rejestrator medyczny + None title
        
    def test_get_position_type_counts_empty_keywords(self):
        """Test with empty keywords dictionary"""
        result = self.service.get_position_type_counts({})
        
        # All offers should be categorized as "Inne" (Polish for "Other")
        self.assertEqual(result.get("Inne", 0), 6)
        
    def test_get_salary_statistics(self):
        """Test salary statistics analysis with Polish salary formats"""
        result = self.service.get_salary_statistics()
        
        # Check basic statistics structure
        self.assertIn("total_offers", result)
        self.assertIn("offers_with_salary", result)
        self.assertIn("offers_without_salary", result)
        self.assertIn("average_salary", result)
        self.assertIn("min_salary", result)
        self.assertIn("max_salary", result)
        self.assertIn("median_salary", result)
        
        # Check expected values based on mock data
        self.assertEqual(result["total_offers"], 6)
        self.assertEqual(result["offers_with_salary"], 5)  # 5 offers have salary data
        self.assertEqual(result["offers_without_salary"], 1)  # 1 offer without salary

        # Check that salary values are reasonable (between 30-53 zł/h based on mock data)
        self.assertGreater(result["average_salary"], 25)
        self.assertLess(result["average_salary"], 60)
        self.assertGreater(result["min_salary"], 25)
        self.assertLess(result["max_salary"], 60)
        
    def test_get_salary_statistics_no_salary_data(self):
        """Test salary statistics when no salary data is available"""
        # Create offers without salary data
        no_salary_offers = [
            JobOffer(
                title="Test Job",
                company="Test Company",
                location="Wrocław",
                salary="",
                url="https://example.com/1",
                site_id="olx.pl"
            )
        ]
        
        mock_provider = MagicMock()
        mock_provider.read_data.return_value = no_salary_offers
        test_service = StatisticsService(mock_provider)
        
        result = test_service.get_salary_statistics()
        
        # Check that all salary statistics are 0
        self.assertEqual(result["offers_with_salary"], 0)
        self.assertEqual(result["offers_without_salary"], 1)
        self.assertEqual(result["average_salary"], 0)
        self.assertEqual(result["min_salary"], 0)
        self.assertEqual(result["max_salary"], 0)
        self.assertEqual(result["median_salary"], 0)

if __name__ == "__main__":
    unittest.main()