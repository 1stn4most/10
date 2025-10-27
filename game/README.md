# 🎮 Time Warp Galaga - A Space Shooter Game

A classic Galaga-style space shooter with a unique **Time Warp** mechanic that lets you slow down time!

## 🌟 Unique Feature: Time Warp

Unlike traditional Galaga, this game features a **Time Warp** ability that allows you to:
- Slow down enemy movement and bullets to 30% speed
- Maintain your normal movement and shooting speed
- Create strategic advantages during intense moments
- Manage your Time Warp energy meter (auto-recharges)

## 🎯 Game Features

- **Progressive Difficulty**: Each level adds more enemies and increases their speed
- **Multiple Enemy Types**: Three different enemy types with varying point values
- **Particle Effects**: Explosive visual feedback for destroyed enemies
- **Wave Patterns**: Enemies move in sinusoidal patterns like classic Galaga
- **Enemy Fire**: Enemies shoot back at you!
- **Lives System**: Start with 3 lives, lose one when hit or when enemies reach the bottom
- **Score Tracking**: Compete for high scores across levels

## 🎮 Controls

| Key | Action |
|-----|--------|
| **Arrow Keys** or **A/D** | Move left and right |
| **SPACE** | Shoot |
| **SHIFT** | Activate Time Warp (slow motion) |

## 📁 File Structure

```
game/
├── index.html    # Main HTML file with game structure
├── style.css     # All styling and visual effects
├── game.js       # Complete game logic and mechanics
└── README.md     # This file
```

## 🚀 How to Run in VS Code

### Method 1: Live Server Extension (Recommended)

1. **Install Live Server Extension**:
   - Open VS Code
   - Go to Extensions (Ctrl+Shift+X or Cmd+Shift+X on Mac)
   - Search for "Live Server" by Ritwick Dey
   - Click "Install"

2. **Launch the Game**:
   - Open the `game` folder in VS Code
   - Right-click on `index.html`
   - Select "Open with Live Server"
   - The game will open in your default browser at `http://127.0.0.1:5500/game/index.html`

### Method 2: Direct Browser Opening

1. **Navigate to the game folder**:
   ```
   /home/runner/work/10/10/game/
   ```

2. **Double-click** `index.html` or drag it to your browser

3. The game should load and be ready to play!

### Method 3: Python HTTP Server

1. Open terminal in VS Code (Ctrl+` or Cmd+`)
2. Navigate to the game directory:
   ```bash
   cd game
   ```
3. Run Python's built-in server:
   ```bash
   # Python 3
   python3 -m http.server 8000
   
   # Python 2
   python -m SimpleHTTPServer 8000
   ```
4. Open browser and go to: `http://localhost:8000`

## 📝 Code Description

### index.html
The main HTML structure containing:
- Game canvas element for rendering
- Start screen with instructions
- Game over screen
- Level complete screen
- Score, lives, level, and Time Warp meter displays

### style.css
Visual styling including:
- Cyberpunk-inspired color scheme (cyan and magenta)
- Glowing text effects and animations
- Responsive design for different screen sizes
- Overlay screens for game states
- Time Warp energy bar styling

### game.js
Complete game logic featuring:

**Core Classes**:
- `Player`: Handles player movement, shooting, and Time Warp activation
- `Enemy`: Manages enemy behavior, movement patterns, and AI shooting
- `Bullet`: Handles projectile physics and collision
- `Particle`: Creates explosion effects

**Game Systems**:
- Time Warp mechanic (slows enemies to 30% speed while player stays normal)
- Collision detection between all game objects
- Progressive difficulty scaling with levels
- Enemy wave spawning system
- Score and lives management
- Particle system for visual effects

**Key Functions**:
- `gameLoop()`: Main game loop using requestAnimationFrame
- `createEnemies()`: Spawns enemy waves with increasing difficulty
- `checkCollision()`: Detects intersections between game objects
- `createExplosion()`: Generates particle effects

## 🎨 Customization

You can easily customize the game by modifying these values in `game.js`:

```javascript
// Player speed
player.speed = 5;

// Time Warp drain rate
timeWarpDrainRate: 0.8

// Time Warp recharge rate
timeWarpRechargeRate: 0.2

// Enemy colors
this.colors = ['#ff0000', '#ff00ff', '#ffff00'];

// Points per enemy type
this.points = (type + 1) * 100;
```

## 🐛 Troubleshooting

**Game doesn't load?**
- Make sure all three files (index.html, style.css, game.js) are in the same folder
- Check browser console for errors (F12)
- Ensure JavaScript is enabled in your browser

**Controls not working?**
- Click on the game canvas to give it focus
- Try refreshing the page

**Performance issues?**
- Close other browser tabs
- Try a different browser (Chrome/Firefox recommended)
- Reduce browser zoom level to 100%

## 🎓 Learning Points

This game demonstrates:
- HTML5 Canvas API for rendering
- JavaScript game loop architecture
- Object-oriented programming with ES6 classes
- Collision detection algorithms
- Particle systems
- Event handling and input management
- Game state management
- CSS animations and effects

## 📜 License

This game is provided as-is for educational and entertainment purposes.

## 🎉 Enjoy!

Have fun playing Time Warp Galaga! See how many levels you can complete and what high score you can achieve! 🚀✨
