# Platformer Adventure
A side-scrolling platformer game developed using Python and Pygame for the Computer Science ATAR Year 12 Task 1.

## Setup
1. Clone the repository: `git clone <repository-url>`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the game: `python src/game.py`

## Project Structure
- `assets/`: Game assets (images, sounds).
- `src/`: Source code for the game.
- `tests/`: Unit tests for game objects.
- `docs/`: Testing screenshots.

## Deliverable 3: Initial Prototype
### Functionality
- Player moves left/right with arrow keys, jumps with UP key.
- Collision detection with platforms implemented.

### Testing Evidence
- **Unit Tests**:
  - File: `tests/test_game_objects.py`
  - Command: `python3 -m unittest tests.test_game_objects -v`
  - Results:
    - `test_player_jump`: Passed (jump sets velocity_y correctly with gravity).
    - `test_gravity_application`: Passed (gravity increases velocity_y).
    - `test_horizontal_movement`: Passed (player moves right with PLAYER_SPEED).
    - `test_collision_landing`: Passed (player lands on platform at y=360).

- **Screenshots**:
  - `docs/ground.png`: Player on ground platform.
  - `docs/jump.png`: Player mid-jump.
  - `docs/platform.png`: Player on elevated platform.

### Debugging Evidence
- **Bug**: Player stuck to platform sides when moving horizontally.
- **Cause**: Collision reset `velocity_x` to 0, overriding input.
- **Fix**: Adjusted `check_collisions` in `src/game.py` to only reset `velocity_x` if moving toward the platform.
- **Result**: Player now moves away smoothly after hitting a side.