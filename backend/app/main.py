from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import system, simulation, data, websocket, teams, players, season, genesis

app = FastAPI(
    title="Stellar Sagan - NFL Simulation Engine",
    description="Backend API for the Stellar Sagan NFL Football Simulation.",
    version="0.1.0",
)

# CORS Configuration
origins = [
    "http://localhost:5173",  # Vite default
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(system.router)
app.include_router(simulation.router)
app.include_router(data.router)
app.include_router(websocket.router)
app.include_router(teams.router, prefix="/api/teams", tags=["teams"])
app.include_router(players.router, prefix="/api/players", tags=["players"])
app.include_router(season.router)
app.include_router(genesis.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Stellar Sagan NFL Simulation Engine"}
