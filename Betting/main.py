from fastapi import APIRouter, Depends, HTTPException,FastAPI

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


@router.put("/update/{id}")
def update_user(id: int, db: Session = Depends(get_db)):
    user = db.query(UserProfile).filter(UserProfile.id == id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Example of updating some fields manually:
    user.first_name = "Updated Name"
    user.phone = "0000000000"
    
    db.commit()
    db.refresh(user)
    
    return {"message": "User updated!", "user_id": id}


app.include_router(router)
