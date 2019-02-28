# Movie-Recommended-System
## Overview

I build a movie recommender system using some memory-based recommendation algorithms. The system is deployed as a Telegram bot and a Web application server.

My recommender system consists of two parts:

1. A python script bot.py that continues to receive user messages from Telegram. When a message from a user is received, it sends request(s) to the recommendation server, and formats a response to be sent back to the user via Telegram.  
2. A python script app.py that implements an HTTP server using Flask. It should provide different routes to accept requests to different functions (see more details below).

The system provides the following functions:

1. Accepts a new user identified by the chat_id
2. Returns a movie that has not yet been rated by a user so that the user can provide his/her rating on the movie
3. If enough ratings have been collected from a user, use the user-based collaborative filtering algorithm to generate recommended movies to the user  

 <div align=center><img src="https://github.com/XM-WANG/Movie-Recommended-System/blob/master/pic/system.png"/></div>
  
More details about how the system was implemented are described below.
## Dataset
We used a dataset commonly used in recommender systems research, the MovieLens 100K movie ratings dataset created by GroupLens at the University of Minnesota (https://grouplens.org/datasets/movielens/). We used the small dataset with 100,000 ratings.

The dataset consists of 100,000 ratings on different movies by the users of the MovieLens recommender system:

* 100,000 ratings (1-5) from 600 users on 9,000 movies
* Each user has at least 20 movies
* Data about the movies and the users

If you are interested in this dataset, please check the README file (http://files.grouplens.org/datasets/movielens/ml-latest-small-README.html)
## The Telegram Bot Script
The Telegram bot script bot.py is used to rely user input to the server, and the server's output back to the user.  

In this project, I create three commands for my boy(api reference:https://core.telegram.org/bots#6-botfather). The user can use these three commands to interact with your recommender system.  
* `/start`
* `/rate`
  * A command to ask the application to present a movie for rating. On reciving this command, the Telegram bot script could:  
   a. Send a request to the server's `/get_unrated_movie` API with the user's `chat_id`  
   b. On receiving the movie information from the server, would send the user two messages:
    * A message containing the name of the movie, and the URL to the movie's page on IMDB
    * A message asking for the user's rating on this movie, with a custom keyboard
  * When a movie rating is received, you should send a request to the server's /rate API to submit the rating
  * An example is shown below:
    
    <div align=center><img width="45%" src="https://github.com/XM-WANG/Movie-Recommended-System/blob/master/pic/rating.png"/></div>
      
* `/recommend`
    - A command to ask the application to recommend a list of movies based on previous ratings. On receiving this command, the Telegram bot script shoud:
        1. Send a request to the server's `/recommend` API to ask for the **top 3** recommended movies for this user.
        2. The server may return two different responses, depending on the number of ratings given by that user:
            - If the user has **10 or more** ratings, the server will return a list of recommended movies
            - If the user has **less than 10** ratings, the server will return an empty list
        3. Upone receiving the response from the server:
            - If the list is not empty, send the list of movies to the user in **separate messages** to the user. Each message contains the title and the URL of the movie's page on IMDB.
            - if the list is empty, send the following message to the user: **"You have not rated enough movies, we cannot generate recommendation for you"**.

**Hint**: You can refer to the [sample bot script](https://github.com/iems5780/1819t1/blob/master/assignments/assignment-3-sample-bot.py) to see how you can structure your handle function to handle commands from the users.

### The Application Server

The application server should be a **Flask application** that accepts **HTTP requests** on different routes.

You should load **ALL** user ratings when initializing the application. For example, you can create a **dictionary** for storing the user's ratings. The key is the user's ID, and the value is a **numpy array** containing the user's rating on different movies.

You may also have to load additional data in the application when it is started, such as the titles and IDs of the movies.

**Hint**: You can add attributes to the Flask application when initializing it, and then in the function of a route you can use `current_app` to get a reference to the application (see example below).

```python
from flask import Flask, current_app

app = Flask(__name__)

# Store something in the "data" attribute
# of the Flask application
app.data = "Some data"

@app.route('/')
def index():
    # Returns "Some data"
    return current_app.data
```

All the **routes** in your Flask application should receive **POST** requests with **JSON data**. They should also send out responses in **JSON format**.

Your Flask application should have the following **routes**:

* `/register`
    - An API for checking whether a user exists in the application
    - It receives JSON data in the form of<br/>`{"chat_id": "(chat ID of the telegram user)"}`
    - If the application has seen this chat ID before, the following JSON response:<br/>`{"exists": 1}`
    - If the application has not seen this chat ID before:
        - Creates a new user and initialize its item ratings to zeros
        - Return the following JSON response:<br/>`{"exists": 0}`
* `/get_unrated_movie`
    - An API for obtaining a movie that is **NOT yet** rated by the user
    - It receives JSON data in the form of<br/>`{"chat_id": "(chat ID of the telegram user)"}`
    - The function handling this API should randomly sample a movie that is not yet rated by the user, and return the movie ID, the title and the URL to the movie's page on IMDB in the following format:<br/>`{"id": 1, "title": "Toy Story (1995)", "url": "..."}`
    - Note that you may need to **generate the URL** of the movie's page using the movie's ID in the dataset
* `/rate_movie`
    - An API for submitting a movie rating form a user
    - The function handling this API should updating the array of movie ratings of the given user with the rating provided
    - It should accept JSON data in the following format:<br/>`{"chat_id": "...", "movie_id": 1, "rating": 5}`
    - On updating the data in the application, it should return the following JSON response:<br/>`{"status": "success"}`
* `/recommend`
    - An API for generating recommended movies for a given user
    - The function handling this API should use the **user-based collaborative filtering** approach to compute the predicted ratings of all movies, and return the **top N** movies as specified in the request JSON
    - **Note**: the API should return an **empty list** if the number of movies rated by the user is **less than 10**
    - The API expects the following JSON input data:<br/>`{"chat_id": "...", "top_n": 3}`
    - It should return the list of movies in the following format:

```javascript
{
    "movies": [
        {
            "title": "...",
            "url": "..."
        },
        {
            "title": "...",
            "url": "..."
        },
        ...
    ]
}
```

**Note:** We DO NOT use a database in this assignment. Hence, if you restart the application, all the users' ratings will be gone (except, of course, the ratings from the MovieLens dataset). To facilitate testing, you can consider adding ratings to your own Telegram user (check the "chat ID" of yourself) when the application starts.

## What to Submit

You should prepare **two files** to be submitted for this assignment:
* **bot.py**: the script in which you implement the Telegram bot
* **app.py**: the script in which you implement the Flask application for movie recommendation

You should put these two files in a folder named <student_id>_assignment3 (e.g. 12345678_assignment3), and compress it into a zip file (e.g. 12345678_assignment3.zip). Submit the compressed file to Blackboard.

 
 
