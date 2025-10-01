// Game Constants
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// Set canvas size
canvas.width = 800;
canvas.height = 600;

// Game State
let gameState = {
    score: 0,
    lives: 3,
    level: 1,
    isPlaying: false,
    isPaused: false,
    timeWarpEnergy: 100,
    timeWarpActive: false,
    timeWarpRechargeRate: 0.2,
    timeWarpDrainRate: 0.8
};

// Arrays for game objects
let bullets = [];
let enemies = [];
let enemyBullets = [];
let particles = [];
let player;

// Input handling
const keys = {};

document.addEventListener('keydown', (e) => {
    keys[e.key] = true;
    keys[e.code] = true;
});

document.addEventListener('keyup', (e) => {
    keys[e.key] = false;
    keys[e.code] = false;
});

// Button handlers
document.getElementById('startButton').addEventListener('click', startGame);
document.getElementById('restartButton').addEventListener('click', restartGame);
document.getElementById('nextLevelButton').addEventListener('click', nextLevel);

// Player class
class Player {
    constructor() {
        this.reset();
    }

    reset() {
        this.x = canvas.width / 2;
        this.y = canvas.height - 80;
        this.width = 40;
        this.height = 40;
        this.speed = 5;
    }

    draw() {
        // Draw spaceship
        ctx.fillStyle = '#00ffff';
        ctx.shadowBlur = 15;
        ctx.shadowColor = '#00ffff';
        
        // Ship body
        ctx.beginPath();
        ctx.moveTo(this.x, this.y - this.height / 2);
        ctx.lineTo(this.x - this.width / 2, this.y + this.height / 2);
        ctx.lineTo(this.x, this.y + this.height / 4);
        ctx.lineTo(this.x + this.width / 2, this.y + this.height / 2);
        ctx.closePath();
        ctx.fill();
        
        // Cockpit
        ctx.fillStyle = '#ff00ff';
        ctx.beginPath();
        ctx.arc(this.x, this.y, 8, 0, Math.PI * 2);
        ctx.fill();
        
        ctx.shadowBlur = 0;
    }

    update() {
        // Movement
        if ((keys['ArrowLeft'] || keys['a'] || keys['A']) && this.x > this.width / 2) {
            this.x -= this.speed;
        }
        if ((keys['ArrowRight'] || keys['d'] || keys['D']) && this.x < canvas.width - this.width / 2) {
            this.x += this.speed;
        }

        // Shooting
        if (keys[' '] || keys['Space']) {
            this.shoot();
        }

        // Time Warp
        if ((keys['Shift'] || keys['ShiftLeft'] || keys['ShiftRight']) && gameState.timeWarpEnergy > 0) {
            gameState.timeWarpActive = true;
            gameState.timeWarpEnergy = Math.max(0, gameState.timeWarpEnergy - gameState.timeWarpDrainRate);
        } else {
            gameState.timeWarpActive = false;
            gameState.timeWarpEnergy = Math.min(100, gameState.timeWarpEnergy + gameState.timeWarpRechargeRate);
        }

        updateTimeWarpBar();
    }

    shoot() {
        const now = Date.now();
        if (!this.lastShot || now - this.lastShot > 250) {
            bullets.push(new Bullet(this.x, this.y - this.height / 2, -8, '#00ffff'));
            this.lastShot = now;
        }
    }
}

// Bullet class
class Bullet {
    constructor(x, y, speed, color) {
        this.x = x;
        this.y = y;
        this.speed = speed;
        this.color = color;
        this.width = 4;
        this.height = 15;
    }

    draw() {
        ctx.fillStyle = this.color;
        ctx.shadowBlur = 10;
        ctx.shadowColor = this.color;
        ctx.fillRect(this.x - this.width / 2, this.y - this.height / 2, this.width, this.height);
        ctx.shadowBlur = 0;
    }

    update() {
        const speedMultiplier = gameState.timeWarpActive && this.speed > 0 ? 0.3 : 1;
        this.y += this.speed * speedMultiplier;
    }

    isOffScreen() {
        return this.y < -20 || this.y > canvas.height + 20;
    }
}

// Enemy class
class Enemy {
    constructor(x, y, type) {
        this.x = x;
        this.y = y;
        this.width = 35;
        this.height = 35;
        this.type = type;
        this.speed = 0.5 + gameState.level * 0.1;
        this.amplitude = 30;
        this.frequency = 0.02;
        this.originalX = x;
        this.time = Math.random() * 100;
        this.shootCooldown = 0;
        
        // Different enemy types
        this.colors = ['#ff0000', '#ff00ff', '#ffff00'];
        this.color = this.colors[type % this.colors.length];
        this.points = (type + 1) * 100;
    }

    draw() {
        ctx.fillStyle = this.color;
        ctx.shadowBlur = 10;
        ctx.shadowColor = this.color;
        
        // Enemy body (alien-like)
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.width / 2, 0, Math.PI * 2);
        ctx.fill();
        
        // Eyes
        ctx.fillStyle = '#000';
        ctx.beginPath();
        ctx.arc(this.x - 8, this.y - 3, 4, 0, Math.PI * 2);
        ctx.arc(this.x + 8, this.y - 3, 4, 0, Math.PI * 2);
        ctx.fill();
        
        ctx.shadowBlur = 0;
    }

    update() {
        const speedMultiplier = gameState.timeWarpActive ? 0.3 : 1;
        
        // Move in a wave pattern
        this.time += this.frequency * speedMultiplier;
        this.x = this.originalX + Math.sin(this.time) * this.amplitude;
        this.y += this.speed * speedMultiplier;

        // Shooting
        this.shootCooldown -= speedMultiplier;
        if (this.shootCooldown <= 0 && Math.random() < 0.002 * (1 / speedMultiplier)) {
            this.shoot();
            this.shootCooldown = 60;
        }
    }

    shoot() {
        enemyBullets.push(new Bullet(this.x, this.y + this.height / 2, 4, '#ff0000'));
    }
}

// Particle class for explosions
class Particle {
    constructor(x, y, color) {
        this.x = x;
        this.y = y;
        this.vx = (Math.random() - 0.5) * 5;
        this.vy = (Math.random() - 0.5) * 5;
        this.color = color;
        this.life = 100;
        this.size = Math.random() * 4 + 2;
    }

    draw() {
        ctx.fillStyle = this.color;
        ctx.globalAlpha = this.life / 100;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fill();
        ctx.globalAlpha = 1;
    }

    update() {
        this.x += this.vx;
        this.y += this.vy;
        this.life -= 2;
    }
}

// Create explosion effect
function createExplosion(x, y, color) {
    for (let i = 0; i < 15; i++) {
        particles.push(new Particle(x, y, color));
    }
}

// Initialize game
function initGame() {
    gameState.isPlaying = false;
    gameState.score = 0;
    gameState.lives = 3;
    gameState.level = 1;
    gameState.timeWarpEnergy = 100;
    
    player = new Player();
    bullets = [];
    enemies = [];
    enemyBullets = [];
    particles = [];
    
    updateUI();
}

// Start game
function startGame() {
    initGame();
    createEnemies();
    gameState.isPlaying = true;
    hideScreen('startScreen');
    gameLoop();
}

// Restart game
function restartGame() {
    hideScreen('gameOverScreen');
    startGame();
}

// Next level
function nextLevel() {
    gameState.level++;
    createEnemies();
    bullets = [];
    enemyBullets = [];
    hideScreen('levelCompleteScreen');
    gameLoop();
}

// Create enemies
function createEnemies() {
    enemies = [];
    const rows = 3 + Math.floor(gameState.level / 2);
    const cols = 8;
    const spacing = 70;
    const offsetX = (canvas.width - (cols - 1) * spacing) / 2;
    const offsetY = 80;

    for (let row = 0; row < rows; row++) {
        for (let col = 0; col < cols; col++) {
            const x = offsetX + col * spacing;
            const y = offsetY + row * 50;
            enemies.push(new Enemy(x, y, row % 3));
        }
    }
}

// Collision detection
function checkCollision(rect1, rect2) {
    return rect1.x < rect2.x + rect2.width &&
           rect1.x + rect1.width > rect2.x &&
           rect1.y < rect2.y + rect2.height &&
           rect1.y + rect1.height > rect2.y;
}

// Update UI
function updateUI() {
    document.getElementById('score').textContent = gameState.score;
    document.getElementById('lives').textContent = gameState.lives;
    document.getElementById('level').textContent = gameState.level;
}

// Update time warp bar
function updateTimeWarpBar() {
    const bar = document.getElementById('timeWarpBar');
    bar.style.width = gameState.timeWarpEnergy + '%';
}

// Show/Hide screens
function showScreen(id) {
    document.getElementById(id).classList.remove('hidden');
}

function hideScreen(id) {
    document.getElementById(id).classList.add('hidden');
}

// Game Over
function gameOver() {
    gameState.isPlaying = false;
    document.getElementById('finalScore').textContent = gameState.score;
    document.getElementById('finalLevel').textContent = gameState.level;
    showScreen('gameOverScreen');
}

// Level Complete
function levelComplete() {
    gameState.isPlaying = false;
    showScreen('levelCompleteScreen');
}

// Main game loop
function gameLoop() {
    if (!gameState.isPlaying) return;

    // Clear canvas
    ctx.fillStyle = '#000';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Draw time warp effect
    if (gameState.timeWarpActive) {
        ctx.fillStyle = 'rgba(255, 0, 255, 0.1)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
    }

    // Update and draw player
    player.update();
    player.draw();

    // Update and draw bullets
    bullets = bullets.filter(bullet => {
        bullet.update();
        bullet.draw();
        return !bullet.isOffScreen();
    });

    // Update and draw enemy bullets
    enemyBullets = enemyBullets.filter(bullet => {
        bullet.update();
        bullet.draw();
        
        // Check collision with player
        if (checkCollision(
            { x: bullet.x - bullet.width / 2, y: bullet.y - bullet.height / 2, width: bullet.width, height: bullet.height },
            { x: player.x - player.width / 2, y: player.y - player.height / 2, width: player.width, height: player.height }
        )) {
            createExplosion(player.x, player.y, '#00ffff');
            gameState.lives--;
            updateUI();
            
            if (gameState.lives <= 0) {
                gameOver();
                return false;
            }
            
            player = new Player();
            return false;
        }
        
        return !bullet.isOffScreen();
    });

    // Update and draw enemies
    enemies = enemies.filter(enemy => {
        enemy.update();
        enemy.draw();

        // Check collision with bullets
        for (let i = bullets.length - 1; i >= 0; i--) {
            if (checkCollision(
                { x: bullets[i].x - bullets[i].width / 2, y: bullets[i].y - bullets[i].height / 2, width: bullets[i].width, height: bullets[i].height },
                { x: enemy.x - enemy.width / 2, y: enemy.y - enemy.height / 2, width: enemy.width, height: enemy.height }
            )) {
                createExplosion(enemy.x, enemy.y, enemy.color);
                gameState.score += enemy.points;
                updateUI();
                bullets.splice(i, 1);
                return false;
            }
        }

        // Check if enemy reached bottom
        if (enemy.y > canvas.height) {
            gameState.lives--;
            updateUI();
            
            if (gameState.lives <= 0) {
                gameOver();
            }
            return false;
        }

        return true;
    });

    // Update and draw particles
    particles = particles.filter(particle => {
        particle.update();
        particle.draw();
        return particle.life > 0;
    });

    // Check level complete
    if (enemies.length === 0 && gameState.isPlaying) {
        levelComplete();
        return;
    }

    // Continue loop
    requestAnimationFrame(gameLoop);
}

// Initialize on load
window.addEventListener('load', () => {
    initGame();
});
