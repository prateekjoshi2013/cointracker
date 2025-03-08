from celery import shared_task
from celery.contrib.abortable import AbortableTask
from celery.exceptions import SoftTimeLimitExceeded,Ignore
from config import REDIS_HOST,REDIS_PORT,REDIS_DB
from time import sleep,time
import redis
from random import randint


# from extensions import db
# from models import User

# Initialize Redis connection (Ensure Redis is running on the same machine or use your Redis instance URL)
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

LOCK_NAME = "sync_task_lock"
LOCK_TIMEOUT = 300  # Lock timeout of 5 minutes


@shared_task(bind=True)
def sync_tx_data(self):
    """
    Task to sync data from a paginated, rate-limited API to the database.
    Ensures only one instance runs at a time with a minimum 5-minute gap between runs.
    """
    print("Starting sync task...")

    # Check if the task is already locked
    if r.get(LOCK_NAME):
        print(f"Another sync task:{sync_tx_data.request.id} is already running. Skipping this run.")
        raise Ignore()  # Ignore this task run since it's already running

    # Set a lock to prevent other tasks from running
    r.setex(LOCK_NAME, LOCK_TIMEOUT, "locked")
    start_time = time()  # Track the start time
    try:
        base_url = "https://example.com/api/data"
        page = 1
        has_more_data = True

        while has_more_data:
            response = requests.get(f"{base_url}?page={page}")
            
            if response.status_code == 429:
                print("Rate limit hit! Waiting before retrying...")
                time.sleep(60)  # Wait for rate limit reset
                continue
            
            data = response.json()
            # Process & save data in DB (implement your logic)
            
            if not data.get("next_page"):
                has_more_data = False
            else:
                page += 1
                    Check if task execution time exceeds the timeout
        if time() - start_time > LOCK_TIMEOUT:
            print("Task timeout reached! Stopping execution.")
            raise SoftTimeLimitExceeded("Task exceeded the time limit")  # Raise exception to stop execution

        print(f"Sync task:{sync_tx_data.request.id} started!")
        sleep(randint(300,350))
        print(f"Sync task:{sync_tx_data.request.id} finished!")
    finally:
        # Release the lock after the task is done
        r.delete(LOCK_NAME)

    return "Completed"