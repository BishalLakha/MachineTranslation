import string
import re
from pickle import dump
from unicodedata import normalize
from numpy import array

def load_data(filename):
    """
    open the file as read only
    :param filename:
    :return:
    """
    with open(filename, mode='rt', encoding='utf-8') as file:
    # read all text
        text = file.read()

    return text

def to_pairs(text):
    """
    split a loaded text into sentences
    :param text:
    :return:
    """
    lines = text.strip().split('\n')
    sent_pairs = [line.split('\t') for line in lines]
    return sent_pairs


def clean_sent_pairs(sent_pairs):
    """
    Clean German-English sentence pairsby carrying out:
    i.   Removing all non-printable characters
    ii.  Removing punctuation
    iii. Normalizing unicode to ASCII
    iv.  Converting to lowercase
    v.   Removing non numeric tokens

    :param sent_pairs:
    :return:
    """
    cleaned = []
    # prepare regex for char filtering
    re_print = re.compile('[^%s]' % re.escape(string.printable))
    # prepare translation table for removing punctuation
    table = str.maketrans('', '', string.punctuation)

    print(table)
    for pair in sent_pairs:
        clean_pair = []
        for line in pair:
            # normalize unicode characters
            line = normalize('NFD', line).encode('ascii', 'ignore')
            line = line.decode('UTF-8')
            # tokenize on white space
            line = line.split()
            # convert to lowercase
            line = [word.lower() for word in line]
            # remove punctuation from each token
            line = [word.translate(table) for word in line]
            # remove non-printable chars form each token
            line = [re_print.sub('', w) for w in line]
            # remove tokens with numbers in them
            line = [word for word in line if word.isalpha()]
            # store as string
            clean_pair.append(' '.join(line))
        cleaned.append(clean_pair)
    return array(cleaned)

def main():
    filename =  "./data/deu-eng/deu.txt"
    text = load_data(filename)
    pairs = to_pairs(text)
    clean_sent_pairs(pairs)



if __name__ =="__main__":
    main()

