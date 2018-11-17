
from flask import Flask, request, make_response, jsonify
import requests
import sys
sys.path.insert(0, "./qa_net")

import solver
import utextdata

app = Flask(__name__)

#### Index Page ####

@app.route('/')
def index():
    return 'UText Webhook'

#### Debug Systems ####

@app.route('/debug')
def debug():
    passage = """
    The UHS Nurse Advice Line is staffed 24 hours a day, every day of the year. Call for advice on how to care for an illness or injury at home or guidance about whether and when to see a healthcare provider.

    The Nurse Advice Line is available only to students at the University of Texas at Austin.
    """
    question = "When is the UHS Nurse Advice Line open?"
    return solver.solve(passage, question)

@app.route('/debug2')
def debug2():
    docs = utextdata.get_relevent_documents(['allergy', 'shots'])
    best_doc_content = docs[0]['_source']['content']
    content = ". ".join(best_doc_content)
    return content

#### Webhook ####

@app.route('/hook', methods=['POST', 'GET'])
def hook():
    if request.method == 'POST':
        return handle_text(request)
    else:
        return 'Invalid Request.'

def handle_text(request):

    req = request.get_json()

    # extract info from dialogflow
    intent_name = req['queryResult']['intent']['displayName'].lower()
    query_params = req['queryResult']['parameters']['query'].lower()
    user_question = req['queryResult']['queryText'].lower()

    # find related docs
    docs = utextdata.get_relevent_documents([intent_name, query_params])
    best_doc = docs[0]['_source']
    passage = ". ".join(best_doc['content'])

    # use AI
    raw_ans = solver.solve(passage, user_question)
    raw_ans = raw_ans.capitalize()

    # construct response
    debug = '[' + query_params + ' @ ' + best_doc['name'] + ']'
    res = debug + ' ' + raw_ans

    print('-> ' + res)

    return make_response(jsonify({'fulfillmentText': res}))

#### Run ####

if __name__ == "__main__":

    # warm up
    passage = """
    The UHS Nurse Advice Line is staffed 24 hours a day, every day of the year.
    """
    solve(passage, "When is the UHS Nurse Advice Line open?")

    app.run(host='0.0.0.0', port=8000, debug=False)
