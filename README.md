# TLDR-bot

## Description
Twitter bot that replies with a TL;DR (Too Long, Didn't Read) of a news article. Currently works with Vox articles (@voxdotcom). 

## Demo
### Step 1: Select a Vox article

### Step 2: Reply to it and tag @TLDRNews2 and write a message that contains #tldr

### Step 3: Wait ~5-10 seconds and get a TL;DR reply from the bot

## Algorithm
Step 1: Get new user mentions (tracked using last_seen.txt file)

Step 2: For each mention, check if the criteria are met (the tweet is a reply to a Vox article and the reply contains #tldr)

Step 3: If the criteria is met, pull the text data from the Vox article using BeautifulSoup

Step 4: Clean the text data using NLTK

Step 5: Describe the sentences numerically using Tf-idf (sklearn)

Step 6: Calculate scores for each sentence using TextRank

Step 7: Choose the top 8% quartile of sentences based on scores

Step 8: Sort the sentences in chronological order so that the writing makes sense

Step 9: Create an image containing the extracted text (to get around Twitter's character count limit)

Step 10: Upload the image to Twitter

Step 11: Create a new reply to the mention with the image attached
