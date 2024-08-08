# GRIDSHOT50

#### **The original idea is from [Aimlabs's Gridshot](https://www.youtube.com/watch?v=eIKA8XQ4p_Q), a training exercise for FPS game players to improve their speed and precision. This project is a simple recreation of that idea, simulating the mechanism with `Python` using the `pygame-ce` library.**
#### Project demo: <https://youtu.be/E27TDOups0E>

## Introduction

### Running the game
The game should be run from the `~/project` directory, via `python project.py`. It needs to be executed locally, as cloud-based environments do not support external displays for the game.

Running the game requires the `pygame-ce` library. If it is not installed yet, run `pip install pygame-ce`.

After successfully running the game, click anywhere on the screen to start playing.

### How to play
*The goal is to shoot as many targets as possible within a period of time (default: 30 seconds). Simply left-click to shoot.*

**Shot targets** disappear and respawn somewhere else on the screen. The number of targets on the screen is fixed (default: 3). A successful shot adds `base score + speed bonus` to your score.

**Speed bonus** is rewarded if the interval between two hit shots is shorter than the bonus interval (default: 1000 milliseconds). The shorter the interval between two precise shots, the more bonus is given: `speed bonus =  10x base score * (bonus interval - interval) / bonus interval`.

**Precision matters!** Any missed shot will result in a score penalty (the penalty is fixed at 10x the base score, so a missed shot will take away more points than a perfect shot awards).

### Saving results
Any high score will be automatically saved, which you can later view by pressing `TAB` from the main screen. If you also want to save a non-high score, press `S` after the round ends.

**Deleted** results cannot be restored!

### Settings
The default settings are balanced, but they can be adjusted in the settings screen by pressing `T` from the main screen.

**Annoying alert**: _Modifying any settings will delete all saved results. This ensures that all results on the scoreboard are from the same settings._

Here is a short description of the settings options:
- **Timer**: Determines how long a round lasts.
- **UI details**: Off for a minimal and less-distracting in-game display.
- **Number of targets**: How many targets spawn on the screen simultaneously.
- **Edge**: The size of the grid of targets. A smaller size puts targets closer (and makes them easier to shoot).
- **Base score** and **Bonus interval**: Used for result calculation.

If changes are made, the game needs restarting (by pressing `R`) to apply them. A ~~annoying~~ reminding alert will stay on the screen until you restart (the game will still run normally).

## Code explanation

### Obstacles
The mechanism is simple, but the implementation is quite challenging. Here are some main things I had to ~~suffer~~ overcome:
- How to use `pygame` (hardest part)
- Write reusable code and avoid repetition
- Avoid circular imports or using magic numbers
- (Advanced) File I/O for loading and saving game data

### project.py and test_project.py
After finishing the project, I realized it was not possible to execute `pytest` effectively for objects, which I use for almost everything in my project. Instead of restructuring, I factored out some crucial functions and put them to the test to ensure they work as expected.

These files were created after everything else was done. The purpose is to run the game and satisfy the requirements.

### do_not_modify.py
This file contains all the parameters used in the game. Any unexpected modification might lead to weird behaviors. Originally, I intended to let users modify this file directly to adjust the game's settings. But I later came up with a better design, allowing users to dynamically adjust settings in the game without touching any part of the code (hence the file name). When the game runs, this file is executed first, loading all the modules and constants required.

The `load_settings` function loads custom settings if they exist, or the `default_settings` in the file. A `data` directory is also created (if not yet) to ensure file I/O works as expected.

A list of `GRID_POS` is calculated, containing screen coordinates to spawn targets on.

### assets.py
This file contains classes for objects used in the game.

`Target` object includes the graphic (red circle) and the hitbox used to detect collisions.

`TextRender` creates text on the screen.

`ModifyButton` allows users to adjust settings dynamically. It interacts with changes from user input and returns the value once the settings are saved.

### game.py
Consists of `Game` and `GameState`, which are the backbone of the game, initializing and allowing the game to run with multiple screens without interrupting each other. These objects constantly listen to events from objects in `states.py` and behave accordingly.

### states.py
The most complex part of the project, containing all the states (scenes) of the game as objects. Every object has a `run()` method, which is called continuously inside the game loop.

`Start` object has `main_menu()`, allowing users to navigate using keyboard input.

`Play` object is the scene where the game happens. `spawn_targets()` and `shoot_target()` operate the game, while `return_results()` constantly updates and returns the results as a `dict` value.

`Result` object shows detailed stats of the round via `stats_display()`. It also allows users to save results with `save_result()`, or automatically saves them if they are a high score. The results are loaded when the object is initialized. It also has functions to handle events after a round finishes.

`ScoreBoard` inherits from `Result`, displays (a maximum of 20) saved results, and the average of them.

`Settings` allows users to dynamically adjust settings in the game or restore them to default.
