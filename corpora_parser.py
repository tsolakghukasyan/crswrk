from bs4 import BeautifulSoup
import os


def get_train_corpus(path, max_text_count=530):  # path = '.../RNC_1M/ruscorpora_1M/texts/'
    """
    Parses xhtml files of Russian National Corpus and retrieves tagged sentences
    which can be used to train a tagger.

    :param path: path to the directory that contains corpus files
    :param max_text_count: the maximum number of corpus files to parse.
    :return: returns list of all tagged sentences, all words and tags.
    """
    corpus = [] # to store all sentences
    words = []  # to store all words
    tags = []   # to store all tags
    j = 0

    for filename in os.listdir(path):

        if j > max_text_count:
            break
        j += 1

        f = open(path + filename, 'r', encoding='cp1251')
        s = f.read()
        f.close()
        soup = BeautifulSoup(s)

        # iterates over all sentences in text file
        # sentences have 'se' tag in the file
        for sentence in soup.find_all('se'):
            sent = []

            # iterates over all words in each sentence
            # words have 'w' tag in the file
            for word in sentence.find_all('w'):
                tag = word.ana['gr']
                i = tag.find(",")
                if i > 0:
                    tag = tag[:i]
                str_word = word.contents[-1]
                # removes stress character
                str_word = str_word.replace('\u0060', '')
                sent.append((str_word, tag))
                words.append(str_word)
                tags.append(tag)
            if len(sent) > 0:
                corpus.append(sent)
                
    return corpus, words, tag

