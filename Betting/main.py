from fastapi import FastAPI, APIRouter, Depends
from sqlalchemy.orm import Session
from configdb.connection import get_db
from modelDB.datascript import UserProfile
from schema.userSchema import UserCreate

app = FastAPI()
router = APIRouter()

# Example endpoint
@router.get("/")
def read_root():
    db = next(get_db())
    print(db.query(UserProfile).all())
    return {"message": "Hello, FastAPI!" ,"Data":db.query(UserProfile).all()}

@router.post("/code")
def correction(payload: UserCreate, db: Session = Depends(get_db)):
    new_user = UserProfile(
    first_name=payload.first_name,
    last_name=payload.last_name,
    password=payload.password,
    age=payload.age,
    email=payload.email,
    phone=payload.phone,
    address=payload.address,
    pic=payload.pic,
    dob=payload.dob
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User added!", "user_id": new_user.id}


app.include_router(router)
