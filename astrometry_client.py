import json
import time
import requests

# --- URLs ---
BASE_URL = 'http://nova.astrometry.net/api'
LOGIN_URL = f'{BASE_URL}/login'
UPLOAD_URL = f'{BASE_URL}/upload'


def login(apiKey, prints=True):
    try:
        login_resp = requests.post(
            LOGIN_URL, data={'request-json': json.dumps({"apikey": apiKey})})
        session = json.loads(login_resp.text)['session']

        if prints:
            print(f"[✓] Login successful. Session : {session}")
        return session
    except Exception as e:
        if prints:
            print(f"[X] Fetal error!\n", e)
        return -1


def submit_file(session, file_path, prints=True):
    try:
        files = {'file': open(file_path, 'rb')}
        payload = {'request-json': json.dumps({'session': session})}

        upload_resp = requests.post(UPLOAD_URL, data=payload, files=files)
        upload_json = json.loads(upload_resp.text)

        if upload_json.get('status') != 'success':
            if prints:
                print("[X] Upload failed:", upload_resp.text)
            return -1

        subid = upload_json['subid']
        if prints:
            print(f"[✓] Upload successful. Submission ID: {subid}")
        return subid
    except Exception as e:
        if prints:
            print(f"[X] Fetal error!\n", e)
        return -1


def get_job_id(subbmition_id, timeout_seconds=None, prints=True):
    try:
        if not timeout_seconds:
            timeout_seconds = 10000

        # Step 3: Poll submission status to get JOB ID
        status_url = f'{BASE_URL}/submissions/{subbmition_id}'
        if prints:
            print(f"[-] Waiting for job to submit...")

        job_id = None
        seconds = 0
        while True:
            status_resp = requests.get(status_url)
            status_json = json.loads(status_resp.text)

            jobs = status_json.get('jobs')
            if jobs and jobs[0] is not None:
                job_id = jobs[0]
                if prints:
                    print(f"[✓] Job ID: {job_id}")
                return job_id

            if prints:
                print(".", end="", flush=True)
            time.sleep(5)
            seconds += 5

            if seconds >= timeout_seconds:
                if prints:
                    print(f"[X] Timout")
                return -1

    except Exception as e:
        if prints:
            print(f"[X] Fetal error!\n", e)
        return -1


def await_job(job_id, timeout_seconds=None, prints=True):
    try:
        if not timeout_seconds:
            timeout_seconds = 10000

        job_status_url = f'{BASE_URL}/jobs/{job_id}'
        seconds = 0

        if prints:
            if prints:
                print(f"[-] Waiting for job to complete...")
        while True:
            job_resp = requests.get(job_status_url)
            job_json = json.loads(job_resp.text)

            status = job_json.get('status')
            if status == 'success':
                if prints:
                    print(f"\n[✓] Job {job_id} completed successfully!")
                break
            elif status == 'failure':
                if prints:
                    print(f"\n[!] Job {job_id} failed.")
                return -1

            if prints:
                print(".", end="", flush=True)
            time.sleep(5)

            if seconds >= timeout_seconds:
                if prints:
                    print(f"[X] Timout")
                return -1
    except Exception as e:
        if prints:
            print(f"[X] Fetal error!\n", e)
        return -1


def fetch_annotations(job_id, prints=True):

    try:
        annotations_url = f'{BASE_URL}/jobs/{job_id}/annotations/'
        annotations_resp = requests.get(annotations_url)
        annotations_json = json.loads(annotations_resp.text)

        annotations = annotations_json.get('annotations', [])

        if len(annotations) == 0:
            if prints:
                print(f"\n[X] Found0 objects.")
            return []

        if prints:
            print(f"\n[✓] Found {len(annotations)} known objects:")
        for ann in annotations:
            names = ', '.join(ann['names'])
            if prints:
                print(
                    f" - {names} at ({ann['pixelx']:.1f}, {ann['pixely']:.1f})")

        return annotations
    except Exception as e:
        if prints:
            print(f"[X] Fetal error!\n", e)
        return []

def get_job_calibration(job_id, prints=True):
    url = f"http://nova.astrometry.net/api/jobs/{job_id}/calibration"
    resp = requests.get(url)
    resp.raise_for_status()
    calib = resp.json()
    if prints: print(f"[✓] Job calibration: RA={calib['ra']}, Dec={calib['dec']}")
    return calib