import pandas as pd
import warnings
import csv
import spacy
from tqdm import tqdm
from cleaned import clean
import pickle
import final_similar
warnings.filterwarnings("ignore")
df = pd.read_csv('E:\\intern\\threads1.csv')
incident= pd.read_csv('E:\\intern\\Incident.csv')
df=clean(df,incident) #clean the dataset



nlp = spacy.load("en_core_web_sm")
tok_text=[] # for our tokenised corpus
#Tokenising using SpaCy:
for doc in tqdm(nlp.pipe(df.Text.iloc[:].str.lower().values, disable=["tagger", "parser","ner","lemmatizer"])):
    tok = [t.text for t in doc if t.is_alpha]
    tok_text.append(tok)
#write tokens in csv file
with open("E:\\intern\\final_full_length.csv", "w", newline="",encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(tok_text)
    
with open('E:\\intern\\final_full_length.csv', newline='',encoding="utf-8") as f:
    reader = csv.reader(f)
    data = list(reader)
#create bmi class object after reading from csv file
bmi=final_similar.find_similar_api(data) 
with open('E:\\intern\\object.obj', 'wb') as object_file:
 
  pickle.dump(bmi, object_file)
print("Training done!!")