from bs4 import BeautifulSoup
import os


def extract(path, max_text_count=530, remove_whitespace_characters=True):
    """
    Parses xhtml files of Russian National Corpus and extracts all tokens, tokenised sentences,
    raw sentences and all raw text in the corpus which can later be used to train and evaluate a tokeniser.

    :param path: path to the directory that contains corpus files
    :param max_text_count: the maximum number of corpus files to parse.
    :param remove_whitespace_characters: if True, removes whitespace characters (' ','\t','\r','\n') from tokens
    :return:
    """
    sents = []
    tokens = []
    sents_with_tokens = []
    raw_text = ''
    j = 0
    # path = '.../RNC_1M/ruscorpora_1M/texts/'

    for filename in os.listdir(path):

        if j > max_text_count:
            break
        j += 1

        f = open(path + filename, 'rb')
        s = f.read()
        f.close()
        s = s.decode('cp1251')
        soup = BeautifulSoup(s)

        for sentence in soup.find_all('se'):

            sent = ''
            sent_with_tokens = []

            t = sentence.find_all(text=True)
            for x in t:
                token = str(x)
                token = token.replace('\u0060', '')

                if remove_whitespace_characters:
                    token = token.replace('\n', '')
                    token = token.replace('\r', '')
                    token = token.replace('\t', '')
                    token = token.replace(' ', '')

                if len(token) > 0:
                    sprtr = ' '
                    sent += token + sprtr
                    raw_text += token + ' '
                    tokens.append(token)
                    sent_with_tokens.append(token)

            if len(sent) > 0:
                sents_with_tokens.append(sent_with_tokens)
                sents.append(sent)

    return tokens, sents_with_tokens, sents, raw_text
