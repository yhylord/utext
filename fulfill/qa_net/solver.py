import tensorflow as tf
import json
import numpy as np
import config as cfg

config = cfg.flags.FLAGS

from model import Model
from prepro import convert_to_features, word_tokenize
import os

with open(os.path.join('qa_net', config.word_emb_file), "r") as fh:
    word_mat = np.array(json.load(fh), dtype=np.float32)
with open(os.path.join('qa_net', config.char_emb_file), "r") as fh:
    char_mat = np.array(json.load(fh), dtype=np.float32)
with open(os.path.join('qa_net', config.test_meta), "r") as fh:
    meta = json.load(fh)

model = Model(config, None, word_mat, char_mat, trainable=False, demo=True)

with open(os.path.join('qa_net', config.word_dictionary), "r") as fh:
    word_dictionary = json.load(fh)
with open(os.path.join('qa_net', config.char_dictionary), "r") as fh:
    char_dictionary = json.load(fh)

sess_config = tf.ConfigProto(allow_soft_placement=True)
sess_config.gpu_options.allow_growth = True

def solve(passage, question):

    with model.graph.as_default():

        with tf.Session(config=sess_config) as sess:
            
            sess.run(tf.global_variables_initializer())
            
            saver = tf.train.Saver()
            saver.restore(sess, tf.train.latest_checkpoint(os.path.join('qa_net', config.save_dir)))
            
            if config.decay < 1.0:
                
                sess.run(model.assign_vars)
                
            context = word_tokenize(passage.replace("''", '" ').replace("``", '" '))
            c,ch,q,qh = convert_to_features(config, (passage, question), word_dictionary, char_dictionary)
            fd = {'context:0': [c], 'question:0': [q], 'context_char:0': [ch], 'question_char:0': [qh]}
            yp1, yp2 = sess.run([model.yp1, model.yp2], feed_dict = fd)
            yp2[0] += 1
            response = " ".join(context[yp1[0]:yp2[0]])

            return response
