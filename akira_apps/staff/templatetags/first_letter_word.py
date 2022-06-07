from django import template
register = template.Library()

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

@register.filter
def first_letter_word(value):
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(value)
    filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words]
    removetable = str.maketrans('', '', '!@#$%^&*()_+-=[]{};:\"\',./<>?\|')
    final = [s.translate(removetable) for s in filtered_sentence]
    final = [s for s in final if s != '']
    chindex=1
    arr = []
    for letter in final:
        if chindex==1:
            arr.append(letter[0].upper())
        else:
            arr.append(letter)
    out = "".join(arr)
    return out