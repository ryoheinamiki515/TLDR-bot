import tweepy
from summarizer import create_TLDR
import time

with open("./passwords.txt", "r") as f:
    CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET = f.read().splitlines()

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

api = tweepy.API(auth)

FILE_PATH = "./last_seen.txt"

def get_last_seen(file_path):
    with open(file_path, "r") as f:
        last_seen = f.readline()
    return last_seen

def write_last_seen(file_path, last_seen_id):
    with open(file_path, "w") as f:
        f.write(str(last_seen_id))

def reply_to_tweets():
    mentions = api.mentions_timeline(since_id=get_last_seen(FILE_PATH), tweet_mode="extended")
    for i, mention in enumerate(mentions):
        mention_id = mention.id
        mention_text = mention.full_text
        mention_reply_to = mention.in_reply_to_screen_name
        user_name = mention.user.screen_name
        if i == 0:
            write_last_seen(FILE_PATH, mention_id)
        if "#tldr" in mention_text.lower() and mention_reply_to == "voxdotcom":
            status_id = mention.in_reply_to_status_id
            status = api.get_status(status_id, tweet_mode="extended")
            url = status._json["entities"]["urls"][0]["url"]
            create_TLDR(url)
            tldr_media = api.media_upload("./pil_text_font.png")
            api.update_status(
                status=f"@{user_name} This TL;DR is created using TextRank, an unsupervised extractive algorithm for summarization",
                media_ids=[tldr_media.media_id],
                in_reply_to_status_id=mention_id
                )
            print("Replied to Tweet")

while True:
    reply_to_tweets()
    time.sleep(15)