#! /usr/bin/env bash
#
echo "Starting test"
#
# Won't work for the first 2 challenge numbers
# Because of the different title naming conventions
# Expect it to work for Challenge #3 onwards
# I could just write a loop for this, but let's be honest.
# No one likes writing loops in bash.
#
./get-post.py 1 1
./get-post.py 1 2
./get-post.py 1 3
./get-post.py 2 1
./get-post.py 2 2
./get-post.py 2 3
./get-post.py 3 1
./get-post.py 3 2
./get-post.py 3 3