# 🚀 Quick Setup Guide for VS Code

## Copy-Paste Instructions

### Step 1: Create the Game Folder
Open VS Code terminal (Ctrl+` or Cmd+`) and run:
```bash
mkdir -p game
cd game
```

### Step 2: Create index.html
Create a new file `game/index.html` and paste this content:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Time Warp Galaga - A Space Shooter Game</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="game-container">
        <div class="header">
            <h1>⏰ TIME WARP GALAGA ⏰</h1>
            <div class="info-panel">
                <div class="stat">
                    <span class="label">Score:</span>
                    <span id="score">0</span>
                </div>
                <div class="stat">
                    <span class="label">Lives:</span>
                    <span id="lives">3</span>
                </div>
                <div class="stat">
                    <span class="label">Level:</span>
                    <span id="level">1</span>
                </div>
                <div class="stat time-warp-meter">
                    <span class="label">Time Warp:</span>
                    <div class="meter">
                        <div id="timeWarpBar" class="meter-fill"></div>
                    </div>
                </div>
            </div>
        </div>
        
        <canvas id="gameCanvas"></canvas>
        
        <div id="startScreen" class="screen">
            <h2>TIME WARP GALAGA</h2>
            <p class="tagline">A classic space shooter with a time-bending twist!</p>
            <div class="instructions">
                <h3>🎮 Controls</h3>
                <p><strong>Arrow Keys / A & D:</strong> Move left and right</p>
                <p><strong>SPACE:</strong> Shoot</p>
                <p><strong>SHIFT:</strong> Activate Time Warp (slow down time!)</p>
                <h3>✨ Special Feature</h3>
                <p>Use <strong>Time Warp</strong> to slow down enemy movements and bullets while maintaining your normal speed! The meter recharges automatically.</p>
                <h3>🎯 Objective</h3>
                <p>Destroy all enemies to advance to the next level. Don't let them reach the bottom or hit you with their bullets!</p>
            </div>
            <button id="startButton" class="game-button">START GAME</button>
        </div>
        
        <div id="gameOverScreen" class="screen hidden">
            <h2>GAME OVER</h2>
            <p class="final-score">Final Score: <span id="finalScore">0</span></p>
            <p class="final-level">Level Reached: <span id="finalLevel">1</span></p>
            <button id="restartButton" class="game-button">PLAY AGAIN</button>
        </div>
        
        <div id="levelCompleteScreen" class="screen hidden">
            <h2>LEVEL COMPLETE!</h2>
            <p class="level-message">Preparing next wave...</p>
            <button id="nextLevelButton" class="game-button">CONTINUE</button>
        </div>
    </div>
    
    <script src="game.js"></script>
</body>
</html>
```

### Step 3: Create style.css
Create a new file `game/style.css` and paste this content:

```css
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Courier New', monospace;
    background: linear-gradient(135deg, #0a0a1a 0%, #1a0a2e 50%, #0a0a1a 100%);
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    color: #fff;
    overflow: hidden;
}

.game-container {
    background: rgba(0, 0, 0, 0.8);
    border: 3px solid #00ffff;
    border-radius: 10px;
    padding: 20px;
    box-shadow: 0 0 30px rgba(0, 255, 255, 0.5);
    max-width: 900px;
    width: 100%;
}

.header {
    text-align: center;
    margin-bottom: 20px;
}

.header h1 {
    color: #00ffff;
    text-shadow: 0 0 10px #00ffff, 0 0 20px #00ffff;
    font-size: 2em;
    margin-bottom: 15px;
    animation: glow 2s ease-in-out infinite alternate;
}

@keyframes glow {
    from {
        text-shadow: 0 0 10px #00ffff, 0 0 20px #00ffff;
    }
    to {
        text-shadow: 0 0 20px #00ffff, 0 0 30px #00ffff, 0 0 40px #00ffff;
    }
}

.info-panel {
    display: flex;
    justify-content: space-around;
    flex-wrap: wrap;
    gap: 20px;
    padding: 15px;
    background: rgba(0, 255, 255, 0.1);
    border-radius: 8px;
    border: 1px solid rgba(0, 255, 255, 0.3);
}

.stat {
    display: flex;
    align-items: center;
    gap: 10px;
}

.label {
    color: #00ffff;
    font-weight: bold;
    font-size: 1.1em;
}

.stat span:last-child {
    color: #fff;
    font-size: 1.2em;
    font-weight: bold;
}

.time-warp-meter {
    flex-direction: column;
    align-items: flex-start;
}

.meter {
    width: 150px;
    height: 20px;
    background: rgba(0, 0, 0, 0.5);
    border: 2px solid #00ffff;
    border-radius: 10px;
    overflow: hidden;
}

.meter-fill {
    height: 100%;
    background: linear-gradient(90deg, #ff00ff 0%, #00ffff 100%);
    transition: width 0.3s ease;
    box-shadow: 0 0 10px #ff00ff;
}

#gameCanvas {
    display: block;
    width: 100%;
    background: #000;
    border: 2px solid #00ffff;
    border-radius: 5px;
    cursor: none;
}

.screen {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: rgba(0, 0, 0, 0.95);
    border: 3px solid #00ffff;
    border-radius: 15px;
    padding: 40px;
    text-align: center;
    box-shadow: 0 0 50px rgba(0, 255, 255, 0.7);
    max-width: 600px;
    z-index: 10;
}

.screen h2 {
    color: #00ffff;
    font-size: 3em;
    margin-bottom: 20px;
    text-shadow: 0 0 20px #00ffff;
}

.tagline {
    color: #ff00ff;
    font-size: 1.2em;
    margin-bottom: 30px;
    font-style: italic;
}

.instructions {
    text-align: left;
    margin: 30px 0;
    padding: 20px;
    background: rgba(0, 255, 255, 0.1);
    border-radius: 10px;
    border: 1px solid rgba(0, 255, 255, 0.3);
}

.instructions h3 {
    color: #ff00ff;
    margin-bottom: 15px;
    font-size: 1.3em;
}

.instructions p {
    margin: 10px 0;
    line-height: 1.6;
    color: #fff;
}

.instructions strong {
    color: #00ffff;
}

.game-button {
    background: linear-gradient(135deg, #ff00ff 0%, #00ffff 100%);
    border: none;
    color: #fff;
    padding: 15px 40px;
    font-size: 1.5em;
    font-weight: bold;
    font-family: 'Courier New', monospace;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 0 20px rgba(255, 0, 255, 0.5);
}

.game-button:hover {
    transform: scale(1.1);
    box-shadow: 0 0 30px rgba(255, 0, 255, 0.8);
}

.game-button:active {
    transform: scale(0.95);
}

.hidden {
    display: none !important;
}

.final-score, .final-level {
    font-size: 1.5em;
    margin: 20px 0;
    color: #fff;
}

.final-score span, .final-level span {
    color: #00ffff;
    font-weight: bold;
}

.level-message {
    font-size: 1.3em;
    color: #ff00ff;
    margin: 20px 0;
}

@media (max-width: 768px) {
    .game-container {
        padding: 10px;
    }
    
    .header h1 {
        font-size: 1.5em;
    }
    
    .info-panel {
        gap: 10px;
    }
    
    .screen {
        padding: 20px;
        max-width: 90%;
    }
    
    .screen h2 {
        font-size: 2em;
    }
}
```

### Step 4: Create game.js
Create a new file `game/game.js` and paste the JavaScript code from the repository file.

*Note: The game.js file is quite large (400+ lines). You can find it in this repository at `game/game.js`*

### Step 5: Launch the Game

**Option A: Using Live Server (Recommended)**
1. Install "Live Server" extension in VS Code
2. Right-click on `index.html`
3. Select "Open with Live Server"

**Option B: Using Python**
```bash
cd game
python3 -m http.server 8000
```
Then open: http://localhost:8000

**Option C: Direct Browser**
Simply double-click `index.html` or drag it to your browser

## 🎮 Controls

| Key | Action |
|-----|--------|
| **Arrow Keys** or **A/D** | Move left and right |
| **SPACE** | Shoot |
| **SHIFT** | Activate Time Warp |

## 🌟 What Makes This Game Special?

### Time Warp Mechanic
Unlike traditional Galaga, this game features a **Time Warp** ability:
- Slows enemies and their bullets to 30% speed
- YOU maintain normal speed for movement and shooting
- Creates strategic opportunities during intense moments
- Auto-recharges when not in use

### Other Features
- Progressive difficulty (more enemies and faster speed each level)
- Three enemy types with different point values
- Particle explosion effects
- Wave movement patterns
- Enemy AI that shoots back
- Lives system
- Score tracking

## 📁 File Descriptions

### index.html (Main Structure)
- Game canvas for rendering
- Start screen with instructions
- Game over screen
- Level complete screen
- HUD showing score, lives, level, and Time Warp meter

### style.css (Visual Design)
- Cyberpunk-inspired color scheme (cyan & magenta)
- Glowing text effects and animations
- Responsive layout
- Time Warp energy bar with gradient
- Modal overlays for game states

### game.js (Game Logic)
**Classes:**
- `Player`: Movement, shooting, Time Warp control
- `Enemy`: AI behavior, wave patterns, shooting
- `Bullet`: Projectile physics affected by Time Warp
- `Particle`: Explosion visual effects

**Systems:**
- Time Warp mechanic (game state management)
- Collision detection (player, enemies, bullets)
- Progressive difficulty scaling
- Enemy spawning system
- Score and lives tracking
- Particle effects system

**Key Functions:**
- `gameLoop()`: Main game loop (requestAnimationFrame)
- `createEnemies()`: Spawns enemy waves
- `checkCollision()`: Box collision detection
- `createExplosion()`: Particle generation

## 🎨 Customization

Easily modify these values in `game.js`:

```javascript
// Player speed (line ~58)
this.speed = 5;

// Time Warp rates (lines ~15-16)
timeWarpRechargeRate: 0.2,  // How fast it recharges
timeWarpDrainRate: 0.8,     // How fast it drains

// Time Warp slowdown effect (lines ~149, ~159)
const speedMultiplier = gameState.timeWarpActive ? 0.3 : 1;

// Enemy colors (line ~175)
this.colors = ['#ff0000', '#ff00ff', '#ffff00'];

// Points per enemy (line ~177)
this.points = (type + 1) * 100;  // 100, 200, or 300 points

// Initial lives (line ~264)
gameState.lives = 3;

// Enemies per row (line ~292)
const cols = 8;
```

## 🐛 Troubleshooting

**Game doesn't appear?**
- Ensure all 3 files are in the same `game` folder
- Check browser console (F12) for errors
- Try a different browser (Chrome/Firefox recommended)

**Controls not responding?**
- Click on the game canvas to give it focus
- Refresh the page (F5)
- Make sure JavaScript is enabled

**Performance issues?**
- Close other browser tabs
- Reduce browser zoom to 100%
- Try incognito/private mode

## 🎓 What You'll Learn

This game demonstrates:
- HTML5 Canvas API for 2D rendering
- JavaScript game loop architecture
- Object-oriented programming with ES6 classes
- Collision detection algorithms
- Particle systems and visual effects
- Event handling and input management
- Game state management
- CSS animations and effects
- Responsive web design

Enjoy playing Time Warp Galaga! 🚀✨
