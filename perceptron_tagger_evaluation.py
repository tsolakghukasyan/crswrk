from nltk.tag.perceptron import *


def cross_val_perceptron(sents, fold_num=10):

    num_sents = len(sents)
    foldsize = int(num_sents / fold_num)
    fold_accuracies = []

    for i in range(fold_num):

        # test sents from sents
        test = sents[i * foldsize: i * foldsize + foldsize]
        # use the rest of sents for training
        train = sents[:i * foldsize] + sents[i * foldsize + foldsize:]
        # initialise a tagger
        tagger = PerceptronTagger(False)
        # train the tagger
        tagger.train(train)
        # evaluate the accuracy using the test sents
        accuracy = tagger.evaluate(test)

        # print and store the accuracy on test sents
        print("Fold number:", i)
        print('From sent', i * foldsize, 'to', i * foldsize + foldsize)
        print ('Accuracy on this fold =', accuracy)
        fold_accuracies.append(accuracy)

    print('average accuracy =', sum(fold_accuracies) / fold_num)
    return fold_accuracies


def evaluate_perceptron_ruscorpora(path, max_text_count=530):
    """
    This method evaluates the accuracy of averaged perceptron POS-tagger on
    Russian National Corpus. It uses 10-fold cross-validation.
    Parameter path is the path to the directory that contains RNC files with tagged texts.
    """

    # parses tagged sentences from all RNC files in the directory
    from . import corpora_parser
    corpus, _, _ = corpora_parser.get_train_corpus(path, max_text_count)

    results = cross_val_perceptron(corpus)
    return results