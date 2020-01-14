# chat-sentiment-analysis-service

## Link: https://chat-api-sentiment-analysis.herokuapp.com/

**Description:**  Bottle API developed in Python that allows you to create users and chats and write message in them. You can also analyze the sentiment of each chat (TextBlob library) and get a recommendation of other users based on what the user has written (sklearn).
All the data is stored in PostgreSQL in Heroku. The API is in a Docker image also deployed on Heroku.
 
I will practice in this project:
- API (bottle)
- TextBlob sentiment analysis
- Docker, Heroku and Cloud databases
- Recommender systems
​
## Goals achieved:
​​
- (L1🧐) Write an API in bottle just to store chat messages in a PosgreSQL database.
- (L2🥳) Extract sentiment from chat messages and perform a report over a whole conversation
- (L3😎) Deploy the service with docker to heroku and store messages in a cloud database.
- (L4🤭) Recommend friends to a user based on the contents from chat `documents` using a recommender system with `NLP` analysis.

​
## How to use this API:

- (GET) `/users` 
  - **Purpose:** Shows all users in DB
  - **Params:** Not needed
  - **Returns:** `user_id` and `usernames`
- (POST) `/user/create` 
  - **Purpose:** Create a user and save into DB
  - **Params:** `username` the user name
  - **Returns:** `user_id`
- (GET) `/user/<user_id>/messages`  
  - **Purpose:** Shows the history of messages for a specific user
  - **Returns:** json array all messages
- (GET) `/user/<user_id>/recommend`  
  - **Purpose:** Recommend friend to this user based on chat contents
  - **Returns:** json array with top 3 similar users
- (POST) `/chat/create` 
  - **Purpose:** Create a conversation to load messages
  - **Params:** Not needed
  - **Returns:** `chat_id`
- (GET) `/chat/<chat_id>/adduser` 
  - **Purpose:** Add a user to a chat, this is optional just in case you want to add more users to a chat after it's creation
  - **Params:** `user_id`
  - **Returns:** `chat_id`
- (POST) `/chat/addmessage` 
  - **Purpose:** Add a message to the conversation.
  - **Params:**
    - `user_id`: Chat to store message
    - `chat_id`: the user that writes the message
    - `text`: Message text
  - **Returns:** `message_id`
- (GET) `/chat/<chat_id>/list` 
  - **Purpose:** Get all messages from `chat_id`
  - **Returns:** json array with all messages from this `chat_id`
- (GET) `/chat/<chat_id>/showconv` 
  - **Purpose:** Get all messages from `chat_id` with the `usernames`and timestamps.
  - **Returns:** json array with all messages from this `chat_id`
- (GET) `/chat/<chat_id>/sentiment` 
  - **Purpose:** Analyze messages from `chat_id`. I use `TextBlob` sentiment analysis package for this task
  - **Returns:** json with all sentiments from messages in the chat
​
​
## Links - API dev in python
- [https://bottlepy.org/docs/dev/]
- [https://www.getpostman.com/]
​
## Links - NLP & Text Sentiment Analysis
- [https://textblob.readthedocs.io/en/dev/]
​
## Links - Heroku & Docker & Cloud Databases
- [https://docs.docker.com/engine/reference/builder/]
- [https://runnable.com/docker/python/dockerize-your-python-application]
- [https://devcenter.heroku.com/articles/container-registry-and-runtime]
- [https://devcenter.heroku.com/categories/deploying-with-docker]
- [https://www.heroku.com/postgres]