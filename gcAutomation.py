# This line is used for compatibility between Python 2 and 3. It makes the print function from Python 3 available in Python 2.
from __future__ import print_function 

# importing necessary modules and functions.
import datetime
import os.path

from sys import argv # used to get command-line arguments
from dateutil import parser # used to parse dates

# the rest are Google API client libraries.
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import pyshorteners # shortens the url


# API request scope, it's requesting access to the user's Google Calendar.
SCOPES = ['https://www.googleapis.com/auth/calendar']


# main function that will be executed when the script is run.

def main():
    """ Entry Point.
    Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    
    creds = None # initializes the creds variable, which will later hold the user's credentials.
    
    '''The file token.json stores the user's access and refresh tokens, and is
    created automatically when the authorization flow completes for the first
    time.'''
    
    # checks if a file named token.json exists. If it does, it reads the user's credentials from it.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open('token.json', 'w') as token: # Save the credentials for the next run
            token.write(creds.to_json())
    
    # This block checks if the script was run with the 'add' command-line argument. 
    # If it was but the necessary arguments are missing, it prints a usage message and exits.
    if len(argv)>1 and argv[1] == 'add':
        if len(argv) < 4:
            print("\n Usage: python script_name.py add <duration_in_hours> <event_description> \n")
            return
        
        # gets the duration and description from the command-line arguments and 
        # calls the addEvent function to add an event to the calendar.
        duration = argv[2]
        description = argv[3]
        addEvent(creds, duration, description)     
    commitHours(creds)  # calls the function to print the durations of the upcoming events.
    

# this function takes the user's credentials as an argument.

def commitHours(creds):
    """Gather and print event durations."""

    try:
        service = build('calendar', 'v3', credentials=creds) # creates a service object for interacting with the API.

        # these lines get the current date and create ISO 8601 timestamp strings for the start and end of the day.
        today = datetime.datetime.today().date()
        timeStart = datetime.datetime.combine(today, datetime.time.min).isoformat() + "+05:30"
        timeEnd = datetime.datetime.combine(today, datetime.time.max).isoformat() + "+05:30"

        # sends a request to the Google Calendar API to get a list of the next 
        # 10 single events on the user's calendar, ordered by start time.
        print('\nGetting the upcoming 10 events \n')
        events_result = service.events().list(
            calendarId='your calendar id here',
            timeMin=timeStart, 
            timeMax=timeEnd,
            maxResults=10, 
            singleEvents=True,
            orderBy='startTime', 
            timeZone='Asia/Kolkata'
        ).execute()

        events = events_result.get('items', []) # gets the list of events from the response.

        if not events:
            print('No upcoming events found. \n')
            return
        
        # initializes a timedelta object to hold the total duration of the events.
        total_duration = datetime.timedelta(hours=0, minutes=0, seconds=0) 

        # This block iterates over the events, parses their start and end times, calculates 
        # their durations, adds them to the total duration, and prints their summaries and durations.
        print("Coding Hours: \n")
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))

            start_formatted = parser.isoparse(start)  # changing the start time to datetime format
            end_formatted = parser.isoparse(end)  # changing the end time to datetime format
            duration = end_formatted - start_formatted

            total_duration += duration
            print(f"{event['summary']}, duration: {duration}")
        print(f"\nTotal coding time: {total_duration}") # prints the total duration of the events.
    
    # catches any HttpError that might occur when making the API request and prints it.
    except HttpError as error:
        print('An error occurred: %s' % error)
        

# this function takes the user's credentials, an event duration, and a description as arguments.        

def addEvent(creds, duration, description):
    """Create a new event."""

    # get the current time and calculate the end time of the event by adding the duration to the start time.
    start = datetime.datetime.utcnow()
    end = datetime.datetime.utcnow() + datetime.timedelta(hours=int(duration))
    
    start_formatted = start.isoformat() + 'Z' # 'Z' indicates UTC time
    end_formatted = end.isoformat() + 'Z' # 'Z' indicates UTC time
    
    # a dictionary representing the event to be added to the calendar.
    event = {
        'summary': description,
        
        'start': {
            'dateTime': start_formatted,
            'timeZone': 'Asia/Kolkata',
            },
        
        'end': {
            'dateTime': end_formatted,
            'timeZone': 'Asia/Kolkata',
            },
        }
    
    # sends a request to the Google Calendar API to insert the event into the user's calendar.
    service = build('calendar', 'v3', credentials=creds)
    event = service.events().insert(calendarId='your calendar id here', 
                                    body=event).execute()
    
    # Shorten the URL using pyshorteners
    shortener = pyshorteners.Shortener()
    short_url = shortener.tinyurl.short(event.get('htmlLink'))

    print('\nEvent created: %s' % short_url)
    
    # print('\nEvent created: %s' % (event.get('htmlLink'))) #prints the URL of the created event.

# this block checks if the script is being run directly and calls the main function if it is.
if __name__ == '__main__':
    main()
