## Overview

Platformer Adventure is a 2D platformer built with Python and Pygame, designed to challenge players with skillful navigation and strategic timing. 

Players control a white rectangular hero, moving left or right, jumping across platforms, and collecting yellow coins to progress through three increasingly complex levels. The game introduces red patrolling enemies and a fast-moving enemy in Level 3, requiring precise movement to avoid game-ending collisions. A blue jump boost power-up in Level 3 enhances the player’s jump height, adding depth to platforming challenges. 

A timer tracks gameplay duration with two-decimal precision, and a restart option allows players to retry levels seamlessly. 

Developed for the Computer Science ATAR Year 12 Task 1, this project showcases object-oriented programming, robust collision detection, and a polished user interface, demonstrating both technical proficiency and creative game design.

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/daniellbaii/platformer-adventure.git
   cd platformer-adventure
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the game:
   ```bash
   python3 -m src.game
   ```

## Project Structure

- `assets/`: Game assets (images, sounds).
- `src/`: Source code for the game.
  - `game.py`: Main game loop and `GameManager` class.
  - `game_objects.py`: Classes for `Player`, `Platform`, `Enemy`, `FastEnemy`, `Coin`, `PowerUp`, and levels.
  - `constants.py`: Game constants (e.g., `SCREEN_WIDTH`, `PLAYER_JUMP_POWER`).
- `tests/`: Unit tests for game objects.
  - `test_game_objects.py`: Tests for game object behaviors.
- `docs/`: Testing screenshots and documentation images.

## Deliverable 3: Initial Prototype

### Functionality

- Player moves left/right with arrow keys, jumps with UP key (hold to repeat).
- Collision detection with platforms (ground and elevated).

### Testing Evidence

- **Unit Tests**:
  - File: `tests/test_game_objects.py`
  - Command:
    ```bash
    python3 -m unittest tests.test_game_objects -v
    ```
  - Results:
    - `test_player_jump`: Passed (jump sets `velocity_y` with gravity).
    - `test_gravity_application`: Passed (gravity increases `velocity_y`).
    - `test_horizontal_movement`: Passed (player moves with `PLAYER_SPEED`).
    - `test_collision_landing`: Passed (player lands on platform at `y=360`).

- **Screenshots**:
  - `docs/ground.png`: Player on ground platform.
  - `docs/jump.png`: Player mid-jump.
  - `docs/platform.png`: Player on elevated platform.

### Debugging Evidence

- **Bug**: Player stuck to platform sides when moving horizontally.
- **Cause**: Collision reset `velocity_x` to 0, overriding input.
- **Fix**: Adjusted `check_collisions` in `src/game.py` to only reset `velocity_x` if moving toward the platform.
- **Result**: Player moves away smoothly after hitting a side.

## Deliverable 4: Intermediate Project Update (Week 9)

### Overview

This update enhances the initial prototype (Deliverable 3) with additional gameplay mechanics and improved code quality, submitted as part of a structured development process for Task 1.

### Functionality

- **Player**: White rectangle, moves left/right (arrow keys), jumps (UP key), collects coins, jumps higher with power-up (Level 3 only).
- **Enemies**: Red rectangles, patrol platforms; game ends on contact with player. Fast enemy in Level 3 moves at double speed.
- **Coins**: Yellow rectangles, increase score when collected (displayed as "Coins: X/7").
- **Power-Up**: Blue rectangle in Level 3, doubles jump height for 5 seconds.
- **Levels**: Three levels with increasing complexity (2, 2, and 3 coins respectively).
- **UI**:
  - Score displayed as "Coins: X/7" in top-left corner.
  - Level indicator ("Level X") in top-right corner.
  - "Game Over" screen on enemy collision; press SPACE to restart level.
  - "You Win!" screen after collecting all coins; press SPACE to replay.
  - Restart option: Press 'R' to restart current level, with "Press R to Restart" text.
  - Timer: Tracks game time (to two decimal places), displayed at top-center during gameplay and on win screen; persists across deaths/restarts, stops on win, resets on replay.

### OOP Implementation

- **Base Class**: `GameObject` provides shared attributes (position, drawing) and methods.
- **Subclasses**: `Player`, `Platform`, `Enemy`, `FastEnemy`, `Coin`, `PowerUp` inherit from `GameObject`, using encapsulation for attributes (e.g., `velocity_x`, `collected`) and polymorphism in `update()` behaviors.

### Testing Evidence

- **Unit Tests**: 8 tests in `tests/test_game_objects.py` covering player jump, gravity, movement, collision, enemy patrolling, fast enemy movement, coin collection, and power-up collection.
- **Command**:
  ```bash
  python3 -m unittest tests.test_game_objects -v
  ```
- **Results**: All tests pass, verifying core and new functionality.

- **Screenshots**:
  - `docs/coin_initial.png`: Player and game objects in initial setup.
  - `docs/coin_collected.png`: Player after collecting a coin, score increases to 1.
  - `docs/enemy_initial.png`: Player on elevated platform before enemy collision.
  - `docs/gameover.png`: Game Over screen showing score and UI.

### Debugging Evidence

- **Bug**: Enemies moved beyond platform edges.
- **Fix**: Added boundary check in `Enemy.update()` to reverse `velocity_x` at platform limits.
- **Bug**: Initial import errors between game and test execution.
- **Fix**: Standardized execution with `python3 -m src.game` from root.

### Code Improvements

- **Error Handling**: Added try/except blocks for Pygame initialization and game execution.
- **Comments**: Included docstrings and inline comments for clarity in `GameManager` methods.

## Deliverable 5: Final Project

### Overview

The final version of Platformer Adventure builds on Deliverables 3 and 4, adding multiple levels, a fast enemy, a jump boost power-up, a persistent timer, and a restart option. It demonstrates advanced game mechanics, robust collision handling, and a polished UI for the Computer Science ATAR Year 12 Task 1.

### Functionality

- **Levels**: Three levels with unique layouts and backgrounds:
  - Level 1: 2 coins, 1 enemy, black background.
  - Level 2: 2 coins, 2 enemies, dark blue background.
  - Level 3: 3 coins, 1 fast enemy, 1 jump boost power-up, dark green background.
- **Player Mechanics**:
  - Move left/right (LEFT/RIGHT arrows), jump (UP arrow).
  - Collect coins (7 total) to progress through levels.
  - Collect jump boost power-up in Level 3 to double jump height for 5 seconds.
- **Enemies**:
  - Standard enemies patrol at 2 pixels/frame.
  - Fast enemy in Level 3 patrols at 4 pixels/frame; contact triggers "Game Over".
- **UI and Controls**:
  - Start screen: Press SPACE to begin.
  - Game Over: Press SPACE to restart current level.
  - Win screen: Press SPACE to replay from Level 1.
  - Restart: Press 'R' to restart current level, with "Press R to Restart" at top-center.
  - Score: "Coins: X/7" at top-left, resets correctly on "R" or death.
  - Level: "Level X" at top-right.
  - Timer: Shows "Time: X.XXs" at top-center, persists across deaths/restarts, stops on "You Win!", resets to 0.00 on replay.
- **Collision System**: Handles platform landing, enemy collisions (game over), coin collection (score increment), and power-up activation (jump boost).

### Testing Evidence

- **Unit Tests**:
  - File: `tests/test_game_objects.py`
  - Command:
    ```bash
    python3 -m unittest tests.test_game_objects -v
    ```
  - Results:
    - `test_player_jump`: Passed (jump applies `jump_multiplier`).
    - `test_gravity_application`: Passed.
    - `test_horizontal_movement`: Passed.
    - `test_collision_landing`: Passed.
    - `test_enemy_patrol`: Passed.
    - `test_fast_enemy_movement`: Passed (moves at 4 pixels/frame).
    - `test_coin_collection`: Passed.
    - `test_powerup_collection`: Passed (sets `jump_multiplier` to 1.5).

- **Screenshots**:
  - `docs/level3.png`: Level 3 with player, fast enemy, jump boost power-up, coins, timer, and "Press R to Restart".
  - `docs/winscreen.png`: Win screen with "You Win!", "Total Coins: 7/7", and final time (e.g., "Time: 30.45s").
  - `docs/start_screen.png`: Start screen that promots the user to press SPACE to start.
  - `docs/gameover_v2.png`: Second version of the game over screen.

### Debugging Evidence

- **Bug**: Power-up not rendering in Level 3.
- **Fix**: Added `power_ups` to `Level.get_objects()` and moved power-up to (300, 400) for visibility.
- **Bug**: Coin counter not resetting on 'R' restart, allowing >7/7 coins.
- **Fix**: Added `level_coin_counts[self.current_level_index] = 0` in `handle_events` for 'R' key.
- **Bug**: Timer continued incrementing on "You Win!" screen.
- **Fix**: Stored `final_time` in `check_collisions` for static display in "FINISHED" state.
- **Bug**: Timer didn’t reset to 0.00 on replay from "FINISHED".
- **Fix**: Reset `start_time` in `reset_level` for "FINISHED" state.

### Code Improvements

- **Modularity**: Added `LevelOne`, `LevelTwo`, `LevelThree` classes for level-specific configurations.
- **Robustness**: Fixed timer and coin counter edge cases for consistent behavior.
- **UI Clarity**: Added "Press R to Restart" and precise timer (two decimal places).

## Known Issues

- Timer text may overlap with score/level on smaller screens; adjustable in `GameManager.render`.
- No sound effects or sprites, as focus was on mechanics and UI.

## Future Improvements

- Add sound effects for jumps, coin collection, and power-up activation.
- Implement a high-score system to save best times.
- Introduce additional power-ups (e.g., speed boost, invincibility).
- Replace rectangles with sprite images for enhanced visuals.