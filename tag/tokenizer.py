import re

RE_FLAGS = re.UNICODE
QUOTE_LEFT = "\u201e" #DOUBLE LOW-9 QUOTATION MARK
QUOTE_RIGHT = "\u201c"  #LEFT DOUBLE QUOTATION MARK


def normalize(txt):
    txt = txt.replace(QUOTE_LEFT, '"')
    txt = txt.replace(QUOTE_RIGHT, '"')
    return txt

def tokenize(txt):
    # separate multiple parens
    txt = re.sub(r'(\(+)', r' \1 ', txt)
    txt = re.sub(r'(\)+)', r' \1 ', txt)
    # and multiple quotes
    txt = re.sub(r'(\"+)', r' \1 ', txt)
    # split off multiple periods, different than single period
    txt = re.sub(r'(\.+)', r' \1 ', txt)

    # split off --, but leave - as they are
    txt = txt.replace('--', ' -- ')
    
    for chr1 in ',?!:;':
        txt = txt.replace(chr1, f' {chr1} ')
        
    #separate after two non-periods
    #so won't modify ...
    #or initial with period
    txt = re.sub(r'([^ \.][^ \.])\.(\s|$)', r'\1 .', txt)        
    return txt.strip().split()
