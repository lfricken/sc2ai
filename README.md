# sc2ai

## Installation:
Install as package - python setup.py install
Use files from local repo - python setup.py develop

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
