# SmashCore
SmashCore is our capstone group project in UMGC CMSC495 (7383) Spring 2025.  Our goal is to develop a retro-style,   
simple, brick-breaking arcade game with modern enhancements.

## Developers
Justin Cooke  
Ann Rauscher  
Camila Roxo  
Justin Smith  
Rex Vargas

## Development Environment
We're developing SmashCore in Python, intending to target releases to Windows, macOS, and Linux platforms.  These are   
the specific tools and libraries we're using to create SmashCore (including the versions used during development):
* **Python 3.13.2** (https://www.python.org/)
* **JetBrains PyCharm 2024.3.5** - IDE (https://www.jetbrains.com/pycharm/)
* **pygame 2.6.0** - library of Python modules designed specifically for writing games (https://www.pygame.org/)
* **pytest 8.3.5** - a testing framework (https://pypi.org/project/pytest/)
* **pylint 3.3.6** - a static code analyzer (https://pypi.org/project/pylint/)
* **pydoc** - an automatic documentation generator (https://docs.python.org/3/library/pydoc.html)
* **bandit 1.8.3** - tool to scan all Python source files and generate a security report (https://pypi.org/project/bandit/)
* **PyInstaller 6.12.0** - a tool that helps package and distribute a Python application for desktop execution (https://pyinstaller.org/)
* **Nuitka 2.6.6** - compiles Python source files, data, and all dependencies into a single executable for simpler distribution (https://nuitka.net/)
* **pygbag 0.9.2** - tool that packages Python/pygame applications for running in a web browser (https://pypi.org/project/pygbag/)

## Configuration/Setup Instructions for Specific Libraries and Tools
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

## GitHub for Issue Tracking, Code Review, and Version and Change Control
We've created a public GitHub site to serve as our project's git repository:  
https://github.com/jcooke-dev/smashCore

This GitHub site provides much of the helpful project and code management support that helps us develop SmashCore quickly  
and with quality, but also transparency among our group members.  We're taking advantage of issue tracking, linked branches,  
pull requests, integrated code reviews, and controlled merges into our 'main', deployable code base branch.  GitHub 'Project  
Views' also aid us in visualizing our development load and expected timeline.

## Source Code Organization
SmashCore's code base is organized into separate folders for source code (\\src\\), assets (\\src\\assets\\), and tests (\\tests\\). We've  
ensured the primary abstract objects, as well as logical/functional providers, are broken into separate Python source files or  
modules.  You can browse our code base here: https://github.com/jcooke-dev/smashCore/tree/main/src

## Gameplay and Testing Considerations and Features
Player interaction with SmashCore is straightforward and requires both the mouse and keyboard at this stage of development.  In  
standard play, the player clicks buttons to choose from Click to Play, Restart Game, Try Again, Quit Game, etc.  The player must  
also launch the ball by pressing the Spacebar and can pause/unpause the game with the ESC key.  During gameplay, the paddle  
is controlled by horizontal mouse movement.  Keep the ball from falling below/past the paddle!

We've added some features to aid our development and game balance/testing/tweaking efforts.  Primarily, this is the **Dev Overlay**.  Access  
this with the **CTRL+d** key combination.  This allows you to see the various toggles and motion-influencing parameters.  These  
include the motion calculation model, the acceleration due to gravity, and a paddle impulse that causes the paddle to strike the ball  
with an upwards force.  All of these parameters are adjustable with the key combinations specified, even if the Developer Overlay  
is hidden.

### AutoPlay
One especially helpful feature is **AutoPlay** (enabled with **CTRL+a**).  With this turned on, the paddle will automatically  
follow the ball.  This is great for testing the standard gameplay, but also useful if you want to see how changing the motion  
parameters (like gravity and paddle impulse) affect gameplay.  It also helps when you're tired of playing well, but need to  
keep testing!

### Key Combinations
This is a list of all parameters that can be toggled/adjusted in game, along with their key combinations.

| Key Combo            | Action                                                                |
|----------------------|-----------------------------------------------------------------------|
| **CTRL + d**         | Toggle the Developer Overlay On/Off                                   |
| **CTRL + a**         | Toggle AutoPlay On/Off                                                |
| **CTRL + p**         | Increase the Paddle Impulse (vertical push against the ball)          |
| **CTRL + SHIFT + p** | Decrease the Paddle Impulse (vertical push against the ball)          |
| **CTRL + g**         | Increase the Gravity                                                  |
| **CTRL + SHIFT + g** | Decrease the Gravity                                                  |
| **CTRL + s**         | Increase the Speed Step (speed added to ball after breaking bricks)   |
| **CTRL + SHIFT + s** | Decrease the Speed Step (speed added to ball after breaking bricks)   |
| **CTRL + m**         | Cycles through motion calculation models (only SIMPLE_1 and VECTOR_1) |

