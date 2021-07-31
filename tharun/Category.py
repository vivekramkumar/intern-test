# importing pandas library(pandas is a fast, powerful, flexible and easy to use open source data analysis and manipulation tool)
import pandas as pd
import pickle
from data_cleaning import cleaning_text,cleaning_text1,contraction_text,meaningless_words
from scipy.stats import randint
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC

# Fetching the data to dataframe for trainig the model
thread_df       = pd.read_excel("//home//ec2-user//intern//intern-test//Sample Data//threads.xlsx")   # threads data_file
incident_df     = pd.read_excel("//home//ec2-user//intern//intern-test//Sample Data//Incidents.xlsx") # incident data_file

# re-arranging the header names
header_row              =       0
thread_df.columns       =       thread_df.iloc[header_row]
incident_df.columns     =       incident_df.iloc[header_row]
thread_df               =       thread_df.drop(header_row)
incident_df             =       incident_df.drop(header_row)

# rename the columns
thread_df.rename(columns={'Foreign Key':'Incident ID'}, inplace=True)
incident_df.rename(columns={'Category ID':'CategoryID'}, inplace=True)

# Selecting only solved threads for training the model
incident_df=incident_df[incident_df['Status']=='Solved']

# Merging the threads data file with incidents file on incident Id,where foreign key in thread data and selecting only required features
inc_thread_df=thread_df[["Incident ID","Text"]].merge(incident_df[["Incident ID","Status","Subject","CategoryID"]],on="Incident ID",how="right")

# In Category column there are rows with No value we will deselect all such valued rows for performing the model better
inc_thread_df=inc_thread_df[inc_thread_df['CategoryID']!='No Value']

# Dropping all null valued rows
inc_thread_df=inc_thread_df.dropna()

# Cleaning the text
inc_thread_df["Text"] = inc_thread_df["Text"].apply(lambda cw: cleaning_text(cw))
inc_thread_df["Text"] = inc_thread_df["Text"].apply(lambda cw: cleaning_text1(cw))
inc_thread_df["Text"] = inc_thread_df["Text"].apply(lambda cw: contraction_text(cw))

# Grouping them by incidents and appending same Incident ID "Text" into one
inc_thread_df['Text'] = inc_thread_df.groupby(['Incident ID'])['Text'].transform(lambda x : ''.join(str(x)))

# Droping duplicates
inc_thread_df = inc_thread_df.drop_duplicates()

# Combining the Text and subject field into text
inc_thread_df["Text"]=inc_thread_df["Subject"]+" "+inc_thread_df["Text"]

# Again Cleaning the text after appending the subject to text
inc_thread_df["Text"] = inc_thread_df["Text"].apply(lambda cw: cleaning_text(cw))
inc_thread_df["Text"] = inc_thread_df["Text"].apply(lambda cw: meaningless_words(cw))
inc_thread_df["Text"] = inc_thread_df["Text"].apply(lambda cw: cleaning_text1(cw))
inc_thread_df["Text"] = inc_thread_df["Text"].apply(lambda cw: contraction_text(cw))

# Create a new column 'Category_id' with encoded categories
inc_thread_df['category_id'] = inc_thread_df['CategoryID'].factorize()[0]
category_id_f2 = inc_thread_df[['CategoryID', 'category_id']].drop_duplicates() 

# Dictionaries for future use
category_to_id = dict(category_id_f2.values)
id_to_category = dict(category_id_f2[['category_id', 'CategoryID']].values)

# Text preprocessing - The text needs to be transformed to vectors so as the algorithms will be able make predictions
tfidf    = TfidfVectorizer(sublinear_tf=True, norm='l2',ngram_range=(1, 2), stop_words='english')
features = tfidf.fit_transform(inc_thread_df.Text)      # We transform each complaint into a vector
labels   = inc_thread_df.category_id

X = inc_thread_df['Text']         # Collection of Text
y = inc_thread_df['CategoryID']    # Target or the labels we want to predict

# training the model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,random_state = 42)
tfidf = TfidfVectorizer(sublinear_tf=True,ngram_range=(1, 3),stop_words='english')
fitted_vectorizer = tfidf.fit(X_train)
tfidf_vectorizer_vectors = fitted_vectorizer.transform(X_train)
model = LinearSVC().fit(tfidf_vectorizer_vectors, y_train)

# save the model with pickle 
with open('Category_model','wb') as f:
    pickle.dump(model,f)

with open('Category_vectorizer','wb') as f:
    pickle.dump(fitted_vectorizer,f)
    
print("-----------------------------Model saved-----------------------------------")
