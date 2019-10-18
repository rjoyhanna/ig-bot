# ig-bot
_Manages an Instagram account to incrementally grow its follow count_

## Current Features
- automated login
- follow specified user by username
- unfollow any sized batch of users

## Implementation
This repository makes use of the [Selenium web driver](https://github.com/SeleniumHQ/selenium/tree/master/py). It starts a Chrome browser and logs into the given Instagram account. It can then be used to follow a specified account, or unfollow a batch of users. All actions performed by the Bot are wrapped with sleep() statements to give Instagram the effect of being used by a human, and to wait for the page to be completely loaded. Since we need to give the impression of human mouse movements, and get around Instagram's rules for maximum pages unfollowed per minute, the unfollow process with take time. The good news is that it is completely automated so you can step away for a few hours and when you return your account will have unfollowed several hundred users.

## Getting Started
Clone the repository to your local machine and edit line 200 of `bot.py` to include your username and password:
```python
    ig_bot = InstagramBot('username', 'password')
```
Provide the bot with the preferred number of batches of users to unfollow on line 204:
```python
    for i in range(1, 100):
```
Then simply run `bot.py` in the terminal and let it run in the background on your PC.
