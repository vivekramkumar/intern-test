import pandas as pd
import re as re
import html
Apos_dict={"'s":" is","n't":" not","'m":" am","'ll":" will","'d":" would","'ve":" have","'re":" are"}

def cleaning_text(string):
        string = re.sub('<.*?>',' ',string)
        string = html.unescape(string)
        string = re.sub(r',', ' ', string)
        string = re.sub(r'[^\w\s]', ' ', string)
        return string
def cleaning_text1(string):
        regex  = re.compile(r'[\n\r\t]')
        regex1 = re.compile(r'[=]')
        string = regex.sub( '', string)
        string = regex1.sub( '',string)
        string = re.sub(r'http\S+', ' ', string)
        string = re.sub(r'www\S+', ' ', string)
        string = re.sub(r'[0-9]', ' ', string)
        string = string.lower()
        string = string.strip()
        string = re.sub(' +', ' ', string)
        return string
def contraction_text(string):
    for key,value in Apos_dict.items():
        if key in string:
            result=string.replace(key,value)
            return result
        else:
            return string
def meaningless_words(string):
        string = re.sub(r'dtype',' ',string)
        string = re.sub(r'object',' ',string)
        string = re.sub(r'name',' ',string)
        string = re.sub(r'hi',' ',string)
        string = re.sub(r'hello',' ',string)
        string = re.sub(r'dear',' ',string)
        string = re.sub(r'thank',' ',string)
        string = re.sub(r'sorry',' ',string)
        string = re.sub(r'span',' ',string)
        string = re.sub(r'px',' ',string)
        return string
    