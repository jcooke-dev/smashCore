# smashCore
SmashCore is our capstone group project in UMGC CMSC495 (7383) Spring 2025.

## Pytest
Configure PyCharm for pytest
* Settings/Python Integrated Tools/Default Test Runner: pytest
* Run/Edit Configurations
* Add a new configuration, name it something like "pytests for tests"
* Point script path and working directory to the tests folder
* Add environment variable: PYTHONPATH=src
* Save
* In the project panel, right click on src. Mark Directory As: Sources Root
* Do the same for tests but mark it Test Sources Root

## Key Combinations

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

