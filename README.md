# SmashCore
SmashCore is our capstone group project in UMGC CMSC495 (7383) Spring 2025.  Our goal is to develop a retro-style, simple, brick-breaking arcade game with modern enhancements.

## Developers
Justin Cooke  
Ann Rauscher  
Camila Roxo  
Justin Smith  
Rex Vargas

## Gameplay and Testing Considerations and Features
> [!NOTE]
To play SmashCore, you must **install Python (tested with 3.13.2) and the pygame library (tested with 2.6.0)**.  We've installed and used many more libraries, but those are only needed when developing this game (and are described below).

Player interaction with SmashCore is straightforward and requires both the mouse and keyboard at this stage of development.  In standard play, the player clicks buttons to choose from Click to Play, Restart Game, Try Again, Quit Game, etc.  The player must also launch the ball by pressing the Spacebar and can pause/unpause the game with the ESC key.  During gameplay, the paddle is controlled by horizontal mouse movement.  Keep the ball from falling below/past the paddle!

We've added some features to aid our development and game balance/testing/tweaking efforts.  Primarily, this is the **Dev Overlay**.  Access this with the **CTRL+d** key combination.  This allows you to see the various toggles and motion-influencing parameters.  These include the motion calculation model, the acceleration due to gravity, and a paddle impulse that causes the paddle to strike the ball with an upwards force.  All of these parameters are adjustable with the key combinations specified, even if the Developer Overlay is hidden.

### AutoPlay
One especially helpful feature is **AutoPlay** (enabled with **CTRL+a**).  With this turned on, the paddle will automatically follow the ball.  This is great for testing the standard gameplay, but also useful if you want to see how changing the motion parameters (like gravity and paddle impulse) affect gameplay.  It also helps when you're tired of playing well, but need to keep testing!

### Key Combinations
This is a list of all parameters that can be toggled/adjusted in game, along with their key combinations.

| Key Combo            | Action                                                                  |
|----------------------|-------------------------------------------------------------------------|
| **CTRL + d**         | Toggle the Developer Overlay On/Off                                     |
| **CTRL + a**         | Toggle AutoPlay On/Off                                                  |
| **CTRL + p**         | Increase the Paddle Impulse (vertical push against the ball)            |
| **CTRL + SHIFT + p** | Decrease the Paddle Impulse (vertical push against the ball)            |
| **CTRL + g**         | Increase the Gravity                                                    |
| **CTRL + SHIFT + g** | Decrease the Gravity                                                    |
| **CTRL + s**         | Increase the Speed Step (speed added to ball after breaking bricks)     |
| **CTRL + SHIFT + s** | Decrease the Speed Step (speed added to ball after breaking bricks)     |
| **CTRL + m**         | Cycles through motion calculation models (only SIMPLE_1 and VECTOR_1)   |
| **CTRL + =**         | (the '+' key) Increase the overall volume                               |
| **CTRL + -**         | Decrease the overall volume                                             |
| **CTRL + l**         | Cycles through all available levels (can use to force load a new level) |


## Development Environment
We're developing SmashCore in Python, intending to target releases to Windows, macOS, and Linux platforms.  These are the specific tools and libraries we're using to create SmashCore (including the versions used during development):
* **Python 3.13.2** (https://www.python.org/)
* **JetBrains PyCharm 2024.3.5** - IDE (https://www.jetbrains.com/pycharm/)
* **pygame 2.6.0** - library of Python modules designed specifically for writing games (https://www.pygame.org/)
* **pytest 8.3.5** - a testing framework (https://pypi.org/project/pytest/)
* **pylint 3.3.6** - a static code analyzer (https://pypi.org/project/pylint/)
* **pdoc 15.0.3** - an automatic documentation generator (https://pdoc.dev/)
* **bandit 1.8.3** - tool to scan all Python source files and generate a security report (https://pypi.org/project/bandit/)
* **pickle** - library to support Python object serialization (https://docs.python.org/3/library/pickle.html)
* **PyInstaller 6.12.0** - a tool that helps package and distribute a Python application for desktop execution (https://pyinstaller.org/)
* **pygbag 0.9.2** - tool that packages Python/pygame applications for running in a web browser (https://pypi.org/project/pygbag/)

## Configuration/Setup Instructions for Specific Libraries and Tools

### Dependencies

This project uses a requirements.txt file to manage dependencies. To install the required libraries, including Pygame and others, run this command in your terminal:                       
pip install -r requirements.txt

### Pytest
Configure PyCharm for pytest
* Settings/Python Integrated Tools/Default Test Runner: pytest
* Run/Edit Configurations
* Add a new configuration, name it something like "pytests for tests"
* Point script path and working directory to the tests folder
* Add environment variable: PYTHONPATH=src
* Save
* In the project panel, right click on src. Mark Directory As: Sources Root
* Do the same for tests but mark it Test Sources Root

To view the unit test code coverage, pycov can be used by running the following command to generate HTML output detailing the test coverage:

   ```PYTHONPATH=src pytest --cov=src tests/ --cov-report html```

### pdoc
To use pdoc to auto-generate a set of HTML files for navigating the program code:
* Ensure pdoc (not pdoc3) is installed
* Add this new environment variable if it doesn't already exist (User or System is fine):
  * PYTHONPATH = [absolute path on your machine to the root SmashCore src\ directory] (for example: ```e:\Users\justin\Documents\UMUC\CMSC495\code\github\smashCore\src```)
* From the PyCharm terminal, run this command from your project/repo root (for example: ```e:\Users\justin\Documents\UMUC\CMSC495\code\github\smashCore```): ```pdoc -o ./docs src/```
* The documentation will be generated in the ```.docs``` folder
* Note that once any documentation changes are merged into the `main` branch, they'll be available here: https://jcooke-dev.github.io/smashCore/src.html

## Building the Source Code for Distribution
Download the full source code directory structure from GitHub: https://github.com/jcooke-dev/smashCore
After installing PyInstaller, in your working Python IDE's terminal window (ensuring the Python scripts are available), execute the OS-specific build script for your current OS in the project root directory:
* bundle_mac.sh
* bundle_linux.sh
* bundle_windows.ps1

This will generate the single executable file for your OS and can be found in the ./dist/ sub-directory.

## GitHub for Issue Tracking, Code Review, and Version and Change Control
We've created a public GitHub site to serve as our project's git repository:  
https://github.com/jcooke-dev/smashCore

This GitHub site provides much of the helpful project and code management support that helps us develop SmashCore quickly and with quality, but also transparency among our group members.  We're taking advantage of issue tracking, linked branches, pull requests, integrated code reviews, and controlled merges into our 'main', deployable code base branch.  GitHub 'Project Views' also aid us in visualizing our development load and expected timeline. We are also taking advantage of Workflows in GitHub to run unit tests, pylint, and bandit on pull request. This ensures that any pull request merged into the main code branch has been had unit tests, pylint, and bandit run against it. 

## Source Code Organization
SmashCore's code base is organized into separate folders for source code (\\src\\), assets (\\src\\assets\\), and tests (\\tests\\). We've ensured the primary abstract objects, as well as logical/functional providers, are broken into separate Python source files or modules.  You can browse our code base here: https://github.com/jcooke-dev/smashCore/tree/main/src

## Source Code API/Documentation
You can view the source code API, automatically generated with pdoc, here: https://jcooke-dev.github.io/smashCore/src.html 


## Credits

**Sound Effects and Music:**
* Free sound effects obtained from [Mixkit](https://mixkit.co/free-sound-effects/game/).

**Game Logo:**
* Designed by [Camila Roxo]
 
**Volume Botton Layout:**
* Designed by [Rex Vargas]

**Game Art:**
* Designed by [Justin Smith]
