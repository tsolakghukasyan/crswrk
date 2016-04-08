from nltk.tokenize import sent_tokenize
from . import token_extract as t_e


def eval_sent_tokenize(path, max_text_count=530):
    """
    Evaluates the standard nltk sentence tokeniser on Russian National Corpus.
    :return: accuracy, precision, recall, f1-measure of segmentation
    """

    # extract raw and segmented versions of text
    _, _, segmented_text, raw_text = t_e.extract(path, max_text_count)

    # tokenise raw text using punkt tokeniser
    res = sent_tokenize(raw_text, 'russian')

    # remove redundant characters from results and segmented text
    # so that we can compare them
    table = str.maketrans('', '', "(){}<>:;.!,\"?`'")
    new_c = [sent.translate(table) for sent in segmented_text]
    new_res = [sent.translate(table) for sent in res]
    new_text = raw_text.translate(table)

    # evaluate the accuracy, precision, recall and f1-measure
    print(evaluate(new_c, new_res))


def evaluate(gold, result):

    gold_sents = remove_whitespaces(gold)
    result_sents = remove_whitespaces(result)

    gold_binary = get_binary(gold_sents)
    result_binary = get_binary(result_sents)

    predicted_pos = result_binary.count(1)
    condition_pos = gold_binary.count(1)

    true_pos = 0.0
    length = len(gold_binary)
    correct = 0.0

    if length == len(result_binary):
        for i in range(length):
            if gold_binary[i] == result_binary[i]:
                correct += 1.0
                if gold_binary[i] == 1:
                    true_pos += 1.0

    else:
        return 0, 0, 0, 0

    accuracy = correct / length
    precision = true_pos / predicted_pos
    recall = true_pos / condition_pos
    f1 = 2 * precision * recall / (precision + recall)

    return accuracy, precision, recall, f1


def get_binary(sents):

    binary = []
    for sent in sents:
        if len(sent) >= 1:
            binary.extend((len(sent) - 1) * [0])
            binary.append(1)

    return binary


def remove_whitespaces(sents):

    temp = []
    for s in sents:
        ss = remove_whitespaces_raw(s)
        temp.append(ss)
    return temp


def remove_whitespaces_raw(raw_text):

    ss = raw_text.replace('\n', '')
    ss = ss.replace('\r', '')
    ss = ss.replace('\t', '')
    ss = ss.replace(' ', '')
    return ss

