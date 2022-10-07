# Discord Escape Room

This project is a discord bot meant to emulate "escape room" puzzles using discord's ui toolkit.

## Examples

## Setup
Ensure you have created a mongoDB Atlas cluster with an API key, as well as a discord bot user.
Run `setup.py` and provide your api token and your bot user token. After this, install the dependencies in a virtual environment, then run `src/escaperoom/main.py`.

## Building an escape room server
The key component to begin creating an escape room setup is the slash command `/initialize`. To begin, run this in the server you want to start an escape room. (Admin permissions are required.)

This should create a new category called `ESCAPE ROOM`, with 1 channel named `room-1`.
To create new channels, use `/newroom`. Each room will also have an associated role.

Puzzles are the main structural component of your escape room. You can create a new puzzle using `/newpuzzle`
