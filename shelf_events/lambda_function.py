import json
import urllib3
import os
import logging

def lambda_handler(event, context):
    logging_handler(event)
    #whurl = os.environ['TESTING'] #for testing channel output
    whurl = os.environ['SLACK_WEBHOOK']
    #message = {"text": f"{event}"} #uncomment to output entire event to slack, may bog down speeds
    message = message_handler(event)
    send_webhook(whurl, message)

    #AKA reverse api
def send_webhook(webhook_url, payload):
    #text = "Hello Hammer Creative, from AWS Lambda"
    
    # Create an HTTP pool manager
    http = urllib3.PoolManager()
    try:
        # Send the POST request with JSON payload
        response = http.request(
            "POST",
            webhook_url,
            body=json.dumps(payload)
        )
        
        # Check for successful response
        if response.status != 200:
            print(f"Error: {response.status}")
        
        else:
            print("Webhook sent successfully")

    except Exception as e:
        # Log the error if the request fails
        return {"statusCode": 500, "body": f"Error: {str(e)}"}

#TODO, needs to change based on event type
def message_handler(event_name):
    #action = ''
    #page_name = ''
    #date_occurred = ''
    #user = ''

    if "bookshelf_create" == event_name['event']:
        action = 'SHELF CREATED'
        page_name = event_name['related_item']['name']
        date_occurred = event_name['related_item']['created_at'].split('T')
        user = event_name['related_item']['created_by']['name']

    if "bookshelf_update" == event_name['event']:
        action = 'SHELF UPDATED'
        page_name = event_name['related_item']['name']
        date_occurred = event_name['related_item']['updated_at'].split('T')
        user = event_name['related_item']['updated_by']['name']

    if "bookshelf_delete" == event_name['event']:
        action = '****SHELF DELETED****'
        page_name = event_name['related_item']['name']
        date_occurred = event_name['related_item']['updated_at'].split('T')
        user = event_name['related_item']['updated_by']['name']

    if "bookshelf_create_from_book" == event_name['event']:
        action = 'SHELF CREATED FROM BOOK'
        page_name = event_name['related_item']['name']
        date_occurred = event_name['related_item']['updated_at'].split('T')
        user = event_name['related_item']['updated_by']['name']

    message = {"text": "----------------------------------------------\n"+
                f"** {action} ** \n"+
                f"Page Name: \"{page_name}\" \n"+
                f"Date: \"{date_occurred}\" \n"+
                f"By: \"{user}\""}
    
    return message

def logging_handler(event):
    logger = logging.getLogger()
    logger.setLevel("INFO")
    logger.info(event)     
 