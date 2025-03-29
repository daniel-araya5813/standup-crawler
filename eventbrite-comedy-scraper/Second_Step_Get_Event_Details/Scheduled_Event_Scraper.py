def save_progress_report(total_links, links_remaining, output_file, run_date, runtime_seconds=None):
    """Save a progress report to a dedicated reports folder."""
    ensure_directory_exists("Reports")
    
    # Calculate completion metrics
    completed_links = total_links - len(links_remaining)
    completion_percentage = (completed_links / total_links) * 100 if total_links > 0 else 0
    
    # Generate report filename
    if links_remaining:
        status = "partial"
    else:
        status = "complete"
    
    report_file = f"Reports/scraper_report_{run_date}_{status}.txt"
    
    # Prepare report content
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("=" * 50 + "\n")
        f.write(f"EVENTBRITE SCRAPER PROGRESS REPORT\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Report time: {current_time}\n")
        f.write(f"Run started: {datetime.strptime(run_date, '%Y-%m-%d_%H-%M-%S').strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        if runtime_seconds:
            hours = runtime_seconds // 3600
            minutes = (runtime_seconds % 3600) // 60
            seconds = runtime_seconds % 60
            f.write(f"Total runtime: {hours}h {minutes}m {seconds}s\n")
        
        f.write("\n")
        f.write(f"Total links: {total_links}\n")
        f.write(f"Completed: {completed_links} ({completion_percentage:.2f}%)\n")
        f.write(f"Remaining: {len(links_remaining)}\n")
        f.write(f"Output file: {output_file}\n\n")
        
        if links_remaining:
            f.write("STATUS: PAUSED/INTERRUPTED\n")
            f.write("To resume, run with --resume flag\n")
        else:
            f.write("STATUS: COMPLETED\n")
            f.write("All links have been successfully processed\n")
        
        f.write("\n" + "=" * 50 + "\n")
    
    logging.info(f"📝 Progress report saved to {report_file}")
    return report_filedef parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Scheduled event scraper with anti-detection")
    parser.add_argument("input_csv", nargs="?", type=str, help="Name or path to input CSV file with event links")
    parser.add_argument("--output", type=str, help="Path to output CSV file for event details")
    parser.add_argument("--batch-size", type=int, default=3, help="Number of links to process per browser session")
    parser.add_argument("--min-delay", type=float, default=3.0, help="Minimum delay between requests in seconds")
    parser.add_argument("--max-delay", type=float, default=7.0, help="Maximum delay between requests in seconds")
    parser.add_argument("--links-per-session", type=int, default=50, 
                        help="Number of links to process before taking a long break")
    parser.add_argument("--min-break", type=int, default=30, help="Minimum break time in minutes")
    parser.add_argument("--max-break", type=int, default=60, help="Maximum break time in minutes")
    parser.add_argument("--sessions-per-day", type=int, default=3, 
                        help="Maximum number of sessions to run per day")
    parser.add_argument("--resume", action="store_true", help="Resume from previous state")
    parser.add_argument("--report-interval", type=int, default=10, 
                        help="How often to report progress (in minutes)")
    return parser.parse_args()