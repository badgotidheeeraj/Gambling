from fastapi import FastAPI, Depends, APIRouter
from sqlalchemy.orm import Session
from configdb.connection import get_db
from schema.userSchema import UserCreate,PhoneRequest,PhoneRequest,OtpResponse
from services.LoginSingup import LoginService
from services.otpService import OtpVerify

app = FastAPI()
router = APIRouter()

@app.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    return LoginService.signup(user, db)

@app.post("/login")
def login(user: UserCreate, db: Session = Depends(get_db)):
    return LoginService.login(user, db)



# --- Route to send OTP ---
@app.post("/otp-send")
def send_otp(request: PhoneRequest, db: Session = Depends(get_db)):
    return OtpVerify.set_otp(request.phone, db)


@app.post("/otp-send", response_model=OtpResponse)
def send_otp(request: PhoneRequest, db: Session = Depends(get_db)):
    
    return OtpVerify.set_otp(request.phone, db)


app.include_router(router)
