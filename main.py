import listen
import tweepy


streamListener = listen.StreamListener()
stream = tweepy.Stream(auth=listen.api.auth, listener=streamListener,tweet_mode='extended')
with open("out.csv", "w", encoding='utf-8') as f:
    f.write("date,user,is_retweet,is_quote,text,quoted_text\n")
tags = ["vacunación","Sinopharm", "minsa", "Pfizer","pandemia", "AstraZeneca", "Covax", "vacunas", "vacunacion","vacunagate","COVIDー19","EsSaludTeInforma", "vacuna"]
stream.filter(track=tags, languages=['es'], locations=[-16.94, -79.47, -2.59, -71.078])
