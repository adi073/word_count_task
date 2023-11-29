#!/usr/bin/python3

import glob

input_dir = 'inputs'
out_dir = 'out'

def count_input_words():
    '''count words from input file'''
    word_dict = {}
    for _file in glob.glob(input_dir + "/*.txt"):
        with open(_file) as f:
            contents = f.read()
            for word in contents.split():
                if word in word_dict:
                    word_dict[word] += 1
                else:
                    word_dict[word] = 1
    return word_dict

def test_word_count():
    original_count_dict = count_input_words()
    for _file1 in glob.glob(out_dir + "/*"):
        with open(_file1) as f:
            for line in f:
                line = line.strip()
                word, count = line.split()
                count = int(count)
                assert word in original_count_dict, f'{word} is not in real words'
                assert count == original_count_dict.pop(word)

    # the dictionary must be empty
    assert not original_count_dict
