import os, requests

def main(event):
  
  token = os.getenv("RevOps")
  custom_object_id = "2-39538272"
  meeting_id = event.get("inputFields").get("meeting_id")
  outcome = event.get("inputFields").get("outcome")
  record_updated = 0
  url = "https://api.hubapi.com/crm/v3/objects"
  headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
  }
  search_url = f"{url}/{custom_object_id}/search"
  search_payload = {
    "filterGroups": [
      {
        "filters": [
          {
            "propertyName": "meeting_record_id",
            "operator": "EQ",
            "value": meeting_id
          }
        ]
      }
    ]
  }
  search_response = requests.post(search_url, headers=headers, json=search_payload)
  if search_response.status_code == 200:
    search_results = search_response.json()
    if "results" in search_results and search_results["results"]:
      record_id = search_results["results"][0]["id"]
      update_url = f"{url}/{custom_object_id}/{record_id}"
      update_payload = {
        "properties": {
          "outcome": outcome
        }
      }
      update_response = requests.patch(update_url, headers=headers, json=update_payload)
      if update_response.status_code == 200:
        record_updated = 1
      else:
        record_updated = 0
    else:
      record_updated = 0
  else:
    record_updated = 0
  return {
    "outputFields": {
      "Meeting_ID": meeting_id,
      "Outcome": outcome,
      "Record_Updated": record_updated
    }
  }