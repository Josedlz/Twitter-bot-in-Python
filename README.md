# Twitter-bot-in-Python
Implementation of an automated Twitter bot

This project was done as a feature of the MVP developed by my team in the "Creamos Juntos" hackathon of BCP and Open Covid Perú. This is a bot of Twitter that uses real time streaming data from the platform using Twitter's API. 

It filters the tweets geographically and by certain keywords related to the pandemic in Perú. It then uses Google Translate's API to translate the tweets and performs a basic sentiment analysis using NLTK (Natural Language Processing Toolkit), a library for NLP of Python. In this case, we did this to recognize negative tweets related to the National Vaccination Program. It then stores the data in a Postgresql database for it to be processed in the future. 

It also includes an additional functionality of automatically uploading a tweet with variable text tagging tne users of the filtered tweets. In this case, we invite the users to our page for information in case we detected a negative commentary. 

To execute the bot, you need to modify the credentials of the database in the database.ini file, and also modify the ones in the main file for the Twitter API. The data will then be stored in the database that correspond to the replaced Postgresql credentials. 
