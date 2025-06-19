from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional

from configdb.connection import get_db
from modelDB.userloginmodel import Users
from schema.userSchema import UserCreate

app = FastAPI()
router = APIRouter()

# ========== JWT SETTINGS ==========
SECRET_KEY = "your-super-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# ========== PASSWORD HASHING ==========
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ========== OAUTH2 ==========
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dummy user for demonstration
fake_users_db = {
    "alice": {
        "username": "alice",
        "hashed_password": pwd_context.hash("secret123"),
        "role": "admin"
    }
}

# ========== UTILITY FUNCTIONS ==========

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user(db_dict, username: str):
    return db_dict.get(username)

def authenticate_user(username: str, password: str):
    user = get_user(fake_users_db, username)
    if not user or not verify_password(password, user["hashed_password"]):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire, "sub": data.get("username")})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username)
    if user is None:
        raise credentials_exception
    return user

# ========== AUTH ROUTES ==========

@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    print(user)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    token = create_access_token({"username": user["username"]})
    return {"access_token": token, "token_type": "bearer"}

# ========== APP ROUTES ==========

@router.get("/")
def read_root(db: Session = Depends(get_db)):
    users = db.query(Users).all()
    return {"message": "Hello, FastAPI!", "data": users}

@router.post("/create-user")
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    new_user = Users(
        id=payload.id,
        email=payload.email,
        password=payload.password,  # Ideally, hash this!
        balance=payload.balance,
        phone=payload.phone,
        pic=payload.pic,
        created_at=payload.created_at,
        is_active=payload.is_active
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User added!", "user_id": new_user.id}

@router.put("/update-user/{id}")
def update_user(id: int, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Example field updates
    user.phone = "0000000000"
    db.commit()
    db.refresh(user)
    return {"message": "User updated!", "user_id": id}

@router.get("/protected")
def protected_route(current_user: dict = Depends(get_current_user)):
    return {"message": f"Hello, {current_user['username']}!"}

# Register routes
app.include_router(router)
