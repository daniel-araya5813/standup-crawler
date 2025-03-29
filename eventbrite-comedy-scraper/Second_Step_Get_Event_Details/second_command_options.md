# Eventbrite Event Details Scraper Commands

This guide covers the commands for the second step of the scraping process, which collects detailed information from event pages. There are two scripts available:

1. `Run_This_Second_To_Get_Event_Details.py` - Basic scraper with anti-detection
2. `Scheduled_Event_Scraper.py` - Advanced scheduled scraper with extensive anti-detection

## Standard Event Details Scraper

### Basic Usage

```bash
python Run_This_Second_To_Get_Event_Details.py [input_csv] [options]
```

### Common Scenarios

#### Process a Small Number of Links (~60)

```bash
python Run_This_Second_To_Get_Event_Details.py event_links.csv --batch-size 5 --delay 4
```

Best practices:
- Use a reasonable batch size (5-8)
- Add moderate delay (3-5 seconds)
- Run during off-peak hours if possible
- Monitor the first few requests to confirm everything is working

#### Process a Large Number of Links (~500)

```bash
python Run_This_Second_To_Get_Event_Details.py event_links.csv --batch-size 3 --delay 5 --max-links 50
```

Best practices:
- Use smaller batches (2-4)
- Use longer delays (5-7 seconds)
- Process in chunks with `--max-links` and `--start-index`
- Wait 1-2 hours between chunks
- Run commands to process in intervals:

```bash
# First 50 links
python Run_This_Second_To_Get_Event_Details.py event_links.csv --batch-size 3 --delay 5 --max-links 50
# Wait 1-2 hours
# Next 50 links
python Run_This_Second_To_Get_Event_Details.py event_links.csv --batch-size 3 --delay 5 --max-links 50 --start-index 50
```

### All Command Options

| Option | Description | Default |
|--------|-------------|---------|
| `input_csv` | Name or path to CSV file with event links | Most recent event_links file |
| `--output` | Path to output CSV file | `Collected_Data/Complete_Event_Descriptions/detailed_events_[timestamp].csv` |
| `--start-index` | Starting index in the links list (for resuming) | 0 |
| `--max-links` | Maximum number of links to process (0 for all) | 0 |
| `--delay` | Delay between requests in seconds | 2 |
| `--batch-size` | Number of links to process per browser session | 8 |
| `--headless` | Run browser in headless mode | True |

## Advanced Scheduled Scraper

The `Scheduled_Event_Scraper.py` script provides automated scheduling and extensive anti-detection measures.

### Basic Usage

```bash
python Scheduled_Event_Scraper.py [input_csv] [options]
```

### Common Scenarios

#### Process a Small Number of Links (~60)

```bash
python Scheduled_Event_Scraper.py event_links.csv --batch-size 3 --links-per-session 20 --sessions-per-day 3
```

Best practices:
- Set `links-per-session` to spread out the scraping
- Allow multiple sessions per day for faster completion
- Keep batch size at 3 for better anti-detection
- Use default delays (3-7 seconds)

#### Process a Large Number of Links (~500)

```bash
python Scheduled_Event_Scraper.py event_links.csv --batch-size 3 --min-delay 4 --max-delay 8 --links-per-session 30 --sessions-per-day 2 --min-break 45 --max-break 90
```

Best practices:
- Limit to 2 sessions per day
- Use longer breaks between sessions (45-90 minutes)
- Process fewer links per session
- Increase minimum delay between requests
- Let the script run for multiple days
- If interrupted, use `--resume` to continue

#### Ultra-Safe Approach for High-Traffic Sites (~1000+ links)

```bash
python Scheduled_Event_Scraper.py event_links.csv --batch-size 2 --min-delay 6 --max-delay 12 --links-per-session 20 --sessions-per-day 1 --min-break 60 --max-break 120
```

Best practices:
- Only 1 session per day
- Very small batch size (2)
- Long delays between requests (6-12 seconds)
- Long breaks between sessions (1-2 hours)
- Different IP addresses if possible (VPN rotation)
- Run during different times of day

### All Command Options

| Option | Description | Default |
|--------|-------------|---------|
| `input_csv` | Name or path to CSV file with event links | Most recent event_links file |
| `--output` | Path to output CSV file | `Collected_Data/Complete_Event_Descriptions/detailed_events_[timestamp].csv` |
| `--batch-size` | Number of links to process per browser session | 3 |
| `--min-delay` | Minimum delay between requests (seconds) | 3.0 |
| `--max-delay` | Maximum delay between requests (seconds) | 7.0 |
| `--links-per-session` | Links to process before taking a long break | 50 |
| `--min-break` | Minimum break time (minutes) | 30 |
| `--max-break` | Maximum break time (minutes) | 60 |
| `--sessions-per-day` | Maximum number of sessions to run per day | 3 |
| `--resume` | Resume from previous state | - |
| `--report-interval` | How often to report progress (minutes) | 10 |

## Additional Tips for Successful Scraping

1. **Monitor the logs:**
   - Check `Logs/detail_collector_*.log` regularly
   - Look for any patterns in errors or timeouts

2. **Use different computers/networks:**
   - Rotate between different networks if scraping large numbers
   - Consider using a VPN with rotating IPs

3. **Timing considerations:**
   - Late night/early morning hours have less traffic and monitoring
   - Weekends may have different traffic patterns
   - Avoid scraping during peak business hours

4. **Handling failure:**
   - If you encounter blocks, wait 24 hours before trying again
   - Consider using more conservative settings if blocked

5. **Resources:**
   - Ensure your computer won't go to sleep during long runs
   - Keep laptop plugged in for extended scraping sessions
   - For the scheduled scraper, the state is saved automatically