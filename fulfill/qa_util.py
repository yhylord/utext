
# imports
import sys
sys.path.insert(0, "./qa-model")

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import numpy as np
np.warnings.filterwarnings('ignore')

import warnings
warnings.filterwarnings("ignore")

import tensorflow as tf
import re

from docqa.data_processing.document_splitter import MergeParagraphs, TopTfIdf, ShallowOpenWebRanker, PreserveParagraphs
from docqa.data_processing.qa_training_data import ParagraphAndQuestion, ParagraphAndQuestionSpec
from docqa.data_processing.text_utils import NltkAndPunctTokenizer, NltkPlusStopWords
from docqa.doc_qa_models import ParagraphQuestionModel
from docqa.model_dir import ModelDir
from docqa.utils import flatten_iterable

# load model
model_dir = ModelDir(os.path.join('.', 'qa-model'))
model = model_dir.get_model()

print('Generating Vocab...', end='')

# preload all the words
vocab = set()
with open(os.path.join('.', 'qa-model', 'glove', 'glove.840B.300d.txt'), encoding='utf-8') as glove:
    for line in glove:
        word = line[:line.index(' ')]
        if word.isalpha() or word in "...,/:;-%$?![]()":
            vocab.add(word.lower())

print('done')

print('Loading Model...', end='')

# init tf session and weights
model.set_input_spec(ParagraphAndQuestionSpec(batch_size=None), vocab)

sess = tf.Session(config=tf.ConfigProto(allow_soft_placement=True))

with sess.as_default():
    best_spans, conf = model.get_prediction().get_best_span(16)
    model_dir.restore_checkpoint(sess)

print('done')

# use docs: list<str> to find ans: str to question: str
def find_answer(documents, raw_question):

    raw_question = raw_question.lower()
    documents = [d.lower() for d in documents]

    global best_spans, conf

    documents = [re.split("\s*\n\s*", doc) for doc in documents]
    tokenizer = NltkAndPunctTokenizer()
    
    question = tokenizer.tokenize_paragraph_flat(raw_question)
    
    documents = [[tokenizer.tokenize_paragraph(p) for p in doc] for doc in documents]
    
    splitter = MergeParagraphs(400)
    
    documents = [splitter.split(doc) for doc in documents]

    if len(documents) == 1:
        selector = TopTfIdf(NltkPlusStopWords(True), n_to_select=5)
        context = selector.prune(question, documents[0])
    else:
        selector = ShallowOpenWebRanker(n_to_select=10)
        context = selector.prune(question, flatten_iterable(documents))

    context = [flatten_iterable(x.text) for x in context]
    
    data = [ParagraphAndQuestion(x, question, None, "user-question%d"%i)
            for i, x in enumerate(context)]

    encoded = model.encode(data, is_train=False)

    with sess.as_default():
        spans, confid = sess.run([best_spans, conf], feed_dict=encoded)

    best_para = np.argmax(confid)
    ans = " ".join(context[best_para][spans[best_para][0]:spans[best_para][1]+1])
    confidence = confid[best_para]

    return ans, confidence

if __name__ == "__main__":

    my_question = "When is the UHS Nurse Advice Line open?"

    documents = [
        """
        The UHS Nurse Advice Line is staffed 24 hours a day, every day of the year. Call for advice on how to care for an illness or injury at home or guidance about whether and when to see a healthcare provider.
        The Nurse Advice Line is available only to students at the University of Texas at Austin.
        """
    ]

    print(find_answer(documents, my_question))
    print(find_answer(documents, my_question))
    print(find_answer(documents, my_question))
