from flask import Flask, render_template, request
import flask
import json
app = Flask(__name__)

@app.route('/',methods=['POST','GET'])
def hello_world():
   return render_template('index.html')


@app.route('/graph',methods=['POST','GET'])


@app.route('/login',methods=['POST','GET'])
def valid():
   if request.method == 'POST':

      link = request.form['url']
      link = link[-11:]
      from googleapiclient.discovery import build
      from googleapiclient.errors import HttpError



      #Fetching the comments from video
      DEVELOPER_KEY = 'AIzaSyB_BlPdj1MyiTn91768-fycRn86sphu3AY'
      YOUTUBE_API_SERVICE_NAME = 'youtube'
      YOUTUBE_API_VERSION = 'v3'

      def get_comments(video_id):
         youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
         results = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            textFormat='plainText',
            maxResults = 1000
         ).execute()
         comments = []
         for item in results['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(comment)
         return comments
      comments = get_comments(link)

      #Cleaning the comments
      import re
      import string
      import nltk
      nltk.download('stopwords')
      from nltk.corpus import stopwords

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


      #Analysing
      nltk.download('vader_lexicon')
      from nltk.sentiment.vader import SentimentIntensityAnalyzer

      polarity = []
      def get_sentiment(text):
         sid = SentimentIntensityAnalyzer()
         sentiment_scores = sid.polarity_scores(text)
         polarity.append(sentiment_scores['compound'])
         if sentiment_scores['compound'] >= 0.05:
            return 'positive'
         elif sentiment_scores['compound'] <= -0.05:
            return 'negative'
         else:
            return 'neutral'

      final_data = []
      for x in range(len(clean_comments)):
         result = get_sentiment(clean_comments[x])
         final_data.append(result)


      #visulalising
      import matplotlib.pyplot as plt

      pos_num = 0
      neg_num = 0
      neu_num = 0
      for x in final_data:
         if x == "positive":
            pos_num += 1
         elif x == "negative":
            neg_num += 1
         elif x == "neutral":
            neu_num += 1
      # Sample sentiment analysis results

      data = {'Emotion' : 'Count',"positive": pos_num, "negative": neg_num, "neutral": neu_num}
      

      return render_template('graph.html',data=data)

if __name__ == '__main__':
    
    
   app.run(debug = True)
   