#! /usr/bin/env python3

# Schematic: evaluate from command line
# ./get-post.py [challengeNumber] [difficultyNumber]
# Will create a directory ./posts/challenge[challengeNumber]/[difficulty]
# Within the directory, create challenge.md with content from Reddit post
# From there, you can try to solve the problem within its own directory

import praw
import re
import os
import sys
import argparse

#==============================================================================
# Section 1: function to download a given post
#==============================================================================
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
        rightChallenge = bool(re.search(u'# *' + str(ch) + ' \[' , title))
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
        print('No results found for post ' + str(challengeNumber) + \
                ' at difficulty ' + str(difficultyNumber) + '. Please try again.')
        return False
    else:
        post = truePosts[0]
        title, url, body = post.title, post.url, post.selftext
        poster = u'/u/' + post.author.name
        
    # Now that we've gotten the post content, we should focus on parsing it
    # Then we can add it to our local file system
    
    filebody = u'#' + title + '\n' + poster + '\n' + url + '\n\n'+ body
    filename = u'challenge.md'
    subdir = u'challenge' + str(challengeNumber)
    subsubdir = str( re.search('\[(\w*?)\]', title).group(1) ) # The difficulty

    # Now use `os` to make dir `posts` if it doesn't exist
    # Then, create file ./posts/subdir/subsubdir/filename
    # Then write `filebody` to the file.

    # Are all of these necessary? Possibly not but won't risk overwrite
    if not os.path.isdir("./posts"):
        os.makedirs("./posts")
    if not os.path.isdir("./posts/" + subdir):
        os.makedirs("./posts/" + subdir)
    if not os.path.isdir("./posts/" + subdir + "/" + subsubdir):
        os.makedirs("./posts/" + subdir + "/" + subsubdir)
    
    os.chmod("./posts", 0o644) # Fix permission errors?
    os.chdir("./posts/" + subdir + "/" + subsubdir)    
    file = open(filename, 'w')
    file.write(filebody)
    file.close()
    print('\nSuccessfully wrote post to file!\nPost: ' + title + '\n' + url)
    
    return True
    
    
#==============================================================================
# Section 2: Parsing arguments to pass to GetPost()    
#==============================================================================

def ParseArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("challenge", help="Reddit post challenge number")
    parser.add_argument("difficulty", help="Difficulty setting. Accepts 1, 2, or 3")
    args = parser.parse_args()
    return args

#==============================================================================
# Execution
#==============================================================================
if __name__ == "__main__":   
    os.chdir(os.path.dirname(sys.argv[0])) # `pwd` is now script location

    args = ParseArguments()        
    challengeNumber = int(args.challenge)
    difficultyNumber = int(args.difficulty)
    
    GetPost(challengeNumber, difficultyNumber)