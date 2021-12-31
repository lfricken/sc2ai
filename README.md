# sc2ai

A collection of StarCraft 2 AI written in python. Some will actually attempt to play the game, some use deep learning via Tensorflow to do predictions.

Here is an example of a win prediction model. It was trained on replays and is just based on the number of each unit that a player has. Here is it's prediction over the course of a game. It has no concept of unit location on the map though.

![Failed to load. Click on win_odds_zerg.png.](https://raw.githubusercontent.com/lfricken/sc2ai/master/win_odds_zerg.png "Score is in game score aggregate of resources and units.")

## Installation:
Install the following in order:
* [Python 3.6.x](https://www.python.org/downloads/)
* [pip](https://pip.pypa.io/en/stable/installing/)
* [tensorflow-gpu](https://www.tensorflow.org/install/gpu) or [tensorflow](https://www.tensorflow.org/install/pip) if you're lame. Do **_not_** attempt to build from source on Windows in either case.
* [Pycharm](https://www.jetbrains.com/pycharm/download/#section=windows)
* Upon cloning the repository, run `update-packages.bat`, which will update other dependencies used by this repository. It relies on pip working from the command-line.

Setting Up Pycharm:
* File > Import Settings > sc2ai directory > pycharm_settings.jar
* Open Project > sc2ai directory
* [Mark the working folder inside `\custom` as source root.](https://stackoverflow.com/questions/31432976/pycharm-not-recognizing-packages-even-when-init-py-exits) You will want to unmark it if you move to another custom folder.
* Run > Templates > Python > 
  * Target To Run: Script path
  * Python interpreter: Python 3.6.x (pointing at your python.exe file)
