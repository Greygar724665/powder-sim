# Powder Simulation

A simple but engaging powder physics simulation built with Python and Pygame. Watch sand particles fall and interact with realistic gravity-based physics!

## What it does

This simulation creates a grid-based physics engine where sand particles:
- Fall downward due to gravity
- Slide diagonally when blocked
- Have natural color variations for realistic appearance
- Update in real-time with smooth animation

## Features

- **Realistic Physics**: Sand particles check for obstacles and fall naturally
- **Dynamic Movement**: Particles slide left or right when they can't fall straight down
- **Visual Variety**: Each sand grain has slight color variations for a natural look
- **Real-time Simulation**: Smooth 20 FPS animation with proper physics timing

## Requirements

- Python 3.x
- Pygame library

## Installation

1. Clone or download this repository
2. Install pygame:
   ```
   pip install pygame
   ```

## Usage

Run the simulation:
```
python game.py
```

The simulation will open a window showing sand particles falling and settling. Currently, it starts with a 10x10 block of sand that demonstrates the physics.

## Code Structure

- `sand` class: Handles individual particle physics and movement
- `empty` class: Represents empty space in the grid
- `water` class: Basic water implementation (currently unused in main simulation)
- Grid-based physics system with collision detection
- Pygame rendering loop for real-time visualization

## Customization

You can modify the simulation by:
- Changing grid size: Adjust `width` and `height` variables
- Modifying initial sand placement: Edit the nested loops that create sand particles
- Adjusting visual appearance: Modify `cell_size` for particle size
- Changing physics speed: Adjust the delay in `pygame.time.delay(50)`

## Future Enhancements

This is a foundation that could be expanded with:
- Interactive sand placement with mouse
- Multiple particle types (water, stone, etc.)
- Different physics behaviors
- Larger simulation grids
- Performance optimizations

## License
If you're wondering the following: "Why is this README so detailed for a powder sim that only has sand?"
Well, I'm lazy with the README's, and Claude Sonnet 4 via CoPilot clearly didn't understand "simple and not very detailed"
This project is open source and available for educational and personal use.
