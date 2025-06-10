# Job Offer Scraper & Analysis System

[![Job Scraper Scheduler](https://github.com/YOUR_USERNAME/offer-scraping-analysis/actions/workflows/job-scraper.yml/badge.svg)](https://github.com/YOUR_USERNAME/offer-scraping-analysis/actions/workflows/job-scraper.yml)

A comprehensive job scraping and analysis system that automatically searches job posting websites, stores data in a database, provides statistical analysis, and offers both GUI and automated email reporting capabilities.

## Features

- 🔍 **Multi-site scraping** - Configurable scraping for multiple job websites (currently OLX.pl)
- 💾 **Database storage** - Persistent data storage using Supabase/PostgreSQL
- 📊 **Statistics & Analytics** - Advanced job market analysis including salary statistics and position categorization
- 🖥️ **GUI Application** - Modern desktop interface built with CustomTkinter for data visualization
- 📧 **Email reports** - Automated email sending with formatted job offers
- ⏰ **Scheduled execution** - Runs automatically via GitHub Actions
- 🧪 **Comprehensive testing** - Unit tests for all components
- 📊 **Logging** - Detailed logs for monitoring and debugging
- ⚙️ **Configurable** - Easy configuration via YAML files
- 📈 **Data visualization** - Charts and graphs for job market trends

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

   Create a `.env` file with your credentials:

   ```bash
   # Email configuration
   FROM_EMAIL=your-email@gmail.com
   GMAIL_PASSWORD=your-app-password
   TO_EMAILS=recipient1@email.com,recipient2@email.com
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   DEFAULT_SUBJECT=Daily Job Report

   # Supabase/Database configuration
   SUPABASE_URL=your-supabase-url
   SUPABASE_ANON_KEY=your-supabase-anon-key
   SUPABASE_DB_HOST=your-db-host
   SUPABASE_DB_NAME=your-db-name
   SUPABASE_DB_USER=your-db-user
   SUPABASE_DB_PASSWORD=your-db-password
   SUPABASE_DB_PORT=5432
   ```

4. **Run the application**

   **Command Line (Scraping & Email):**

   ```bash
   python -m src.main.main
   ```

   **GUI Application:**

   ```bash
   python -m src.main.GUI
   ```

   **Windows Batch File:**

   ```cmd
   run.cmd
   ```

### GitHub Actions Setup

For automated scheduling, see [GITHUB_ACTIONS_SETUP.md](GITHUB_ACTIONS_SETUP.md) for detailed instructions.

## Configuration

### Job Sites (`src/resources/config.yml`)

Configure which websites to scrape and how to extract data:

```yaml
scraper:
  sites:
    - id: olx.pl
      url: "https://www.olx.pl/praca/wroclaw/q-praca-dla-studenta/?search%5Bfilter_enum_experience%5D%5B0%5D=exp_no&search%5Bfilter_enum_type%5D%5B0%5D=parttime"
      selectors:
        offersContainer: 'div[data-testid="listing-grid"]'
        offerBox: '[data-cy="l-card"]'
        title: 'div[data-testid="l-card"] a h4'
        company: 'div[data-testid="l-card"] div[class^="css-1lb10r"]'
        location: 'div[data-testid="l-card"] div[class^="css-9yllbh"]:nth-of-type(2)'
        salary: 'div[data-testid="l-card"] div[class^="css-9yllbh"]:nth-of-type(1)'
        url: 'div[data-testid="l-card"] a[href]'
        addInfo: 'div[data-testid="l-card"] div[class^="css-mr8xj"]'
```

### Environment Variables (`.env`)

```bash
# Email Settings
FROM_EMAIL=your-email@gmail.com
GMAIL_PASSWORD=your-app-password
TO_EMAILS=recipient1@email.com,recipient2@email.com
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
DEFAULT_SUBJECT=Daily Job Report

# Database Settings (Supabase/PostgreSQL)
SUPABASE_URL=your-supabase-url
SUPABASE_ANON_KEY=your-supabase-anon-key
SUPABASE_DB_HOST=your-db-host
SUPABASE_DB_NAME=your-db-name
SUPABASE_DB_USER=your-db-user
SUPABASE_DB_PASSWORD=your-db-password
SUPABASE_DB_PORT=5432
```

## Project Structure

```
├── src/
│   ├── main/
│   │   ├── main.py                     # Main CLI application entry point
│   │   ├── GUI.py                      # Desktop GUI application
│   │   ├── config/
│   │   │   ├── ConfigLoader.py         # Configuration management
│   │   │   └── logger_config.py        # Logging configuration
│   │   ├── model/
│   │   │   └── JobOffer.py            # Job offer data model
│   │   ├── persistance/
│   │   │   └── Supabase.py            # Database operations (Supabase/PostgreSQL)
│   │   └── service/
│   │       ├── ScraperService.py       # Web scraping logic
│   │       ├── StatisticsService.py    # Data analysis and statistics
│   │       ├── EmailFormatService.py   # Email formatting
│   │       └── EmailSenderService.py   # Email sending
│   ├── resources/
│   │   └── config.yml                 # Scraping configuration
│   └── test/                          # Unit tests
│       ├── ConfigLoaderTest.py
│       ├── ScraperServiceTest.py
│       ├── StatisticsServiceTest.py
│       ├── EmailFormatServiceTest.py
│       └── EmailSenderServiceTest.py
├── .github/workflows/                 # GitHub Actions workflows
├── logs/                              # Application logs
├── requirements.txt                   # Python dependencies
├── run.cmd                           # Windows batch runner
└── README.md                         # Project documentation
```

## Testing

Run the complete test suite:

```bash
python -m pytest src/test/ -v
```

Test individual components:

```bash
python -m pytest src/test/ScraperServiceTest.py -v
python -m pytest src/test/StatisticsServiceTest.py -v
python -m pytest src/test/EmailFormatServiceTest.py -v
python -m pytest src/test/EmailSenderServiceTest.py -v
python -m pytest src/test/ConfigLoaderTest.py -v
```

## Core Components

### 1. Data Collection

- **ScraperService**: Extracts job offers from configured websites
- **JobOffer Model**: Structured data representation
- **Supabase Integration**: Persistent storage with duplicate detection

### 2. Data Analysis

- **StatisticsService**:
  - Position type categorization with Polish keywords
  - Salary analysis (range parsing, averages, medians)
  - Market trend analysis

### 3. User Interfaces

- **CLI Application** (`main.py`): Automated scraping and email reporting
- **GUI Application** (`GUI.py`):
  - Interactive data exploration
  - Statistical visualizations with matplotlib
  - Modern dark theme with CustomTkinter

### 4. Automation & Reporting

- **Email Integration**: Formatted reports with new job offers
- **GitHub Actions**: Scheduled daily execution
- **Logging**: Comprehensive logging for monitoring and debugging

## Automation

The project includes automated execution via GitHub Actions:

**Job Scraper Scheduler** (`.github/workflows/job-scraper.yml`)

- Runs daily at 8:00 AM UTC (10:00 AM CET)
- Executes the full scraping and email sending process
- Can be triggered manually via workflow_dispatch
- Automatically uploads logs as artifacts for 30 days retention
- Supports all required environment variables via GitHub Secrets

## GUI Application Features

The desktop application (`src/main/GUI.py`) provides:

- **Modern Interface**: Dark theme with CustomTkinter
- **Data Visualization**: Interactive job offer browsing
- **Statistics Display**: Real-time job market analytics
- **Charts & Graphs**: Matplotlib integration for visual analysis
- **Filtering Options**: Browse offers by various criteria
- **Database Integration**: Direct access to stored job data

## Statistics & Analytics

The `StatisticsService` provides comprehensive analysis:

### Position Type Analysis

- Automatic categorization using Polish keywords
- Categories include: Sprzedawca/Konsultant, Gastronomia, Recepcjonista, Medyczny, etc.
- Custom keyword support for flexible categorization

### Salary Analysis

- Polish salary format parsing (e.g., "30,50 - 33 zł / godz. brutto")
- Statistical calculations: average, median, min/max
- Range detection and processing
- Hourly rate analysis optimized for student jobs

## Monitoring & Logging

- **GitHub Actions**: View execution logs in the Actions tab
- **Email reports**: Receive formatted job offers with only new entries
- **Log files**: Detailed logs stored in `logs/` directory with daily rotation
- **Database tracking**: Automatic duplicate detection and prevention
- **Artifacts**: GitHub Actions automatically uploads logs for 30 days retention
- **Error handling**: Comprehensive error logging and graceful failure handling

## Dependencies

The project uses the following key dependencies:

```python
beautifulsoup4==4.13.4     # Web scraping and HTML parsing
requests==2.32.3           # HTTP requests for web scraping
python-dotenv==1.1.0       # Environment variable management
PyYAML==6.0.2              # YAML configuration file parsing
lxml==5.4.0                # XML/HTML processing
customtkinter==5.2.2       # Modern GUI components
psycopg2==2.9.10           # PostgreSQL database adapter
supabase==2.15.2           # Supabase client for database operations
matplotlib==3.10.3         # Data visualization and charts
```

## Customization

### Adding New Job Sites

1. Update `src/resources/config.yml` with new site configuration:

   ```yaml
   - id: new-site
     url: "https://example-job-site.com/jobs"
     selectors:
       offersContainer: "div.jobs-container"
       offerBox: "div.job-card"
       title: "h2.job-title"
       company: ".company-name"
       location: ".job-location"
       salary: ".salary-info"
       url: "a.job-link"
   ```

2. Test selectors using browser developer tools
3. Run the scraper to verify data extraction
4. Add unit tests for the new site

### Modifying Email Format

Edit `src/main/service/EmailFormatService.py` to customize:

- Email body structure and HTML formatting
- Subject line format and content
- New job offer filtering logic
- Email template styling

### Customizing Statistics

Modify `src/main/service/StatisticsService.py` to:

- Add new position categories
- Customize Polish keyword matching
- Implement additional salary analysis metrics
- Create custom data aggregations

### Changing Automation Schedule

Modify the cron expression in `.github/workflows/job-scraper.yml`:

```yaml
schedule:
  - cron: "0 8 * * *" # Daily at 8:00 AM UTC
  # Examples:
  # - cron: "0 */6 * * *"    # Every 6 hours
  # - cron: "0 9 * * 1-5"    # Weekdays at 9 AM
```

## Database Schema

The application uses a PostgreSQL database with the following structure:

```sql
CREATE TABLE job_offers (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    company VARCHAR(255),
    location VARCHAR(255),
    salary VARCHAR(255),
    url VARCHAR(500) UNIQUE,
    site_id VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    additional_info TEXT
);
```

## Usage Examples

### Running Different Modes

**1. Full Automation (Scrape + Store + Email):**

```bash
python -m src.main.main
```

**2. GUI Mode for Data Analysis:**

```bash
python -m src.main.GUI
```

**3. Windows Batch Execution:**

```cmd
run.cmd
```

### Testing Specific Components

**Test scraping functionality:**

```bash
python -m pytest src/test/ScraperServiceTest.py::TestScraperService::test_scrape_first_few_offers_all_sites -v
```

**Test statistics generation:**

```bash
python -m pytest src/test/StatisticsServiceTest.py::TestStatisticsService::test_get_salary_statistics -v
python -m pytest src/test/StatisticsServiceTest.py::TestStatisticsService::test_get_position_type_counts_default_polish_keywords -v
```

**Test email formatting:**

```bash
python -m pytest src/test/EmailFormatServiceTest.py::TestEmailFormatService::test_format_email_with_multiple_offers -v
python -m pytest src/test/EmailFormatServiceTest.py::TestEmailFormatService::test_format_email_subject_with_offers -v
```

**Test email sending:**

```bash
python -m pytest src/test/EmailSenderServiceTest.py::TestEmailSenderService::test_email_service_configuration -v
```

**Test configuration loading:**

```bash
python -m pytest src/test/ConfigLoaderTest.py::TestConfigLoader::test_load_config_success -v
```

## Troubleshooting

### Common Issues

1. **Database Connection Errors**

   - Verify Supabase credentials in `.env`
   - Check network connectivity
   - Ensure database exists and is accessible

2. **Scraping Failures**

   - Website structure may have changed
   - Update selectors in `config.yml`
   - Check for anti-bot measures

3. **Email Sending Issues**

   - Use Gmail App Passwords, not regular passwords
   - Verify SMTP settings
   - Check spam folders for test emails

4. **GUI Not Loading**
   - Ensure CustomTkinter is properly installed
   - Check for display/graphics driver issues
   - Verify database connectivity

### Log Analysis

Logs are stored in the `logs/` directory with daily rotation:

- Format: `YYYY-MM-DD.log`
- Levels: INFO, DEBUG, WARNING, ERROR
- Automatic cleanup after 30 days in GitHub Actions

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass (`python -m pytest src/test/ -v`)
6. Update documentation if needed
7. Commit your changes (`git commit -m 'Add amazing feature'`)
8. Push to the branch (`git push origin feature/amazing-feature`)
9. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Add type hints for new functions
- Include comprehensive error handling
- Write unit tests for new features
- Update README for significant changes
- Use meaningful commit messages

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Security & Best Practices

- **Environment Variables**: Use `.env` for local development, GitHub Secrets for CI/CD
- **Database Security**: Never commit database credentials
- **Email Security**: Use Gmail App Passwords for authentication
- **Dependencies**: Regularly update packages for security patches
- **Error Handling**: Graceful failure handling prevents data loss
- **Logging**: Sensitive information is never logged
- **Rate Limiting**: Respectful scraping practices to avoid IP blocking

---

**Note**: Replace `YOUR_USERNAME` in the badge URLs with your actual GitHub username before deploying.
