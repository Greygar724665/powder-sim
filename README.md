# Powder Simulation

A powder physics simulation made with Python and Pygame.  It's basically a falling sand game where you can watch different materials interact with gravity, temperature, and each other.

## What it does

This is a grid-based physics engine where particles behave like their real-world counterparts.  Sand falls and slides around obstacles, water flows and can freeze or evaporate, lava melts things, and there's even acid that dissolves stuff.  Each particle type has its own physics behavior and temperature properties.

## Features

- **Multiple particle types**: Sand, dirt, stone, water, lava, acid, ice, steam, fire, and more
- **Temperature system**: Particles heat up and cool down, affecting state changes (water freezes into ice, evaporates into steam, etc.)
- **Realistic physics**: Different movement patterns for granular materials (sand, dirt), liquids (water, lava), and gases (steam, fire)
- **Interactive placement**: Draw particles with your mouse (left click to place, right click to erase)
- **Visual variety**: Each particle has subtle color variations so they look more natural
- **State changes**: Watch water boil into steam, lava cool into basalt, and ice melt back into water

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

The window opens with an empty grid. Click and drag to place the currently selected particle type. Right-click to erase. Watch as particles fall, flow, heat up, cool down, and interact with each other. 

## Particle Types

**Granular (falls and slides):**
- Sand - classic falling sand behavior
- Dirt - similar to sand but slightly different properties

**Liquids (flows horizontally):**
- Water - flows freely, freezes at 0°C, evaporates at 100°C
- Lava - flows slowly, extremely hot, solidifies into basalt when it cools
- Acid - corrosive liquid that dissolves other particles

**Straight Falling:**
- Stone - falls straight down without sliding
- Mud - dense falling material

**Gases (rises):**
- Steam - rises up, created when water evaporates
- Fire - burns upward, has a limited lifetime
- Cold Fire - blue fire that's actually cold (because why not)

**Static:**
- Ice - frozen water, melts back when warmed
- Basalt - cooled lava, can melt again at high temperatures
- Tungsten - high melting point material

## Customization

You can tweak the simulation by modifying variables in `game.py`:
- Grid size:  Change `width` and `height`
- Cell size: Adjust `cell_size` for larger/smaller particles  
- Ambient temperature: Modify `ambient_temperature` to change the default environment
- Particle properties: Each particle class has properties like conductivity, color, and temperature thresholds

## How it works

The simulation uses a class hierarchy where all particles inherit from a base `Particle` class. There are several behavior categories (Granular, Liquid, Gas, Static) that define how particles move.  The temperature system allows heat to transfer between neighboring particles, causing phase changes when thresholds are reached.

## License

If you're wondering why this README was so over-the-top detailed before - I asked Claude to keep it simple and it apparently didn't understand "not very detailed." This version is actually written by a human (mostly).

This project is open source and available for educational and personal use.
