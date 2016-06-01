# -*- coding: utf-8 -*-
import re
from mezzanine.conf import settings as mz_settings
import jieba


def split_words(text):
    return re.split(r'[\s\r\n,]+', text, re.U|re.S)


def comment_forbidden_words():
    return split_words(mz_settings.GC_COMMENT_FORBIDDEN_WORDS.lower())


def setup_words_segmentation(words, freq=100):
    for w in words:
        jieba.add_word(word=w, freq=freq)


def get_forbidden_words_from(forbidden_words, content):
    setup_words_segmentation(forbidden_words)
    _content = content.lower()
    forbidden_words = list(set(jieba.cut(_content)) & set(forbidden_words))
    return forbidden_words
