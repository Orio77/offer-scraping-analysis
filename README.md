# Job Offer Scraper & Email Sender

[![Job Scraper Scheduler](https://github.com/YOUR_USERNAME/offer-scraping-analysis/actions/workflows/job-scraper.yml/badge.svg)](https://github.com/YOUR_USERNAME/offer-scraping-analysis/actions/workflows/job-scraper.yml)

An automated job scraper that searches multiple job posting websites, extracts relevant job offers, and sends formatted email reports on a scheduled basis using GitHub Actions.

## Features

- 🔍 **Multi-site scraping** - Configurable scraping for multiple job websites
- 📧 **Email reports** - Automated email sending with formatted job offers
- ⏰ **Scheduled execution** - Runs automatically via GitHub Actions
- 🧪 **Comprehensive testing** - Unit tests for all components
- 📊 **Logging** - Detailed logs for monitoring and debugging
- ⚙️ **Configurable** - Easy configuration via YAML files

## Quick Start

### Local Development

1. **Clone the repository**

   ```bash
   git clone https://github.com/YOUR_USERNAME/offer-scraping-analysis.git
   cd offer-scraping-analysis
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**

   ```bash
   cp .env.example .env
   # Edit .env with your email credentials
   ```

4. **Run the scraper**
   ```bash
   python main.py
   ```

### GitHub Actions Setup

For automated scheduling, see [GITHUB_ACTIONS_SETUP.md](GITHUB_ACTIONS_SETUP.md) for detailed instructions.

## Configuration

### Job Sites (`resources/config.yml`)

Configure which websites to scrape and how to extract data:

```yaml
scraper:
  sites:
    - id: example-site
      url: "https://example.com/jobs"
      selectors:
        offerBox: "div.job-listing"
        title: "h2.job-title"
        company: ".company-name"
        location: ".job-location"
        salary: ".salary-info"
        url: "a.job-link"
```

### Email Settings (`.env`)

```bash
FROM_EMAIL=your-email@gmail.com
PASSWORD=your-app-password
TO_EMAILS=recipient1@email.com,recipient2@email.com
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
DEFAULT_SUBJECT=Daily Job Report
```

## Project Structure

```
├── main.py                 # Main application entry point
├── ConfigLoader.py         # Configuration management
├── ScraperService.py       # Web scraping logic
├── JobOffer.py            # Job offer data model
├── EmailFormatService.py   # Email formatting
├── EmailSenderService.py   # Email sending
├── logger_config.py        # Logging configuration
├── requirements.txt        # Python dependencies
├── resources/
│   └── config.yml         # Scraping configuration
├── test/                  # Unit tests
├── .github/workflows/     # GitHub Actions workflows
└── logs/                  # Application logs
```

## Testing

Run the test suite:

```bash
python -m pytest test/ -v
```

Test individual components:

```bash
python -m pytest test/ScraperServiceTest.py -v
python -m pytest test/EmailFormatServiceTest.py -v
python -m pytest test/EmailSenderServiceTest.py -v
python -m pytest test/ConfigLoaderTest.py -v
```

## Automation

The project includes two GitHub Actions workflows:

1. **Job Scraper Scheduler** (`.github/workflows/job-scraper.yml`)

   - Runs daily at 8:00 AM UTC
   - Executes the full scraping and email sending process
   - Can be triggered manually

## Monitoring

- **GitHub Actions**: View execution logs in the Actions tab
- **Email reports**: Receive formatted job offers via email
- **Log files**: Detailed logs stored in `logs/` directory
- **Artifacts**: Logs automatically uploaded for 30 days retention

## Customization

### Adding New Job Sites

1. Update `resources/config.yml` with new site configuration
2. Test selectors to ensure proper data extraction
3. Run tests to verify functionality

### Modifying Email Format

Edit `EmailFormatService.py` to customize:

- Email body structure
- Subject line format
- HTML formatting (if needed)

### Changing Schedule

Modify the cron expression in `.github/workflows/job-scraper.yml`:

```yaml
schedule:
  - cron: "0 8 * * *" # Daily at 8:00 AM UTC
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Security

- Use GitHub Secrets for sensitive information
- Never commit credentials to the repository
- Use Gmail App Passwords for email authentication
- Regularly update dependencies

---

**Note**: Replace `YOUR_USERNAME` in the badge URLs with your actual GitHub username.
