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

