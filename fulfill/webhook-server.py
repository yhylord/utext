import sys
sys.path.insert(0, "./qa_net")

from flask import Flask, request, make_response, jsonify
import solver
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return 'UText Webhook'

@app.route('/debug')
def debug():
    passage = """
    The UHS Nurse Advice Line is staffed 24 hours a day, every day of the year. Call for advice on how to care for an illness or injury at home or guidance about whether and when to see a healthcare provider.

    The Nurse Advice Line is available only to students at the University of Texas at Austin.
    """
    question = "When is the UHS Nurse Advice Line open?"
    return solver.solve(passage, question)

@app.route('/hook', methods=['POST', 'GET'])
def hook():
    if request.method == 'POST':
        return handle_text(request)
    else:
        return 'Invalid Request.'

def handle_text(request):
    """Main Intent Handler
     This handles the intent as sent by dialog flow
    """
    # api_data = get_data()
        
    req = request.get_json()
    query = req['queryResult']['parameters']['query']
    res = 'Connected! ' + query
        
    return make_response(jsonify({'fulfillmentText': res}))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=False)
