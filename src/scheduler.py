"""
Scheduling module for automatic news updates
"""

import asyncio
import schedule
import time
import logging
from datetime import datetime, timedelta
from threading import Thread
from typing import List, Callable

from .config import Config
from .news_aggregator import NewsAggregator


class NewsScheduler:
    """Scheduler for automatic news updates"""
    
    def __init__(self, config: Config):
        self.config = config
        self.aggregator = NewsAggregator(config)
        self.is_running = False
        self.scheduler_thread = None
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
    
    def setup_schedule(self):
        """Setup scheduled tasks based on configuration"""
        
        # Clear any existing jobs
        schedule.clear()
        
        # Get fetch times from config
        fetch_times = self.config.config_data.get('schedule', {}).get('fetch_times', ['06:00', '12:00', '18:00'])
        
        # Schedule news updates
        for fetch_time in fetch_times:
            schedule.every().day.at(fetch_time).do(self._scheduled_update)
            self.logger.info(f"Scheduled news update at {fetch_time}")
        
        # Schedule cleanup task (daily at midnight)
        schedule.every().day.at("00:00").do(self._cleanup_old_cache)
        self.logger.info("Scheduled cache cleanup at midnight")
    
    def _scheduled_update(self):
        """Execute scheduled news update"""
        try:
            self.logger.info("Starting scheduled news update")
            
            # Run async update in sync context
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            articles = loop.run_until_complete(self.aggregator.update_news())
            
            loop.close()
            
            self.logger.info(f"Scheduled update completed: {len(articles)} articles fetched")
            
        except Exception as e:
            self.logger.error(f"Scheduled update failed: {str(e)}")
    
    def _cleanup_old_cache(self):
        """Clean up old cached files"""
        try:
            from pathlib import Path
            import os
            
            cache_dir = Path(self.config.cache_dir)
            retention_days = self.config.cache_retention_days
            cutoff_date = datetime.now() - timedelta(days=retention_days)
            
            cleaned_count = 0
            
            for cache_file in cache_dir.glob("articles_*.json"):
                try:
                    # Extract date from filename
                    date_str = cache_file.stem.split('_')[1]  # articles_YYYYMMDD.json
                    file_date = datetime.strptime(date_str, '%Y%m%d')
                    
                    if file_date < cutoff_date:
                        os.remove(cache_file)
                        cleaned_count += 1
                        self.logger.info(f"Removed old cache file: {cache_file}")
                        
                except (ValueError, IndexError) as e:
                    self.logger.warning(f"Could not parse date from cache file {cache_file}: {e}")
            
            self.logger.info(f"Cache cleanup completed: {cleaned_count} files removed")
            
        except Exception as e:
            self.logger.error(f"Cache cleanup failed: {str(e)}")
    
    def start(self):
        """Start the scheduler"""
        if self.is_running:
            self.logger.warning("Scheduler is already running")
            return
        
        self.setup_schedule()
        self.is_running = True
        
        # Start scheduler in a separate thread
        self.scheduler_thread = Thread(target=self._run_scheduler, daemon=True)
        self.scheduler_thread.start()
        
        self.logger.info("News scheduler started")
    
    def stop(self):
        """Stop the scheduler"""
        self.is_running = False
        schedule.clear()
        
        if self.scheduler_thread and self.scheduler_thread.is_alive():
            self.scheduler_thread.join(timeout=5)
        
        self.logger.info("News scheduler stopped")
    
    def _run_scheduler(self):
        """Run the scheduler loop"""
        while self.is_running:
            try:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
            except Exception as e:
                self.logger.error(f"Scheduler error: {str(e)}")
                time.sleep(60)  # Continue after error
    
    def get_next_run_times(self) -> List[str]:
        """Get next scheduled run times"""
        jobs = schedule.get_jobs()
        next_runs = []
        
        for job in jobs:
            if job.next_run:
                next_runs.append({
                    'job': str(job.job_func.__name__),
                    'next_run': job.next_run.strftime('%Y-%m-%d %H:%M:%S')
                })
        
        return next_runs
    
    def force_update(self):
        """Force an immediate news update"""
        self.logger.info("Force updating news")
        self._scheduled_update()
    
    def get_status(self) -> dict:
        """Get scheduler status"""
        return {
            'is_running': self.is_running,
            'scheduled_jobs': len(schedule.get_jobs()),
            'next_runs': self.get_next_run_times(),
            'last_update': self._get_last_update_time()
        }
    
    def _get_last_update_time(self) -> str:
        """Get the time of the last cache update"""
        try:
            from pathlib import Path
            
            cache_dir = Path(self.config.cache_dir)
            today_cache = cache_dir / f"articles_{datetime.now().strftime('%Y%m%d')}.json"
            
            if today_cache.exists():
                mod_time = datetime.fromtimestamp(today_cache.stat().st_mtime)
                return mod_time.strftime('%Y-%m-%d %H:%M:%S')
            else:
                return "Never"
                
        except Exception:
            return "Unknown"


def run_daemon():
    """Run the scheduler as a daemon"""
    import signal
    import sys
    
    # Setup logging for daemon mode
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/scheduler.log'),
            logging.StreamHandler()
        ]
    )
    
    config = Config()
    scheduler = NewsScheduler(config)
    
    def signal_handler(signum, frame):
        print("Received signal to stop scheduler")
        scheduler.stop()
        sys.exit(0)
    
    # Handle shutdown signals
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        print("Starting news scheduler daemon...")
        print("Press Ctrl+C to stop")
        
        scheduler.start()
        
        # Keep the main thread alive
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("Stopping scheduler...")
        scheduler.stop()


if __name__ == "__main__":
    run_daemon()