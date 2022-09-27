# Introduction

This project is intended to create a simple chatbot app for a moving company using an untrained openai model.

The bot is designed to answer questions, collect user information and calculate the price based on working hours.

* To run the bot you will need to have an openai account and your openai api key.


# Installation

First clone the project
```
git clone https://github.com/Razlif/moverbot.git
```
Next install the required packages
```
pip3 install --user -r requirements.txt
```

# Openai Credentials

To use the program you will need your openai api key.

To get it, follow these steps:

Go to the [spotify developer section](https://developer.spotify.com/dashboard/applications)

1. Log into your Spotify account.

2. Click on ‘Create an app’.

3. Enter an ‘App name’ and an ‘App description’ and mark the checkboxes.

4. After the app is created you will see your ‘Client Id’. Then can click on ‘Show client secret` to reveal your ’Client secret key’.

* The spotify user name can be located in the the url for the user's main page for example, https://open.spotify.com/user/< user name >


# Setting up environment variables

Next edit the .env file in the project folder and include the spotify credentials.

.env:
```
SECRET_KEY = "Your openai api key"
```

# Updating the company information and settings

Now you can run the python script directly from the command line
```
python3 spotify_to_mp3.py
```
This will prompt you to enter the download path and the spotify username that has the playlists to download.

you can also input the arguments directly in the command line:
```
python3 spotify_to_mp3.py --path <download path for the mp3 folders> --uname <the spotify username>
```

# The conversation flow

# Running the chatbot

# Notes