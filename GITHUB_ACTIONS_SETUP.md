# GitHub Actions Job Scraper Setup

This project uses GitHub Actions to automatically run the job scraper on a schedule.

## Setup Instructions

### 1. Repository Secrets

You need to configure the following secrets in your GitHub repository:

1. Go to your repository on GitHub
2. Click on **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret** and add each of the following:

| Secret Name       | Description                                        | Example Value                               |
| ----------------- | -------------------------------------------------- | ------------------------------------------- |
| `FROM_EMAIL`      | The Gmail address to send emails from              | `your-email@gmail.com`                      |
| `EMAIL_PASSWORD`  | App password for Gmail (NOT your regular password) | `abcd efgh ijkl mnop`                       |
| `TO_EMAILS`       | Comma-separated list of recipient emails           | `recipient1@gmail.com,recipient2@gmail.com` |
| `SMTP_SERVER`     | SMTP server for sending emails                     | `smtp.gmail.com`                            |
| `SMTP_PORT`       | SMTP port number                                   | `587`                                       |
| `DEFAULT_SUBJECT` | Default email subject                              | `Daily Job Offer Report`                    |

### 2. Gmail App Password Setup

For security, you should use a Gmail App Password instead of your regular password:

1. Enable 2-Factor Authentication on your Gmail account
2. Go to Google Account settings → Security → 2-Step Verification → App passwords
3. Generate a new app password for "Mail"
4. Use this 16-character password as your `EMAIL_PASSWORD` secret

### 3. Workflow Configuration

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

### 4. Cron Schedule Examples

| Schedule                     | Cron Expression | Description         |
| ---------------------------- | --------------- | ------------------- |
| Every day at 8 AM UTC        | `0 8 * * *`     | Current setting     |
| Twice daily (8 AM, 6 PM UTC) | `0 8,18 * * *`  | Morning and evening |
| Weekdays only at 9 AM UTC    | `0 9 * * 1-5`   | Monday to Friday    |
| Every 6 hours                | `0 */6 * * *`   | 4 times per day     |

### 5. Manual Triggering

You can manually trigger the scraper:

1. Go to your repository on GitHub
2. Click **Actions** tab
3. Select **Job Scraper Scheduler** workflow
4. Click **Run workflow** → **Run workflow**

### 6. Monitoring

- **Logs**: Check the Actions tab for execution logs
- **Artifacts**: Log files are automatically uploaded and stored for 30 days
- **Email notifications**: You'll receive scraped job offers via email

### 7. Testing

The repository includes a test workflow that:

- Runs on every push/pull request
- Tests all components without sending emails
- Ensures the scraper works across Python 3.11 and 3.12

### 8. Customization

To modify what gets scraped:

1. Edit `resources/config.yml` to add/remove job sites
2. Update selectors if websites change their structure
3. Modify email format in `EmailFormatService.py`

### Security Notes

- Never commit actual email credentials to the repository
- Use GitHub Secrets for all sensitive information
- The `.env` file is created dynamically during workflow execution
- Consider using environment-specific configurations for production

### Troubleshooting

| Issue               | Solution                                                      |
| ------------------- | ------------------------------------------------------------- |
| Emails not sending  | Check EMAIL_PASSWORD is an app password, not regular password |
| No job offers found | Website structure may have changed - update selectors         |
| Workflow fails      | Check logs in Actions tab, verify all secrets are set         |
| Wrong timezone      | Adjust cron schedule - GitHub Actions uses UTC                |
