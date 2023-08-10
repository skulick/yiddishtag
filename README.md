# yiddishtag

A Part-of-Speech tagger for Yiddish, as described in 
[A Part-of-Speech Tagger for Yiddish](https://arxiv.org/abs/2204.01175).  

## Installation 

The code is based on [flairNLP](https://github.com/flairNLP/flair), and the 
installation will install `flair` and associated dependencies, along with
some scripts that are wrappers around using `flair`, specialized for Yiddish
tagging.

The installation simply consists of setting up a virtual environment and then
using the requirements.txt file.  The code has been tested with python 3.9 and 3.11.
It should work with any python >= 3.7, but we have not verified that. 

```
python -m venv env-yiddishtag
source env-yiddishtag/bin/activate
cd env-yiddishtag
git clone https://github.com/skulick/yiddishtag
cd yiddishtag
pip install -r requirements.txt
```
which will then install `flair` and associated dependencies. 

## Tagging

The file `tag/tag.py` can be used to run the tagger. Its usage is:

```
usage: tag.py [-h] [--ext EXT] [--skiptok] [--linebyline] [--uni] model out_dir files [files ...]
```
where the arguments are:

Argument | Description |  Default
--- | --- | ---
`model` | model name | N/A
`out_dir` | output directory <br> will be created if necessary | N/A
`files` | list of files to process | N/A
`--skiptok`,<br>`-s`  &nbsp; &nbsp; &nbsp;| skips the tokenization | do not skip the tokenization
`--lineseg`,<br>`-l`  &nbsp; &nbsp; &nbsp;| sentence segments each line separately | concatenates all tokens together first,<br>  then sentence segments
`--uni`, `-u` | adds Unicode code points to output for each token | does not add Unicode code points
`--ext`, `-e` | adds `EXT` after each file's output name | `.tagged`

For each file in `files`, it will read in the text, (optionally) tokenize and sentence segment the text, and write the output to the `out_dir` directory.  Each output file has the name of the input file with a `.tagged` appended after it.  

The different options for segmentations are ones we have found useful for tagging different material.  The tokenization is very simple, just separating out punctuation from words.  This is contained in `tag/tokenizer.py`. The sentence segmentation and tokenization is not meant to be complete, and may need to modified for different files. 

### Sample Usage

We provide a sample input file in `./sample/sample.txt`, and a tagged version in `./sample/sample.txt.tagged`  

The command
```
python tag/tag.py skulick/xlmb-ck05-yid1 ./out/ ./sample/sample.txt
```
will
use the model at https://huggingface.co/skulick/xlmb-ck05-yid1 
to tag `./sample/sample.txt` and
write the tagged version to `./out/sample.txt.tagged`,
which should be identical to the supplied `sample.txt.tagged`

It is not necessary to use `tag.py`. The model is just a `flair` model, and the tagging can be done directly in python. We provide `tag.py` as a convenience and example of use with different input file possibilities. 
