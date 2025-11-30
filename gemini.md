# NFL Sim Engine: The Digital Gridiron

**DOCUMENT ID:** NFL-SIM-001
**STATUS:** ARCHITECTURE_DEFINED
**AUTHOR:** Gemini
**DIRECTIVE:** Generate a comprehensive blueprint and task list for the NFL Sim Engine.

---

## 1.0 NARRATIVE ARC: THE PROBLEM EXPOSITION

Professional football is a game of immense complexity, with interacting systems of player skills, team strategy, financial management, and career progression. Most sports simulation games offer a surface-level experience. The goal of the **NFL Sim Engine** is to create a deeply immersive, highly detailed, and endlessly replayable simulation of managing a professional football franchise.

This system is built to model the granular details of the sport, from individual player attributes and physics-based game outcomes to complex AI-driven decision-making for coaches and general managers. It aims to be the "Dwarf Fortress" of football simulations—a true digital gridiron.

The guiding philosophy is **Emergent Narrative Generation**: the system will not tell stories, but create a world so detailed that compelling stories naturally emerge from the simulation.

## 2.0 SYSTEM ARCHITECTURE BLUEPRINT

The NFL Sim Engine is a full-stack application with a clear separation between the backend simulation engine and the frontend user interface.

```text
[ User Input (React UI) ] -> [ FastAPI Backend ]
                                |
                                +--> [ API Layer ] -> Exposes REST endpoints for all game data.
                                |
                                +--> [ Orchestrator ] -> Manages game state, calendar, and events (e.g., season, offseason, draft).
                                |
                                +--> [ RPG Engine ] -> Handles player progression, traits, and narrative events.
                                |
                                +--> [ Game Engine ] -> Simulates individual plays and games using physics and AI.
                                |
                                +--> [ Database (SQLAlchemy) ] -> Persists all game state via a detailed relational schema.
                                |
                                V
[ Simulated NFL World (Dynamic UI) ]
```

### **2.1 Input Layer: The Front Office**

A web-based interface for the user to act as the General Manager and Head Coach of their team.

- **UI:** A React/Vite application.
- **Function:** Allows the user to:
  - Manage the roster (sign, trade, draft players).
  - Set team strategy and depth charts.
  - Advance the game week by week.
  - View detailed stats, standings, and league news.
- **Output:** API calls to the backend to execute user actions and fetch updated game state.

### **2.2 Core Logic: The Simulation Engine (Python/FastAPI)**

The backend is a powerful Python application that runs the entire simulation.

- **API Layer:** Built with FastAPI, it provides endpoints for the frontend to interact with the game world. Uses Pydantic for data validation.
- **Orchestrator (`/orchestrator`):** The heart of the simulation's lifecycle. It manages the progression of time, from advancing weeks in the season to stepping through the complex phases of the offseason (free agency, draft, etc.).
- **RPG Engine (`/rpg`):** Manages the "human" elements of the simulation. This includes player personality traits, career progression, coaching styles, and narrative event generation.
- **Game Engine (`/engine`):** The low-level simulation core. It simulates individual game outcomes based on player ratings, team strategies, AI decisions, and a physics model.
- **Database (`/models`):** A highly detailed database schema managed with SQLAlchemy and Alembic. It models everything from player contracts and detailed attributes to game stats and team financial data.

### **2.3 Output Layer: The Living League**

The state of the simulated NFL world is presented to the user through the frontend. The UI dynamically updates to reflect the results of the user's decisions and the outcomes of the background simulation.

```text
/
  /backend
    /app
      /api
      /core
      /engine
      /models
      /orchestrator
      /rpg
      /schemas
    main.py
    requirements.txt
  /frontend
    /src
      /components
      /pages
      /services
    package.json
  ...
```

---

## 3.0 TASK EXECUTION FRAMEWORK: THE DEVELOPMENT ROADMAP

This represents a potential storyboard for the project's development and future.

### **STAGE 1: FOUNDATION & CORE MODELS**

- **[x] Define System Architecture Blueprint (`NFL-SIM-001`)**
- **[x] Technology Stack Selection**
  - `[x]` Backend: Python `FastAPI`
  - `[x]` Frontend: `React/Vite` with TypeScript
  - `[x]` Database: `PostgreSQL` / `SQLite` via `SQLAlchemy`
- **[x] Database Schema Implementation (`/models`)**
  - `[x]` Implement core models: `Player`, `Team`, `Game`, `Season`.
  - `[x]` Add detailed player attributes (skills, contract, RPG traits).
  - `[x]` Set up Alembic for database migrations.

### **STAGE 2: SIMULATION ENGINE IMPLEMENTATION**

- **[x] Task 2.1: Game Simulation Engine (`/engine`)**
  - `[x]` Develop play resolution logic.
  - `[x]` Implement basic AI for play-calling.
  - `[x]` Develop physics model for on-field action.
- **[x] Task 2.2: Season Orchestrator (`/orchestrator`)**
  - `[x]` Implement week-by-week season progression.
  - `[x]` Implement standings calculation.
  - `[x]` Implement playoff simulation logic.
- **[x] Task 2.3: Offseason Orchestrator**
  - `[x]` Implement player progression and regression logic (`/rpg`).
  - `[x]` Implement rookie generation and the NFL Draft.
  - `[x]` Implement free agency logic.

### **STAGE 3: FRONTEND UI & USER INTERACTION**

- **[x] Task 3.1: Setup Project Scaffolding**
  - `[x]` Initialize React/Vite project.
- **[x] Task 3.2: Build Core UI Views (`/pages`)**
  - `[x]` Implement Roster management screen.
  - `[x]` Implement Standings and Schedule views.
  - `[x]` Implement Player profile pages.
- **[x] Task 3.3: API Integration (`/services`)**
  - `[x]` Create services to fetch data from the FastAPI backend.
  - `[x]` Implement state management for the application (e.g., Zustand or Redux Toolkit).

### **STAGE 4: DEPLOYMENT & CONTINUOUS IMPROVEMENT**

- **[x] Task 4.1: Containerize the Application**
  - `[x]` Write a `Dockerfile` for the backend.
  - `[x]` Write a `Dockerfile` for the frontend.
  - `[x]` Create a `docker-compose.yml` for local development.
- **[ ] Task 4.2: Establish Testing Framework**
  - `[x]` Add unit tests for the simulation engine.
  - `[x]` Add API integration tests.
  - `[ ]` Add E2E tests for the frontend user flows.

---

## END OF DOCUMENT
