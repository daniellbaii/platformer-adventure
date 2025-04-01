# Platformer Adventure
A side-scrolling platformer game developed using Python and Pygame for the Computer Science ATAR Year 12 Task 1.

## Setup
1. Clone the repository: `git clone https://github.com/daniellbaii/platformer-adventure.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the game: `python3 -m src.game`

## Project Structure
- `assets/`: Game assets (images, sounds).
- `src/`: Source code for the game.
- `tests/`: Unit tests for game objects.
- `docs/`: Testing screenshots.

## Deliverable 3: Initial Prototype
### Functionality
- Player moves left/right with arrow keys, jumps with UP key (hold to repeat).
- Collision detection with platforms (ground and elevated).

### Testing Evidence
- **Unit Tests**:
  - File: `tests/test_game_objects.py`
  - Command: `python3 -m unittest tests.test_game_objects -v`
  - Results:
    - `test_player_jump`: Passed (jump sets velocity_y with gravity).
    - `test_gravity_application`: Passed (gravity increases velocity_y).
    - `test_horizontal_movement`: Passed (player moves with PLAYER_SPEED).
    - `test_collision_landing`: Passed (player lands on platform at y=360).

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
- **Player**: White rectangle, moves left/right (arrow keys), jumps (UP key), collects coins.
- **Enemies**: Red rectangles, patrol the elevated platform; game ends on contact with player.
- **Coins**: Yellow rectangles, increase score when collected (displayed as "Coins Collected: X").
- **UI**: Score displayed in top-left corner; "Game Over" text on enemy collision.

### OOP Implementation
- **Base Class**: `GameObject` provides shared attributes (position, drawing) and methods.
- **Subclasses**: `Player`, `Platform`, `Enemy`, `Coin` inherit from `GameObject`, using encapsulation for attributes (e.g., `velocity_x`, `collected`) and polymorphism in `update()` behaviors.

### Testing Evidence
- **Unit Tests**: 6 tests in `tests/test_game_objects.py` covering player jump, gravity, movement, collision, enemy patrolling, and coin collection.
- **Command**: `python3 -m unittest tests.test_game_objects -v`
- **Results**: All tests pass, verifying core and new functionality.

- **Screenshots**:
  - `docs/coin_initial.png`: Player and other game objects in their inital setup.
  - `docs/coin_collected.png`: Player immediately after colliding with the coin, score increases to 1.
  - `docs/enemy_initial.png`: Player on elevated platform before colliding with enemy.
  - `docs/gameover.png`: Game Over screen that displays both the score and game over UIs.

### Debugging Evidence
- **Bug**: Enemies moved beyond platform edges.
- **Fix**: Added boundary check in `Enemy.update()` to reverse `velocity_x` at platform limits.
- **Bug**: Initial import errors between game and test execution.
- **Fix**: Standardized execution with `python3 -m src.game` from root.

### Code Improvements
- **Error Handling**: Added try/except blocks for Pygame initialization and game execution.
- **Comments**: Included docstrings and inline comments for clarity in `GameManager` methods.