import requests
import sys
import os
import logging
from datetime import datetime

current_timestamp_raw = datetime.now()
current_timestamp = current_timestamp_raw.strftime("%Y%m%d-%I%M%S")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] - %(message)s",
    handlers=[
        logging.FileHandler(f"./{current_timestamp}.log"),
        logging.StreamHandler()
    ]
)

gh_access_token = 'token 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'

headers = {
    'Authorization': gh_access_token
}

proceed = False

logging.info("Checking if there are any Job in Queue or In Progress")
no_wait = True
while True:
    response = requests.request(method="GET", url="https://api.github.com/repos/madhum-py/common_test/actions/runs?per_page=30", headers = headers)
    ##print(response.json())
    ##print(response.headers)
    link_header = (response.headers)['Link'].split(";")
    last_index = link_header.index(' rel="last"')
    number_of_pages = int(link_header[last_index - 1].split("page")[-1].strip("=").strip(">"))
    #print(number_of_pages)
    count = 1
    go_ahead = True
    for i in response.json()['workflow_runs']:
        if count == 1:
            first_job_name = i['name']
            count += 1
            continue
        #print(f"--- {count} ---")
        count += 1
        workflow_name = i['name']
        workflow_started_at = i['created_at']
        workflow_status = i['status']
        workflow_run_number = i['run_number']
        #print(workflow_status)
        #print(i['conclusion'])

        status_list = ["in_progress", "queued", "requested", "waiting"]
        if workflow_status in status_list and i['name'] == first_job_name:
            logging.info(f"Workflow '{workflow_name} (Run Number : #{workflow_run_number}) is currently in '{workflow_status}' State. Hence, waiting for 5 seconds")
            os.system("sleep 5")
            go_ahead = False
            no_wait = False
            break

        if count == 12:
            break

    if go_ahead:
        if no_wait:
            logging.info("No recent job in Queued/In Progress. Hence, starting the Workflow")
        else:
            logging.info("All the workflows are completed now. Hence, starting the Workflow.")
        break

