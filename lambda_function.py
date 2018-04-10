import csv
import re
from typing import List

def lambda_handler(event, context):
    to_number = event['To']
    from_number = event['From']
    body = event['Body']
    
    body = body.strip('+')
    body = re.sub('[!@#$.]', '', body)
    
    if not to_number:
        return "The function needs a 'To' number"
    elif not from_number:
        return "The function needs a 'From' number"
    elif not body:
        return "The function needs a 'Body' message to send."
        
    message = body.split('+')

    for row in getData('data.csv'):
        for word in message:
            word = word.lower()
            if word in row['Keywords']:
                return rowtomessage(row)
        
    return "insufficient info"

def notblank(value: str):
    return value == ''

def rowtomessage(row: List[str]):
    message = ''
    for key, val in row.items():
        if key != 'Keywords' and val != '':
            message = message + key + ': ' + val + '\n' 
    return message

def getData(filename: str):
    with open(filename, newline='') as data:
        cols = ['Resource', 'Website', 'Email', 'Phone Number', 'Office Location', 'Office Hours', 'Pertinent Info']
        datareader = csv.DictReader(data, restkey='Keywords', fieldnames=cols, delimiter=',')

        for row in datareader:
            yield row

