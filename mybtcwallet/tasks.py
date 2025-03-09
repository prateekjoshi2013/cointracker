from celery import shared_task
from celery.exceptions import SoftTimeLimitExceeded,Ignore
from sqlalchemy import func
from config import REDIS_HOST,REDIS_PORT,REDIS_DB
from time import sleep,time
import redis
from random import randint
from extensions import db
from models import Address,Transaction,generate_uuid
from client.blockchain import addresses_balance, addresses_rawaddr
import math

# Initialize Redis connection (Ensure Redis is running on the same machine or use your Redis instance URL)
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

LOCK_NAME = "sync_task_lock"
LOCK_TIMEOUT = 300  # Lock timeout of 5 minutes
BATCH_SIZE = 50

def find_unsynced_addresses():
    records = db.session.query(Address).with_entities(Address.address, Address.id).all()
    db_counts = db.session.query(
        Transaction.address_id, 
        func.max(Transaction.timestamp).label('latest_timestamp'),
        func.count(Transaction.id).label('transaction_count')
    ).group_by(Transaction.address_id).all()
    addresses_address_to_id,addresses_id_to_address,db_count_map,db_tx_map=dict(),dict(),dict(),dict()
    addresses_address_to_id ={ addr:id for addr,id in records }
    addresses_id_to_address ={ id:addr for addr,id in records }
    addresses_balances = addresses_balance(list(addresses_address_to_id.keys()))
    for id,timestamp,tx_count in db_counts:
        db_tx_map[id]={
            "last_synced_ts": timestamp,
            "synced_tx_count": tx_count,
        }

    for address,id in addresses_address_to_id.items():
        db_count_map[address]={
            "id": id,
            "curr_balance": addresses_balances[address]['final_balance'],
            "synced_tx_count": 0 if id not in db_tx_map else db_tx_map[id]['synced_tx_count'],
            "last_synced_ts": 0 if id not in db_tx_map else db_tx_map[id]['last_synced_ts'],
            "total_tx_count": addresses_balances[address]['n_tx'],
        }
    
    addresses_to_sync = { id:data for id,data in db_count_map.items() if data['total_tx_count']-data['synced_tx_count']  }
    return addresses_to_sync
    # Iterate through the results and print the address_id, latest timestamp, and transaction count
    # for address_id, latest_timestamp, transaction_count in results:
    #     if transaction_count 
        

def insert_in_batches(records, batch_size=1000):
    """
    Insert records into the database in batches to avoid lock contention.
    """
    # Iterate over records in batches
    for i in range(0, len(records), batch_size):
        batch = records[i : i + batch_size]
        
        # Insert the batch of records
        db.session.bulk_insert_mappings(Transaction, batch)
        
        # Commit the changes to the database
        db.session.commit()


@shared_task(bind=True)
def sync_tx_data(self):
    """
    Task to sync data from a paginated, rate-limited API to the database.
    Ensures only one instance runs at a time with a minimum 5-minute gap between runs.
    """
    

    # Check if the task is already locked
    if r.get(LOCK_NAME):
        print(f"Another sync task is already running. Skipping this run.")
        raise Ignore()  # Ignore this task run since it's already running
    

    # Set a lock to prevent other tasks from running
    r.setex(LOCK_NAME, LOCK_TIMEOUT, "locked")
    start_time = time()  # Track the start time
    try:
        print(f"Sync task:{sync_tx_data.request.id} started!")
        addresses_to_sync=find_unsynced_addresses()
        print(addresses_to_sync)
        for address,data in addresses_to_sync.items():
            remaining_tx = data['total_tx_count'] - data['synced_tx_count']
            page_number = math.ceil(remaining_tx / 50)  # Round up to ensure you get the next set of records
            offset = (page_number-1) * 50  # Correct offset calculation
            print("-->",address,offset)
            result=addresses_rawaddr(address,offset=offset)
            # filter out records based on last synced tx timestamp
            txs=[  
                {
                    "id": generate_uuid(),
                    "address_id": data['id'],
                    "from_addresses": [
                        {
                            "addr" : inp["prev_out"]["addr"] if "addr" in inp["prev_out"] else None  ,
                            "value" : inp["prev_out"]["value"] if "value" in inp["prev_out"] else None,
                        }
                        for inp in  tx["inputs"]  
                    ],
                    "to_addresses": [
                        {
                            "addr" :  out["addr"] if "addr" in out else None ,
                            "value" : out["value"] if "value" in out else None,
                        } 
                        for out in tx["out"] 
                    ],
                    "fee": tx["fee"],
                    "result": tx["result"],
                    "balance": tx["balance"],
                    "timestamp": tx["time"],
                    "txid": tx["hash"],
                }
                for tx in result['txs'] if tx["time"] > data['last_synced_ts']
            ]
            insert_in_batches(txs)
        if time() - start_time > LOCK_TIMEOUT:
            print("Task timeout reached! Stopping execution.")
            raise SoftTimeLimitExceeded("Task exceeded the time limit")  # Raise exception to stop execution
        print(f"Sync task:{sync_tx_data.request.id} finished!")
    finally:
        # Fetch latest timestamp for each address_id
        db_counts = db.session.query(
            Transaction.address_id, 
            func.count(Transaction.id).label('transaction_count')
        ).group_by(Transaction.address_id).all()

        # Convert to dictionary format for bulk update
        updates = [
            {"id": address_id, "last_synced_tx": last_synced_tx}
            for address_id, last_synced_tx in db_counts
        ]
        # Perform bulk update
        db.session.bulk_update_mappings(Address, updates)
        db.session.commit()
        # Release the lock after the task is done
        r.delete(LOCK_NAME)

    return "Completed"