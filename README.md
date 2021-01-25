## itechart-pylab-2021
## Assigment
The assignment consists of a scrapper of reddit posts and a RESTful server. Python script using the Beautiful Soup library to collect data from the site www.reddit.com by posts in the Top -> This Month category. The Assignment application saves the parser data not directly to a file, but through a separate RESTful service available on http://localhost:8087/, which in turn provides a simple API for working with basic file operations. The service saves the result to a text file named reddit-YYYYMMDD.txt

## Requirements

#### python version > 3.0.0

#### libraries: requests, bs4, uuid1, selenium

## Lauch
1. Download from a remote repository to your PC.
2. Install the required libraries.
2. Enter $pythoт3 server.py in your command line to start the server.
3. Enter $python3 main.py to load Reddit posts data on server.
