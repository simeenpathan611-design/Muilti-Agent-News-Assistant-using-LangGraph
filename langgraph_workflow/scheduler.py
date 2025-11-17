# langgraph_workflow/scheduler.py
# Runs the full newsletter workflow automatically on a schedule
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from time import sleep
from langgraph_workflow.graph_definition import run_newsletter_workflow
from utils.logger import setup_logger

logger = setup_logger("scheduler")

def job():
    """Job to run the complete newsletter workflow."""
    logger.info("🕒 Scheduled job triggered.")
    try:
        result = run_newsletter_workflow()
        logger.info(f"✅ Workflow completed successfully at {datetime.now()}")
        logger.info(f"Result: {result}")
    except Exception as e:
        logger.error(f"❌ Error during scheduled run: {e}")

def start_scheduler(run_now=True):
    """Starts the scheduler for daily execution.

    Args:
        run_now (bool): If True, run the job once immediately after starting the scheduler.
                        Default True to enable quick testing.
    """
    scheduler = BackgroundScheduler()

    # Schedule the job at 9:00 AM every day (you can change this time)
    scheduler.add_job(job, 'cron', hour=9, minute=0)

    scheduler.start()
    logger.info("🗓️ Scheduler started. Job will run every day at 9:00 AM.")

    if run_now:
        logger.info("⚡ Running initial workflow immediately (run_now=True)...")
        job()

    try:
        # Keep the process alive so the background scheduler can run jobs
        while True:
            sleep(60)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        logger.info("🛑 Scheduler stopped manually.")

# Allow `python -m langgraph_workflow.scheduler` to start scheduler
if __name__ == "__main__":
    # By default we want to run immediately for testing
    start_scheduler(run_now=True)
