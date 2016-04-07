# -*- coding: utf-8 -*-
from textblob import TextBlob
import random
import logging

logger = logging.getLogger(__name__)


class TextCorpus(object):
    def __init__(self, seq_sent, nouns_to_sent, adjct_to_sent, verbs_to_sent, nouns_to_quest):
        self.seq_sent =  seq_sent
        self.nouns_to_sent = nouns_to_sent
        self.adjct_to_sent = adjct_to_sent
        self.verbs_to_sent = verbs_to_sent
        self.nouns_to_quest = nouns_to_quest

    def gen_text(self, seeds, desired_length):
        seed = random.choice(seeds)
        if seed in self.nouns_to_sent:
            seed_sents = self.nouns_to_sent[seed]
        elif seed in self.adjct_to_sent:
            seed_sents = self.adjct_to_sent[seed]
        elif seed in self.verbs_to_sent:
            seed_sents = self.verbs_to_sent[seed]
        else:
            logging.debug("No match for seed: {}".format(seed))
            return None

        seed_sent = random.choice(seed_sents)
        #seed_idx = self.seq_sent.index(seed_sent)

        return seed_sent.raw


def keyed_list_append(key, value, dic):
    if key in dic:
        dic[key].append(value)
    else:
        dic[key] = [value]
    return dic


def gen_text_corpus(src_file):
    with open('resources/'+src_file, 'r') as myfile:
        speech_txt = myfile.read().replace('\n', ' ').replace('’', '\'').replace('“', '"').replace('”', '"').replace('—', '-')

    speech_txt = speech_txt.decode('ascii', errors="replace")

    txt_b = TextBlob(speech_txt)
    indexed_verbs = {}
    indexed_nouns = {}
    indexed_adjct = {}
    noun_to_quest = {}
    seq_sentences = []
    for sentence in txt_b.sentences:
        if len(sentence.words) > 2:
            seq_sentences.append(sentence)
            #print "{}\n\t{}".format(sentence, sentence.tags)
            for tag in sentence.tags:
                if tag[1].startswith('VB'):
                    keyed_list_append(tag[0], sentence, indexed_verbs)
                if tag[1].startswith('NN'):
                    keyed_list_append(tag[0], sentence, indexed_nouns)
                    if sentence.ends_with('?'):
                        keyed_list_append(tag[0], sentence, noun_to_quest)
                if tag[1].startswith('JJ'):
                    keyed_list_append(tag[0], sentence, indexed_adjct)

    textCorpus = TextCorpus(seq_sentences, indexed_nouns, indexed_adjct, indexed_verbs, noun_to_quest)

    return textCorpus
