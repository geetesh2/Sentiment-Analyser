import re
import string
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from app import comments

def clean_text(text):
    text = text.lower()
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'http\S+', '', text)
    text = ' '.join(word for word in text.split() if word not in stopwords.words('english'))
    return text

clean_comments = []
for x in range(len(comments)):
 clean_op = clean_text(comments[x])
 clean_comments.append(clean_op)

# print(clean_comments)