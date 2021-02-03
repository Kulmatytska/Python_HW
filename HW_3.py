import re

text = """homEwork:

  tHis iz your homeWork, copy these Text to variable.



  You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.



  it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.



  last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, but ALL whitespaces. I got 87."""

# count the whitespaces
count_sp = len(re.findall(' ',  text))
count_ws = len(re.findall('\n',  text))
print(f'The count of whitespaces is {count_sp + count_ws}')

# normalize the text and correct "iz"
chars_to_replace = {' iz ': ' is ','\n\n\n': '',':\n': ':'}
for key, value in chars_to_replace.items():
    text = text.lower().replace(key, value)

# add words
a = text.split()
for element in a:
    if element.endswith('.'):
        text = text + ' ' + element[:-1]

# convert first letter of sentence
text_corrected = re.sub("(^|[.:])\s*([a-zA-Z])", lambda p: p.group(0).upper(), text)

print(text_corrected)
