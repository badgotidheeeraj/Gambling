from fastapi import FastAPI, WebSocket,Depends, APIRouter
from sqlalchemy.orm import Session
from configdb.connection import get_db
from schema.userSchema import UserCreate,PhoneRequest,PhoneRequest,OtpResponse
from services.LoginSingup import LoginService
from services.otpService import OtpVerify
from services.dashBoard import GamePlay


app = FastAPI()
router = APIRouter()

@app.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    return LoginService.signup(user, db)

@app.post("/login")
def login(user: UserCreate, db: Session = Depends(get_db)):
    return LoginService.login(user, db)

# --- Route to send OTP ---
@app.post("/otp-send", response_model=OtpResponse)
def send_otp(request: PhoneRequest, db: Session = Depends(get_db)):
    
    return OtpVerify.set_otp(request.phone, db)

@app.get("/dashboard-app")
def dashboard():
    result = GamePlay.run_game_loop(tick_speed=0.01)
    return {
        "status": "Game finished",
        "crash_point": result["crash_point"],
        "multiplier_history": result["multiplier_history"]
    }

# WebSocket impleamnt here
@app.websocket("/ws/game")
async def websocket_game(websocket: WebSocket):
    await websocket.accept()
    await GamePlay.run_game_loop(websocket)



@app.post("/cash-in")
async def cashIN(cash:cashSchema):
   
    return GamePlay.run_game_loop(cash.cash,cash.gamePoint)




app.include_router(router)


















"""
    bet = 100
player_cashout_at = 2.0  # Player decides to cash out at 2x
crash = generate_crash_point()
print(f"Crash Point: {crash}x")

multis = run_game_loop(crash)
win, amount = cash_out(multis, player_cashout_at, bet)


if win:
    print(f"✅ Cashed out at {player_cashout_at}x! You win: ${amount}")
else:
    print("💥 You crashed! You lose your bet.")
"""
