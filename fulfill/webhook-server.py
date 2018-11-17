
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
    
    query_type = req['queryResult']['parameters']['query'].lower()
    user_question = req['queryResult']['queryText']['query'].lower()

    docs = utextdata.get_relevent_documents([query_type])
    best_doc = docs[0]['_source']
    passage = ". ".join(best_doc['content'])
    
    res = 'Connected! ' + query_type + ' ' + best_doc['name']
        
    return make_response(jsonify({'fulfillmentText': res}))

#### Run ####

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=False)
