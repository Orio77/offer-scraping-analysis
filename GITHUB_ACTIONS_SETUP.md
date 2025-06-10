# GitHub Actions Job Scraper Setup

This project uses GitHub Actions to automatically run the job scraper on a schedule.

## Setup Instructions

### 1. Repository Secrets

You need to configure the following secrets in your GitHub repository:

1. Go to your repository on GitHub
2. Click on **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret** and add each of the following:

#### Email Configuration Secrets

| Secret Name       | Description                                        | Example Value                               |
| ----------------- | -------------------------------------------------- | ------------------------------------------- |
| `FROM_EMAIL`      | The Gmail address to send emails from              | `your-email@gmail.com`                      |
| `GMAIL_PASSWORD`  | App password for Gmail (NOT your regular password) | `abcd efgh ijkl mnop`                       |
| `TO_EMAILS`       | Comma-separated list of recipient emails           | `recipient1@gmail.com,recipient2@gmail.com` |
| `SMTP_SERVER`     | SMTP server for sending emails                     | `smtp.gmail.com`                            |
| `SMTP_PORT`       | SMTP port number                                   | `587`                                       |
| `DEFAULT_SUBJECT` | Default email subject                              | `Daily Job Offer Report`                    |

#### Database Configuration Secrets (Supabase/PostgreSQL)

| Secret Name            | Description                       | Example Value                  |
| ---------------------- | --------------------------------- | ------------------------------ |
| `SUPABASE_URL`         | Your Supabase project URL         | `https://xxx.supabase.co`      |
| `SUPABASE_ANON_KEY`    | Supabase anonymous/public API key | `eyJhbGciOiJIUzI1NiIsInR5c...` |
| `SUPABASE_DB_HOST`     | Database host                     | `db.xxx.supabase.co`           |
| `SUPABASE_DB_NAME`     | Database name                     | `postgres`                     |
| `SUPABASE_DB_USER`     | Database username                 | `postgres`                     |
| `SUPABASE_DB_PASSWORD` | Database password                 | `your-secure-password`         |
| `SUPABASE_DB_PORT`     | Database port                     | `5432`                         |

### 2. Gmail App Password Setup

For security, you should use a Gmail App Password instead of your regular password:

1. Enable 2-Factor Authentication on your Gmail account
2. Go to Google Account settings → Security → 2-Step Verification → App passwords
3. Generate a new app password for "Mail"
4. Use this 16-character password as your `GMAIL_PASSWORD` secret

### 3. Supabase Database Setup

To set up your Supabase database:

1. Create a free account at [supabase.com](https://supabase.com)
2. Create a new project
3. Go to **Settings** → **Database** to find connection details
4. Go to **Settings** → **API** to find your URL and API keys
5. The table will be automatically created when you first run the application

### 4. Local Development Environment

For local development, create a `.env` file in the project root:

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
SUPABASE_DB_NAME=postgres
SUPABASE_DB_USER=postgres
SUPABASE_DB_PASSWORD=your-db-password
SUPABASE_DB_PORT=5432
```

### 5. Workflow Configuration

The scraper is configured to run:

- **Daily at 8:00 AM UTC** (10:00 AM CET during standard time)
- **Manually** via the GitHub Actions tab

You can modify the schedule in `.github/workflows/job-scraper.yml`:

```yaml
on:
  schedule:
    # Modify this cron expression to change the schedule
    - cron: "0 8 * * *" # Daily at 8:00 AM UTC
```

### 6. Cron Schedule Examples

| Schedule                     | Cron Expression | Description         |
| ---------------------------- | --------------- | ------------------- |
| Every day at 8 AM UTC        | `0 8 * * *`     | Current setting     |
| Twice daily (8 AM, 6 PM UTC) | `0 8,18 * * *`  | Morning and evening |
| Weekdays only at 9 AM UTC    | `0 9 * * 1-5`   | Monday to Friday    |
| Every 6 hours                | `0 */6 * * *`   | 4 times per day     |

### 7. Manual Triggering

You can manually trigger the scraper:

1. Go to your repository on GitHub
2. Click **Actions** tab
3. Select **Job Scraper Scheduler** workflow
4. Click **Run workflow** → **Run workflow**

### 8. Monitoring

- **Logs**: Check the Actions tab for execution logs
- **Artifacts**: Log files are automatically uploaded and stored for 30 days
- **Email notifications**: You'll receive scraped job offers via email
- **Database**: Job offers are stored in Supabase with automatic duplicate prevention

### 9. Testing

The repository includes comprehensive unit tests that:

- Test all components without sending actual emails
- Verify database operations and data integrity
- Ensure scraping functionality works correctly
- Run automatically on code changes

Run tests locally:

```bash
python -m pytest src/test/ -v
```

### 10. Customization

To modify what gets scraped:

1. Edit `src/resources/config.yml` to add/remove job sites
2. Update selectors if websites change their structure
3. Modify email format in `src/main/service/EmailFormatService.py`
4. Customize statistics in `src/main/service/StatisticsService.py`

### Security Notes

- Never commit actual credentials to the repository
- Use GitHub Secrets for all sensitive information
- The `.env` file is created dynamically during workflow execution
- Database credentials are encrypted and stored securely
- Consider using environment-specific configurations for production

### Troubleshooting

| Issue                     | Solution                                                      |
| ------------------------- | ------------------------------------------------------------- |
| Emails not sending        | Check GMAIL_PASSWORD is an app password, not regular password |
| Database connection fails | Verify all Supabase secrets are correctly set                 |
| No job offers found       | Website structure may have changed - update selectors         |
| Workflow fails            | Check logs in Actions tab, verify all secrets are set         |
| Wrong timezone            | Adjust cron schedule - GitHub Actions uses UTC                |
| Duplicate job offers      | Database automatically prevents duplicates by URL             |
