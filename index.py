import sys
answer = str(input("Do you want to add a tweet?(y/n) "))
if answer.lower() == "y":
    tweet = str(input("Enter your tweet "))
    tweet_id = int(input("Enter your twitter id "))
    string = "{\"text\": \"" + tweet + "\", \"id\": " + str(tweet_id) + "}"
    with open("tweets.json", "a") as myfile:
        myfile.write(string)
    print ("Tweet has been added! Clustering on all tweets now...")

else:
	print ("Clustering on all tweets now...")
	
