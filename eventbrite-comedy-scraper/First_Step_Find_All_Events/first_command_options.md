# Eventbrite Find Events Scraper Commands

This guide covers the commands for the first step of the scraping process, which discovers event links from Eventbrite search results.

## Basic Usage

```bash
python First_Step_Find_All_Events/Run_This_First_To_Find_Events.py [options]
```

## Common Scenarios

### Search a Small Number of Pages (~5 pages)

```bash
python First_Step_Find_All_Events/Run_This_First_To_Find_Events.py --start 1 --end 5 --delay 3
```

Best practices:
- Use moderate delay (3-4 seconds)
- Default options are usually fine for small searches
- Run during off-peak hours if possible
- Set reasonable retry count (1-2)

### Search a Large Number of Pages (~20+ pages)

```bash
python First_Step_Find_All_Events/Run_This_First_To_Find_Events.py --start 1 --end 10 --delay 5 --retry 2
```

Then continue with subsequent ranges:

```bash
python First_Step_Find_All_Events/Run_This_First_To_Find_Events.py --start 11 --end 20 --delay 5 --retry 2
```

Best practices:
- Break search into multiple smaller ranges
- Use longer delays (5-7 seconds)
- Increase retry count to handle timeouts
- Wait 20-30 minutes between search batches
- Use headless mode for extended searching
- Consider different time periods instead of many pages

### Very Large Search with Different Geographic Areas

For very large searches, divide by location rather than just pages:

```bash
# First search Toronto
python First_Step_Find_All_Events/Run_This_First_To_Find_Events.py --base-url "https://www.eventbrite.ca/d/canada--toronto/stand-up-comedy/" --start 1 --end 10 --delay 5

# Then search Ottawa
python First_Step_Find_All_Events/Run_This_First_To_Find_Events.py --base-url "https://www.eventbrite.ca/d/canada--ottawa/stand-up-comedy/" --start 1 --end 10 --delay 5

# Then search Vancouver
python First_Step_Find_All_Events/Run_This_First_To_Find_Events.py --base-url "https://www.eventbrite.ca/d/canada--vancouver/stand-up-comedy/" --start 1 --end 10 --delay 5
```

## All Command Options

| Option | Description | Default |
|--------|-------------|---------|
| `--start` | Start page number | 1 |
| `--end` | End page number | 3 |
| `--base-url` | Base URL to search | From Main_Settings.py |
| `--headless` | Run browser in headless mode | False |
| `--retry` | Number of retries per page | 1 |
| `--browser` | Browser to use (chrome, firefox) | chrome |
| `--delay` | Delay in seconds between requests | 5 |

## Additional Tips for Successful Event Discovery

1. **Search Strategies:**
   - Search by geographic area rather than deep pages
   - Consider different event categories to find more events
   - Searching for specific venues can yield better results

2. **Changing Search Terms:**
   - Try different variations: "stand-up comedy", "comedy show", "comedy night"
   - Include specific comedians' names for niche events
   - Search by venue names known for comedy

3. **Timing Tips:**
   - Run searches weekly to catch new events
   - Weekend searches often yield more upcoming events
   - New events are typically posted at the beginning of the month

4. **Handling Search Results:**
   - Each search creates a new CSV file with a timestamp
   - Merge multiple searches using the merge feature in the Data_Organizer
   - Remove duplicates when combining multiple search results

5. **If Searches Are Blocked:**
   - Try a different browser (Firefox instead of Chrome)
   - Use longer delays between requests
   - Rotate IP addresses if possible
   - Change user agent strings

6. **Command for Merging Results:**
   ```bash
   # Create a script to use the merge function
   python -c "from Shared_Tools_Both_Steps_Use.Data_Organizer import merge_csv_files; merge_csv_files(['file1.csv', 'file2.csv'], 'merged_output.csv', 'event_link')"
   ```

7. **Finding the Most Events:**
   - Search by multiple cities in separate runs
   - Search different date ranges
   - Use shorter search intervals (less pages per run)
   - Try different search terms for comedy events