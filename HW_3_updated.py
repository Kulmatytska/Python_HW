import re

text = """homEwork:

  tHis iz your homeWork, copy these Text to variable.



  You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.



  it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.



  last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, but ALL whitespaces. I got 87."""

# count the whitespaces
def count_whitespaces(text):
    count_ws = len(re.findall('\s',  text))
    print(f'The count of whitespaces is {count_ws}')
    return count_ws

# normalize the text and correct "iz"
def normalization (text):
    chars_to_replace = {' iz ': ' is ','\n\n\n': '',':\n': ':'}
    for old_value, new_value in chars_to_replace.items():
        text = text.lower().replace(old_value, new_value)
    text_corrected = re.sub("(^|[.:])\s*([a-zA-Z])", lambda p: p.group(0).upper(), text)
    print(text_corrected)
    return text_corrected

# add words
def add_sentence(text_corrected):
    words = text_corrected.split()
    for word in words:
        if word.endswith(':'):
            text_corrected = text_corrected + ' ' + word[:-1]
        elif word.endswith('.'):
            text_corrected = text_corrected + ' ' + word[:-1]
    print(text_corrected)
    return text_corrected


if __name__=='__main__':
    count_whitespaces(text)
    text_corrected = normalization (text)
    add_sentence(text_corrected)