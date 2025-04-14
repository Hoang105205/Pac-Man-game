# 👾 Pac-Man AI Project 🎮  

## 📌 Overview  
This project is an AI-driven Pac-Man game where multiple ghosts use different pathfinding algorithms to chase Pac-Man. The implemented algorithms include:  

-  **BFS (Breadth-First Search)**  
-  **DFS (Depth-First Search)**  
-  **UCS (Uniform Cost Search)**  
-  **A\* (A-Star Search)**  

Each ghost follows a unique algorithm to navigate the maze and attempt to catch Pac-Man.  

## ✨ Features  
✅ Pac-Man controlled by the player 🎮  
✅ Four ghosts using different search algorithms 👻👻👻👻  
✅ Collision avoidance between ghosts 🚫👾  
✅ A simple grid-based game environment 🟦  

## ⚙️ Installation  
### 📋 Requirements  
Ensure you have Python installed along with the required dependencies. Install dependencies using:  

```sh
pip install -r requirements.txt
```

### ▶️ Running the Game
-   **Terminal**
```sh
python main.py
```
-   **.exe**
```
Click file Pacman game.exe
```

## 📂 File Structure
```
23127047_23127462_23127463/  
├── Source/    
    ├── main.py          # Entry point of the game  
    ├── Assets/          # Store game textures
    ├── Object/          # Directory for game objects (ghost, pacman, etc.)  
    ├── constants.py     # Define game constants  
    ├── Pacman game.exe  # Game application
├── requirements.txt # Dependencies  
├── README.md        # Project documentation 

```

## 🎮 Controls
**For PacMan**
- ⬆️ **Up Arrow**: Move up  
- ⬇️ **Down Arrow**: Move down  
- ⬅️ **Left Arrow**: Move left  
- ➡️ **Right Arrow**: Move right  


## 🧠 AI Behavior
Each ghost follows a different strategy:
- **BFS Ghost**: Finds the shortest path using breadth-first search
- **DFS Ghost**: Explores deeper paths before backtracking
- **UCS Ghost**: Uses uniform cost search with custom step costs based on terrain and distance.
- **A\* Ghost**: Uses A* search with a heuristic for optimal pathfinding

## 🚀 Future Improvements
- Implement smarter AI behavior
- Add power-ups and special abilities
- Improve collision handling between ghosts

