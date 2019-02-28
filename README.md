# Movie-Recommended-System
## overview

I build a movie recommender system using some memory-based recommendation algorithms. The system is deployed as a Telegram bot and a Web application server.

My recommender system consists of two parts:

1. A python script bot.py that continues to receive user messages from Telegram. When a message from a user is received, it sends request(s) to the recommendation server, and formats a response to be sent back to the user via Telegram.  
2. A python script app.py that implements an HTTP server using Flask. It should provide different routes to accept requests to different functions (see more details below).

The system should provide the following functions:

Accepts a new user identified by the chat_id
Returns a movie that has not yet been rated by a user so that the user can provide his/her rating on the movie
If enough ratings have been collected from a user, use the user-based collaborative filtering algorithm to generate recommended movies to the user
