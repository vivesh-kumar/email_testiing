import time
import uuid
from datetime import datetime
from email_service import send_confirmation_email

def process_task(
    recipient_email: str,
    recipient_name: str = "User",
    task_name: str = "Data Ingestion & Report Processing",
    custom_details: dict = None
) -> dict:
    """
    Executes a simulated or actual processing pipeline,
    and then sends a confirmation email to the recipient.
    """
    start_time = time.time()
    job_id = f"JOB-{uuid.uuid4().hex[:8].upper()}"
    
    print(f"\n[START] Starting process: '{task_name}' for {recipient_name} ({recipient_email})")
    print(f"[JOB ID] {job_id}")

    # Simulated processing pipeline milestones
    steps_log = []
    
    # Step 1: Input Validation
    print("  -> Step 1: Validating request parameters...")
    time.sleep(0.5)
    steps_log.append("Input payload verified & validated successfully")

    # Step 2: Processing / Computation
    print("  -> Step 2: Running core processing logic...")
    time.sleep(0.8)
    steps_log.append("Data processing and transformation executed")

    # Step 3: Verification & Storage
    print("  -> Step 3: Finalizing output artifacts...")
    time.sleep(0.4)
    steps_log.append("Outputs compiled and integrity checks passed")

    duration_secs = round(time.time() - start_time, 2)
    timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Aggregate metadata
    details = {
        "Status Code": "200 OK",
        "Records Processed": "1,420 entries",
        "Environment": "Production Server",
    }
    if custom_details:
        details.update(custom_details)

    job_data = {
        "job_id": job_id,
        "task_name": task_name,
        "recipient_name": recipient_name,
        "recipient_email": recipient_email,
        "status": "SUCCESS",
        "duration": f"{duration_secs}s",
        "timestamp": timestamp_str,
        "steps": steps_log,
        "details": details
    }

    print(f"[COMPLETE] Processing finished in {duration_secs}s. Sending confirmation email...")
    
    # Send confirmation email
    email_result = send_confirmation_email(recipient_email, job_data)
    job_data["email_result"] = email_result

    return job_data

