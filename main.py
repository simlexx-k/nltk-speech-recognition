import nltk
nltk.download('swahili')
from nltk.tag import pos_tag

sentence = 'Currently, NLTK pos_tag only supports English and Russian.'

tokenize = nltk.word_tokenize(sentence)

split_sentence = sentence.split()

tagged = pos_tag(split_sentence, lang='eng')
print(tagged)