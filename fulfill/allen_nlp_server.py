from allennlp.predictors.predictor import Predictor
predictor = Predictor.from_path("./bidaf-model.tar.gz")
predictor.predict(
          passage="The Matrix is a 1999 science fiction action film written and directed by The Wachowskis, starring Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss, Hugo Weaving, and Joe Pantoliano.",
            question="Who stars in The Matrix?"
            )

from flask import Flask, request, make_response, jsonify
import requests,sys
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
    return predictor.predict(passage, question)['best_span_str']

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
    query_params = req['queryResult']['parameters'].get('query',"").lower()
    user_question = req['queryResult']['queryText'].lower()
    print('intent_name: ', intent_name)
    print('query_params: ', query_params)
    print('user_question: ', user_question)
    # find related docs
    docs = utextdata.get_relevent_documents([intent_name, query_params])
    docs = docs[:5]
    raw_answers = []
    for i,doc in enumerate(docs):
        passage = ". ".join(doc['_source']['content'])
        # use AI
        prediction = predictor.predict(passage=passage, question=user_question)
        raw_ans = prediction['best_span_str']
        raw_ans = raw_ans.capitalize()
        raw_answers.append({'ans': raw_ans, 'doc_index': i, 'ans_length': len(raw_ans)})
        print('raw_ans: ', raw_ans)
    
    raw_answers.sort(key= lambda ans_dict: ans_dict['ans_length'])

    best_answer_and_doc = raw_answers[len(raw_answers)//2]
    best_ans = best_answer_and_doc['ans']
    best_doc = docs[best_answer_and_doc['doc_index']]['_source']

    # construct response
    debug = '[' + query_params + ' @ ' + best_doc['name'] + ']'
    res = debug + ' ' + best_ans

    print('-> ' + res)

    return make_response(jsonify({'fulfillmentText': res}))

#### Run ####

if __name__ == "__main__":

    app.run(host='0.0.0.0', port=8000, debug=False)
