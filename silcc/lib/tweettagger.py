import sys

from silcc.lib.tweetparser import TweetParser
from silcc.lib.basictagger import BasicTagger

class TweetTagger(object):

    @classmethod
    def tag(cls, tweet, debug=False):
        parsed_tweet = TweetParser.parse(tweet, debug=debug)
        text = parsed_tweet.get('text')
        tags = BasicTagger.tag(text)
        # Now add the hashtags from the parsing...
        hashtags = parsed_tweet.get('hashtags', [])
        # Strip off the '#'...
        hashtags = [h[1:] for h in hashtags]
        for tag in hashtags:
            if tag in tags: continue
            tags.append(tag)
        return tags

if __name__ == '__main__':
    tweet = sys.argv[1]
    tags = TweetTagger.tag(tweet)
    print tags






    
