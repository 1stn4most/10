# 📋 Copy & Paste Instructions for VS Code

## 🎯 Complete Step-by-Step Guide

Follow these exact steps to get the game running in VS Code:

---

## Step 1: Open VS Code and Create Project Folder

1. Open **VS Code**
2. Go to **File → Open Folder**
3. Create a new folder called `time-warp-galaga` and open it
4. Open the integrated terminal: **Terminal → New Terminal** (or press `Ctrl+``)

---

## Step 2: Create the File Structure

In the terminal, type:
```bash
mkdir game
cd game
```

---

## Step 3: Create the HTML File

1. In VS Code, click **File → New File**
2. Save it as `index.html` inside the `game` folder
3. **Copy and paste** the entire code below:

<details>
<summary>📄 Click to expand index.html code (58 lines)</summary>

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

</details>

4. **Save the file** (`Ctrl+S` or `Cmd+S`)

---

## Step 4: Create the CSS File

1. In VS Code, click **File → New File**
2. Save it as `style.css` inside the `game` folder
3. **Copy and paste** the entire code below:

<details>
<summary>📄 Click to expand style.css code (210 lines)</summary>

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

</details>

4. **Save the file** (`Ctrl+S` or `Cmd+S`)

---

## Step 5: Create the JavaScript File

1. In VS Code, click **File → New File**
2. Save it as `game.js` inside the `game` folder
3. Go to the repository and **copy the entire content** of `game/game.js`
4. **Paste it** into your new `game.js` file

**Or download it directly from:**
`https://github.com/1stn4most/10/raw/main/game/game.js`

4. **Save the file** (`Ctrl+S` or `Cmd+S`)

---

## Step 6: Launch the Game

### Method A: Live Server Extension (Recommended) ⭐

1. **Install Live Server Extension:**
   - Click the Extensions icon in VS Code (or press `Ctrl+Shift+X`)
   - Search for "**Live Server**" by Ritwick Dey
   - Click **Install**

2. **Launch the Game:**
   - Right-click on `index.html` in the file explorer
   - Select "**Open with Live Server**"
   - Your browser will open automatically with the game!

### Method B: Python HTTP Server

1. In the VS Code terminal, make sure you're in the `game` folder:
```bash
cd game
```

2. Run the server:
```bash
python3 -m http.server 8000
```

3. Open your browser and go to: `http://localhost:8000`

### Method C: Direct File Open

1. In VS Code Explorer, right-click `index.html`
2. Select "**Reveal in File Explorer**" (Windows) or "**Reveal in Finder**" (Mac)
3. Double-click the file to open it in your default browser

---

## 🎮 How to Play

### Controls
- **Arrow Keys** or **A/D** → Move left/right
- **SPACE** → Shoot
- **SHIFT** → Activate Time Warp (slow down time!)

### Objective
- Destroy all enemies to advance levels
- Don't let enemies reach the bottom
- Avoid enemy bullets
- Use Time Warp strategically!

### Special Feature: Time Warp ⏰
- Hold **SHIFT** to slow down enemies and bullets to 30% speed
- YOU maintain normal speed!
- Watch the purple/cyan energy meter - it recharges automatically
- Use it strategically during intense moments

---

## 📁 Final Folder Structure

Your project should look like this:
```
time-warp-galaga/
└── game/
    ├── index.html    (Game structure)
    ├── style.css     (Visual styling)
    └── game.js       (Game logic)
```

---

## ✨ What Each File Does

### index.html
- Creates the game canvas
- Provides start screen with instructions
- Shows game over and level complete screens
- Displays HUD (score, lives, level, Time Warp meter)

### style.css
- Cyberpunk color scheme (cyan & magenta)
- Glowing text effects
- Responsive design
- Button hover effects
- Time Warp energy bar styling

### game.js
- **Player Class**: Movement, shooting, Time Warp activation
- **Enemy Class**: AI behavior, wave patterns, shooting
- **Bullet Class**: Projectile physics
- **Particle Class**: Explosion effects
- **Game Loop**: Main update/render cycle
- **Collision Detection**: Checks hits between objects
- **Time Warp System**: Slows enemy movement/bullets

---

## 🎨 Customization Tips

Want to modify the game? Here are some easy tweaks in `game.js`:

**Make the player faster:**
```javascript
// Line ~58
this.speed = 7;  // Default is 5
```

**Change Time Warp recharge speed:**
```javascript
// Line ~15
timeWarpRechargeRate: 0.5,  // Default is 0.2 (faster recharge)
```

**Adjust Time Warp slowdown:**
```javascript
// Lines ~149, ~159
const speedMultiplier = gameState.timeWarpActive ? 0.2 : 1;  // Default is 0.3 (slower)
```

**More starting lives:**
```javascript
// Line ~264
gameState.lives = 5;  // Default is 3
```

**Change enemy colors:**
```javascript
// Line ~175
this.colors = ['#ff0000', '#00ff00', '#0000ff'];  // Red, Green, Blue
```

---

## 🐛 Troubleshooting

**Game doesn't load?**
- ✅ Check that all 3 files are in the `game` folder
- ✅ Open browser console (press F12) to see errors
- ✅ Try a different browser (Chrome or Firefox)

**Controls not working?**
- ✅ Click on the game canvas to give it focus
- ✅ Refresh the page (F5)

**Can't see the player ship?**
- ✅ The ship appears at the bottom center when you start
- ✅ It's a cyan triangle with a magenta cockpit
- ✅ Try moving left/right to see it

**Performance issues?**
- ✅ Close other browser tabs
- ✅ Set browser zoom to 100%
- ✅ Try incognito/private browsing mode

---

## 🎉 You're Done!

Enjoy playing **Time Warp Galaga**! 🚀

Try to beat your high score and see how many levels you can complete!

Don't forget to use the **Time Warp** ability (SHIFT key) when things get intense! ⏰✨
