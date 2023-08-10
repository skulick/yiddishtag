"""Runs the tagger on given files

See README.md for usage
"""
import os
import argparse
import pathlib
import itertools
import unicodedata
from flair.models import SequenceTagger
from flair.data import Sentence
from tokenizer import normalize, tokenize


def split_sents(tokens):
    """Split a list of tokens into sentences"""
    sents = []
    idxs = [idx for (idx, token) in enumerate(tokens, 1)
            if token in '.?!']
    start_idxs = [0] + idxs
    end_idxs = idxs + [len(tokens)]
    sents = [tokens[start:end]
             for (start, end) in zip(start_idxs, end_idxs)
             if start < end]
    if len(sents[-1]) == 0:
        print('huh')
    return sents

def get_sents_from_file(fname, skiptok, lineseg):
    """Convert one file to the sentences needed for tagging

    First normalizes and tokenizes each line
    Then gets the sentences from each one, or combines all lines
    together and gets the sentences from the one string

    Parameters
    ==========
    fname: Path
        file to tag
    skiptok: boolean
        if True, skips the tokenization and normalization
    lineseg: boolean
        if True, sentence segments each line separately
        if False, concatenates all tokens together first

    Returns
    =======
    list of Sentence
    """
    with open(fname, 'r', encoding='utf-8') as fin:
        lines = fin.readlines()
    lines = [unicodedata.normalize('NFC', line)
             for line in lines]
    lines = [line.rstrip('\n') for line in lines]

    # skip blank lines
    lines = [line for line in lines if line]

    if not skiptok:
        lines = [tokenize(normalize(line)) for line in lines]
    else:
        lines = [line.split() for line in lines]

    if lineseg:
        lines = [split_sents(line) for line in lines]
        sents_ = itertools.chain.from_iterable(lines)
    else:
        all_tokens = list(itertools.chain.from_iterable(lines))
        sents_ = split_sents(all_tokens)

    # False means to not use the flair tokenizer
    sents = [Sentence(sent_, False)
             for sent_ in sents_]
    return sents

def write_file(sents, out_fname, uni):
    """Write the output, one token each row

    Parameters
    ==========
    sents: list of Sent
        tagged sentences
    out_fname: Path
        output file
    uni: boolean
       if True, also writes all the Unicode for each token
    """
    with open(out_fname, 'w', encoding='utf-8') as fout:
        for (num, sent) in enumerate(sents):
            fout.write(f'SENT\t{num}\n')
            for (num2, token) in enumerate(sent.tokens):
                pred_labels = token.annotation_layers['predicted']
                assert len(pred_labels) == 1, 'impossible'
                pred_label = pred_labels[0]
                if uni:
                    hex_lst = [(hex(ord(chr1)), unicodedata.name(chr1))
		               for chr1 in token.text]
                    hex_lst_str = ' '.join([f'{a}:{b}' for (a,b) in hex_lst])
                    fout.write(f'TOK\t{num2}\t{token.text}\t'
                               f'{pred_label.value}\t{pred_label.score:.2f}\t'
                               f'{hex_lst_str}\n')
                else:
                    fout.write(f'TOK\t{num2}\t{token.text}\t'
                               f'{pred_label.value}\t{pred_label.score:.2f}\n')
            fout.write('\n')

def main():
    parser = argparse.ArgumentParser(description='tag yiddish')
    parser.add_argument('model', type=pathlib.Path)
    parser.add_argument('out_dir', type=pathlib.Path)
    parser.add_argument('files', type=pathlib.Path, nargs='+')
    parser.add_argument('--ext', '-e', type=str, default='.tagged',
                        help='extension to add to output file name')
    parser.add_argument('--skiptok', '-s', action='store_true',
                        help='skip tokenization')
    parser.add_argument('--lineseg', '-l', action='store_true',
                        help='sentence segment each line separately')
    parser.add_argument('--uni', '-u', action='store_true',
                        help='add unicode info for each line')


    args = parser.parse_args()

    tagger = SequenceTagger.load(args.model)
    print(f'loaded tagger {args.model}')

    os.makedirs(args.out_dir, exist_ok=True)

    for fname in args.files:
        sents = get_sents_from_file(fname, args.skiptok, args.lineseg)
        tagger.predict(sents, label_name="predicted")
        out_fname = args.out_dir / f'{fname.name}{args.ext}'
        write_file(sents, out_fname, args.uni)

if __name__ == '__main__':
    main()
