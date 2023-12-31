# yiddishtag

A Part-of-Speech tagger for Yiddish, as described in 
[A Part-of-Speech Tagger for Yiddish](https://arxiv.org/abs/2204.01175).  Please see this paper for full details of the tagset. 

Please note that the tagger, as described in that paper, was trained and evaluated on a relatively small amount of text.  We welcome any feedback, either on the Issues section here, or you can send email to Seth Kulick (<skulick@ldc.upenn.edu>).


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

<span style="display: inline-block; width:800px">Argument</span> | Description |  Default
-------- | -------- | ---
model | model name | N/A
out_dir | output directory <br> will be created if necessary | N/A
files | list of files to process | N/A
<span style="display: inline-block; width:1000px">--skiptok</span>,<br> -s,   | skips the tokenization | do not skip the tokenization
--lineseg, <br> -l  | sentence segments each line separately | concatenates all tokens together first, then sentence segments
--uni, <br> -u | adds Unicode code points to output for each token | does not add Unicode code points
--ext EXT, <br> -e EXT | adds EXT after each file's output name | .tagged

For each file in `files`, it will read in the text, (optionally) tokenize and sentence segment the text, and write the output to the `out_dir` directory.  Each output file has the name of the input file with a `.tagged` appended after it.  

The different options for segmentations are ones we have found useful for tagging different material.  The tokenization is very simple, just separating out punctuation from words.  This is contained in `tag/tokenizer.py`. We have used this sentence segmentation and tokenization for files we have worked with, but it may need to modified for different input files.  

### Sample Usage

We provide a sample input file in `./sample/sample.txt`, and a tagged version in `./sample/sample.txt.tagged`  

The command
```
python tag/tag.py skulick/xlmb-ck05-yid1 ./out/ ./sample/sample.txt
```
will use the model at https://huggingface.co/skulick/xlmb-ck05-yid1 
to tag `./sample/sample.txt` and
write the tagged version to `./out/sample.txt.tagged`,
which should be identical to the supplied `sample.txt.tagged`

It is not necessary to use `tag.py`. The model is just a `flair` model, and the tagging can be done directly in python. We provide `tag.py` as a convenience and example of use with different input file possibilities. 

The first time this command is run, it will download models from hugging face, which could take a few minutes.  

## Usage Notes

The Unicode representation of Yiddish can be encoded in several ways.  The data from the Penn Parsed Corpus of Historical Yiddish that was used to train this tagger (see [here](https://github.com/skulick/ppchyprep)) used the Unicode code points

```
0x5f0	HEBREW LIGATURE YIDDISH DOUBLE VAV
0x5f1	HEBREW LIGATURE YIDDISH VAV YOD
0x5f2	HEBREW LIGATURE YIDDISH DOUBLE YOD
```
for tsvey vovn, vov yud, and tsvey yudn, respectively, instead of decomposing them into the separate letters.  It also only used code points in "Hebrew block" (0590-05FF) of Unicode, not the  the "presentation forms" (FB00-FB4F).  








