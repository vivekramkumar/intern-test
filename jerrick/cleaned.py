import re as re
import html
from nltk.stem import WordNetLemmatizer
wordLemm = WordNetLemmatizer()
#vivek cleaning function
def clean(df,incident):
    df.rename(columns={'Foreign Key':'Incident ID'},inplace=True)

    df=df[["Incident Thread ID","Incident ID","Text","Thread Entry Type"]].merge(incident[["Incident ID","Status"]],on="Incident ID",how="left")
    
    df.set_index('Incident Thread ID')
    df=df[df['Thread Entry Type']=='Customer']
    df=df[df['Status'] == 'Solved']
    df['Text']=df['Text'].str.replace("<div>",'')
    df['Text']=df['Text'].str.replace("<div>",'')
    df['Text']=df['Text'].str.replace('</div>','')
    df['Text']=df['Text'].str.replace('\n','')
    df['Text']=df['Text'].str.replace('<br>','')
    df['Text']=df['Text'].str.replace('<br />','')
    df['Text']=df['Text'].str.replace('<div style="margin:0px 0px 8px 0px;">','')
    df['Text']=df['Text'].str.replace('<span>','')
    df['Text']=df['Text'].str.replace('</span>','')
    df['Text']=df['Text'].str.replace('==================== text File Attachment ====================','')
    #df['Text']=df['Text'].str.replace('+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------','')
    df=df[df['Text'].str.len()>12]
    return df

#jerrick cleaning function
def preprocess_text(data):
    preprocessed=[]
    for text in data:
        text=str(text)
        text=re.sub(r'@[A-Za-z0-9]+'," ",text) 
        text=re.sub(r'^[A-Za-z0-9.!?]+'," ",text) 
        text=re.sub(r'https?://[A-Za-z0-9./]+'," ",text) 
        text=re.sub(r' +'," ",text)
        text = text.lower()
        text = re.sub(r"\'s", " ", text)
        text = re.sub(r"\'ve", " have ", text)
        text = re.sub(r"can't", "cannot ", text)
        text = re.sub(r"n't", " not ", text)
        text = re.sub(r"\'d", " would ", text)
        text = re.sub(r"\'ll", " will ", text)
        text = re.sub(r"\'scuse", " excuse ", text)
        text = text.strip(' ')
        text = text.strip('. .')
        text = text.replace('.',' ')
        text = text.replace('-',' ')
        text = text.replace("’", "'").replace("′", "'").replace("%", " percent ").replace("₹", " rupee ").replace("$", " dollar ")
        text = text.replace("won't", "will not").replace("cannot", "can not").replace("can't", "can not")
        text = text.replace("€", " euro ").replace("'ll", " will")
        text = text.replace("don't", "do not").replace("didn't", "did not").replace("im","i am").replace("it's", "it is")
        text = text.replace(",000,000", "m").replace("n't", " not").replace("what's", "what is")
        text = text.replace(",000", "k").replace("'ve", " have").replace("i'm", "i am").replace("'re", "are")
        text = text.replace("he's", "he is").replace("she's", "she is").replace("'s", " own")
        text = re.sub('\s+', ' ', text)

        textwords = ''
        for word in text.split():
            if len(word)>1:
                word = wordLemm.lemmatize(word)
                textwords += (word+' ')
        preprocessed.append(textwords)
    return preprocessed

# tharun cleaning functions
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