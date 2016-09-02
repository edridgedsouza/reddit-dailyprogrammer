#! /usr/bin/env python3

# Schematic: evaluate from command line
# ./get-post.py -c [challengeNumber] -d [difficultyNumber]
# Will create a directory ./posts/challenge[challengeNumber]/[difficulty]
# Within the directory, create post.md with content from Reddit post
# From there, you can try to solve the problem within its own directory

# Hard-code these in for quick eval. Add in argparse when functional

import praw
import re
import os
#import argparse

def GetPost(challengeNumber, difficultyNumber):
    user_agent = "Edridge D'Souza get-post script for /r/dailyprogrammer"
    r = praw.Reddit(user_agent=user_agent)
    sub = 'dailyprogrammer'
    
    def BuildQuery(ch, diff):
        challenge = u'Challenge #' + str(ch)
        difficulty = {
            1: u'easy',
            2: u'(med OR intermediate)',
            3: u'(hard OR difficult)'    
        }[diff]
        return challenge + ' ' + difficulty   
    query = BuildQuery(challengeNumber, difficultyNumber)
    
    # Return most relevant submissions to search, then double-check titles
    subsearch = [i for i in r.search(query, subreddit = sub, sort = u'relevance')]
    
    # Double-check post title contains right challenge number and difficulty
    def VerifyPost(redditobject, ch, diff):
        title = redditobject.title.lower()
        rightChallenge = bool(re.search(str(ch), title))
        difficulty = {
            1: u'easy',
            2: u'(medium|intermediate)',
            3: u'(hard|difficult)'
        }[diff]
        
        rightDiff = bool(re.search(str(difficulty), title))
        return rightChallenge and rightDiff
        
    truePosts = [i for i in subsearch if VerifyPost(i, challengeNumber, difficultyNumber)]
    
    # Select just the first (i.e. most relevant) post
    if len(truePosts) == 0:
        print("No results found. Please try again.")
        return False
    else:
        post = truePosts[0]
        title, url, body = post.title, post.url, post.selftext
    
    # Now that we've gotten the post content, we should focus on parsing it
    # Then we can add it to our local file system
    
    filebody = u'#' + title + '\n' + url + '\n\n'+ body
    filename = u'challenge.md'
    subdir = u'challenge' + str(challengeNumber)
    subsubdir = str( re.search('\[(\w*?)\]', title).group(1) ) # The difficulty

    # Now use `os` to make dir `posts` if it doesn't exist
    # Then, create file ./posts/subdir/subsubdir/filename
    # Then write `filebody` to the file.

    
    
#==============================================================================
# Execution
#==============================================================================
if __name__ == "__main__":
    challengeNumber = 255
    difficultyNumber = 3
    GetPost(challengeNumber, difficultyNumber)

    