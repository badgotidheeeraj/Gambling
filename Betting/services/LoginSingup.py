from fastapi import  HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from modelDB.userloginmodel import Users
from schema.userSchema import LoginSchema,UserCreate
from .auth import JWTToken

class LoginService:
    @staticmethod
    def signup(user: UserCreate, db: Session):
    # Check if username already exists
        db_user = db.query(Users).filter(Users.username == user.username).first()
        if db_user:
            raise HTTPException(status_code=400, detail="Username already exists")

        # Hash the user's password
        hashed_password = JWTToken.hash_password(user.password)

        # Create new user instance
        new_user = Users(
            username=user.username,
            email=user.email,
            password=hashed_password,
            phone=user.phone,
            created_at=datetime.utcnow().date()
        )

        # Add and save to database
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {"message": "User created successfully"}

    @staticmethod
    def login(user: LoginSchema, db: Session):
        
        db_user = db.query(Users).filter(Users.username == user.username).first()
        if not db_user:
            raise HTTPException(status_code=400, detail="Invalid username or password")

        if not JWTToken.verify_password(user.password, db_user.password):
            raise HTTPException(status_code=400, detail="Invalid username or password")

        token = JWTToken.create_access_token(data={"sub": db_user.username})
        return {"access_token": token, "token_type": "bearer"}



