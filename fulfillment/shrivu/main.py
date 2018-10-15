from flask import Flask, request, make_response, jsonify

from datetime import datetime
import dateutil.parser
import requests
import json

WEEKDAYS = "MON,TUE,WED,THU,FRI,SAT,SUN".split(",")

# The "API" is just a spreadsheet
API_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT0zmqln59WP2xs5kWgZlnIbaFLqoqVQIWkNf_b697OYe9IF1zaztwWQc5d52G9AuMT4LF22zk0V0wM/pub?output=csv"


def get_data():
    """Retrieve API data as a dict

    data[utfood][weekday] = "startime:endtime"
    """
    r = requests.get(API_URL).text

    data = {}

    lines = r.replace('\r', '').split('\n')

    for line in lines[1:]:
        
        line_data = line.split(',')
        times = {}
        for i, day in enumerate(WEEKDAYS):
            times[day] = line_data[i + 1]

        data[line_data[0]] = times

    return data

def get_time_open(request):
    """Main Intent Handler

    This handles the intent as sent by dialog flow
    """
    api_data = get_data()
        
    req = request.get_json()

    # extract intent info
    query = req['queryResult']
    place = query['parameters']['utfood']
    timequery = query['parameters']['utfood']

    # assume user wants when place is open
    if len(timequery) == 0:
        timequery = ["time", "open"]

    # parse time info
    query_datetime = get_time(query['parameters'])[0]

    ## Generate Response
    weekday = WEEKDAYS[query_datetime.weekday()]

    if api_data[place][weekday] != '-':

        res = f'{place.title()} is open {api_data[place][weekday]}'

    else:

        res = f'{place.title()} is closed all day.'
    ##
        
    return make_response(jsonify({'fulfillmentText': res}))

def get_time(params):
    """Extract datetime from params

    Since the time can be in many formats,
    this must check every variation and convert
    them into a standard [starttime, endtime]
    """
    if params['date']:
        date = dateutil.parser.parse(params['date'])
        return [date, date]
    
    elif params['date-time']:

        # date-time can be a dict or a str
        if isinstance(params['date-time'], str):
            date = dateutil.parser.parse(params['date-time'])
            return [date, date]
        
        else:
            start = dateutil.parser.parse(params['date-time']['startDateTime'])
            end = dateutil.parser.parse(params['date-time']['endDateTime'])
            return [start, end]
        
    else:
        date = datetime.today()
        return [date, date]
