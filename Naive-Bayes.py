
import os
import math
from collections import defaultdict

def load_training_data(vocab, directory):
    """ Create the list of dictionaries """
    top_level = os.listdir(directory)
    dataset = []
    for d in top_level:
        if d[-1] == '/':
            label = d[:-1]
            subdir = d
        else:
            label = d
            subdir = d+"/"
        files = os.listdir(directory+subdir)
        for f in files:
            bow = create_bow(vocab, directory+subdir+f)
            dataset.append({'label': label, 'bow': bow})
    return dataset

def create_vocabulary(directory, cutoff):
    """ Create a vocabulary from the training directory
        return a sorted vocabulary list
    """
    top_level = os.listdir(directory)
    vocab = {}
    for d in top_level:
        subdir = d if d[-1] == '/' else d+'/'
        files = os.listdir(directory+subdir)
        for f in files:
            with open(directory+subdir+f,'r') as doc:
                for word in doc:
                    word = word.strip()
                    if not word in vocab and len(word) > 0:
                        vocab[word] = 1
                    elif len(word) > 0:
                        vocab[word] += 1
    return sorted([word for word in vocab if vocab[word] >= cutoff])

def create_bow(vocab, filepath):
    """ Create a single dictionary for the data
        Note: label may be None
    """
    bow = defaultdict(int)
    with open(filepath, 'r') as doc:
        for word in doc:
            word = word.strip()
            if word in vocab:
                bow[word] += 1
            else:
                bow[None] += 1
    return dict(bow)

def prior(training_data, label_list):
    """ return the prior probability of the label in the training set
        => frequency of DOCUMENTS
    """
    smooth = 1 # smoothing factor
    logprob = {}
    number_of_files = {}

    for label in label_list:
        number_of_files[label] = 0

    for data in training_data:
        number_of_files[data['label']] += 1

    # print(number_of_files)
    for key, val in number_of_files.items():
        logprob[key] = math.log((val+smooth)/((len(training_data))+len(label_list)))

    return logprob

def p_word_given_label(vocab, training_data, label):
    """ return the class conditional probability of label over all words, with smoothing """
    smooth = 1 # smoothing factor
    word_prob = defaultdict(int)

    total_word_count = 0
    word_count = defaultdict(int)

    for data in training_data:
        if data['label'] == label:
            bow = data['bow']
            for word, count in bow.items():
                total_word_count += count
                word_count[word] += count
    new_vocab = set()
    for data in training_data:
        bow = data['bow']
        for word, count in bow.items():
            new_vocab.add(word)

    for word in new_vocab:
        word_prob[word] = math.log((word_count[word] + smooth*1)/(total_word_count + smooth*(len(vocab)+1)))

    if None not in word_prob.keys():
        word_prob[None] = math.log((smooth*1)/(total_word_count + smooth*(len(vocab)+1)))

    return dict(word_prob)

def train(training_directory, cutoff):
    retval = {}
    label_list = os.listdir(training_directory)
    retval['vocab'] = create_vocabulary(training_directory, cutoff)
    training_data = load_training_data(retval['vocab'], training_directory)
    retval['log prior'] = prior(training_data, label_list)
    retval['log p(w|y=2016)'] = p_word_given_label(retval['vocab'], training_data, '2016')
    retval['log p(w|y=2020)'] = p_word_given_label(retval['vocab'], training_data, '2020')
    return retval

def classify(model, filepath):

    retval = defaultdict(int)
    retval['log p(y=2016|x)'] = model['log prior']['2016']
    retval['log p(y=2020|x)'] = model['log prior']['2020']

    # print(model['log p(w|y=2020)'])
    with open(filepath, 'r') as doc:
        for word in doc:
            word = word.strip()
            if word in model['log p(w|y=2020)'].keys():
                retval['log p(y=2020|x)'] += model['log p(w|y=2020)'][word]
            else:
                retval['log p(y=2020|x)'] += model['log p(w|y=2020)'][None]

            if word in model['log p(w|y=2016)'].keys():
                retval['log p(y=2016|x)'] += model['log p(w|y=2016)'][word]
            else:
                retval['log p(y=2016|x)'] += model['log p(w|y=2016)'][None]

    retval['predicted y'] = '2016' if retval['log p(y=2016|x)'] > retval['log p(y=2020|x)'] else '2020'

    return dict(retval)

# model = train('./HW2/corpus/training/', 2)


# print(classify(model, './HW2/corpus/test/2016/0.txt'))
# print(classify(model, './HW2/corpus/test/2016/68.txt'))
# print(classify(model, './HW2/corpus/test/2016/54.txt'))
#


# files = os.listdir("./HW2/corpus/test/2016/")
#
# for f in files:
#     print('2016', classify(model, './HW2/corpus/test/2016/'+f)['predicted y'])
#
#
# files = os.listdir("./HW2/corpus/test/2020/")
#
# for f in files:
#     print('2020', classify(model, './HW2/corpus/test/2020/'+f)['predicted y'])

# print(vocab)
# print(create_bow(vocab, './HW2/EasyFiles/2016/1.txt'))
# training_data = load_training_data(vocab,'./HW2/EasyFiles/')
# print(
# for data in training_data:
#     print(data['bo'])
# print(
#
#
# print(p_word_given_label(vocab, training_data, '2016'))
#
# vocab = create_vocabulary('./HW2/corpus/training/', 2)
# # print(vocab)
# # print(create_bow(vocab, './HW2/EasyFiles/2016/1.txt'))
# training_data = load_training_data(vocab,'./HW2/corpus/training/')
# print(prior(training_data, ['2020', '2016']))
