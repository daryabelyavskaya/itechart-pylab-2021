## itechart-pylab-2021
## Assigment
The assignment consists of a scrapper of reddit posts and a RESTful server. Python script using the Beautiful Soup library to collect data from the site www.reddit.com by posts in the Top -> This Month category. The Assignment application saves the parser data not directly to a database, but through a separate RESTful service available on http://localhost:8087/, which in turn provides a simple API for working with basic file operations. The service saves the result to database named 'posts'. The project can work with databases postgresql and mongodb.

## Requirements

#### python version > 3.6.0

#### libraries: requests, bs4, uuid1, selenium, dacite, dataclasses, decouple, psycopg2 (for postgresql), pymongo (for mongodb),

## Lauch
1. Download from a remote repository to your PC.
2. Install the required libraries.
3. Select the database you want to work with.
  #### Guide for PostgreSql:
     Run sql_utils.sql to create databases and table use command:
        $psql -f sql_utils.sql targetdatabase
     Change the environment variables DATABASE in file .env to POSTGRESQL and set your username as CLIENT and your password as PASSWORD.
  #### Guide for MongoDB:
    Run mongo.js to create databases and table use command:
        $mongo < mongo.js
     Change the environment variables DATABASE in file .env to MONGODB and set your username as CLIENT and your password as PASSWORD.
4. Enter $python3 server.py in your command line to start the server.
5. Enter $python3 main.py to load Reddit posts data on server.

## File .env
File .env has the next environment variables 
HOST,DATABASE, DATABASE_NAME, CLIENT, PASSWORD, PORT.
<<<<<<< HEAD

=======
>>>>>>> 03641df53de60beec8b6485104f7f7285798d763
