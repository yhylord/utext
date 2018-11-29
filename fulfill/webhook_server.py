
from flask import Flask, request, make_response, jsonify
import requests
import sys
sys.path.insert(0, "./document-qa")

import qa_util
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
    return qa_util.find_answer([passage], question)[0]


@app.route('/debug2')
def debug2():
    docs = utextdata.get_relevent_documents(['allergy', 'shots', 'who provides allergy shots?'])
    best_doc_content = docs[0]['_source']['content']
    content = ". ".join(best_doc_content)
    return content

@app.route('/debug3')
def debug3():
    return handle_text('Allergies', 'Allergy Shots', 'Who provides allergy shots?')

#### Webhook ####

@app.route('/hook', methods=['POST', 'GET'])
def hook():
    if request.method == 'POST':
        intent, query, question = parse_dialogflow(request.get_json())
        return handle_text(intent, query, question)
    else:
        return 'Invalid Request.'


def parse_dialogflow(json_req):
    
    intent_name = json_req['queryResult']['intent']['displayName'].lower()
    
    try:
        query_params = json_req['queryResult']['parameters']['query'].lower()
    except KeyError:
        query_params = ''
        
    user_question = json_req['queryResult']['queryText'].lower()
    
    return intent_name, query_params, user_question


def handle_text(intent_name, query_params, user_question):

    # find related docs
    docs = utextdata.get_relevent_documents([intent_name, query_params, user_question])[:10]
    best_docs = [". ".join(d['_source']['content']) for d in docs]

    # use AI
    all_ans = []
    for doc in best_docs:
        ans, conf = qa_util.find_answer([doc], user_question)
        ans = format_ans(ans)
        all_ans.append((ans, conf))
    all_ans.sort(key=lambda a:a[1], reverse=True)
    
    # construct response
    debug = '[' + docs[0]['_source']['name'] + '] ' + f'(Confidence: {all_ans[0][1]:.2f}%)'
    res = debug + ' ' + all_ans[0][0]

    print('-> ' + res)

    return make_response(jsonify({'fulfillmentText': res}))


def format_ans(ans):
    return ans.capitalize()

#### Run ####

if __name__ == "__main__":

    app.run(host='0.0.0.0', port=8000, debug=False)
