## Building Event Extraction and Trending Framework for Twitter


This is my capstone project for the Data Science Immersive at General Assembly. 

In this project, my goals are:
  1. Set up real-time Data Collection process and Data Infrastructure
  2. Examine different Natural Language Processing tools on collected tweets
  3. Create A|B Testing Model on similarity comparison
  4. Use Time Series Modeling to catch the trends
  5. Tuning hyperparameters for model improvement

To test my framework:
  1. I collected and cleaned over 1.5 million tweets from uing TwitterStream API
            
            /lib/get_tweets.py
  2. Create scheduled and on demand LSA processing for text vectrozation
            
            /ipynb/01_Fit_pipeline_TfiDf_SVD.ipynb
            
  3. Event and Trend Detection using Cosine Similarity and ARIMA modeling
            
            Event extracting using TFIDF and SVD
              /ipynb/03_Tweets_Modeling_CosineSim_AB_Test_SVD.ipynb
            
            Hashtag Time Series Modeling 
              /ipynb/05_Hashtags_Modeling_WhatsTrending.ipynb
        
#### Technologies used in the project
 1. Python
 2. TwitterStream API
####   Data Management
  1. postgres
  2. redis
####   Modeling
  1. NLP (LSA): SAPCY | TFIDF |SVD | Count Vectorizer 
  2. Cosine Similarity
  3. ARIMA Modeling
  
#### For a more detailed description of this project see /doc/Twitter_capstone_GA_Profile.pdf
