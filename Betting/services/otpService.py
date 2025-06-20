import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from modelDB.userloginmodel import Users
from modelDB.otpModel import Otp


class OtpVerify:
    @staticmethod
    def generate_otp(length=4):
        return ''.join([str(random.randint(0, 9)) for _ in range(length)])

    @staticmethod
    def set_otp(username: str, db: Session):
        user = db.query(Users).filter_by(username=username).first()
        if not user:
            print(f"User '{username}' not found. Creating new user.")
            user = Users(username=username)
            db.add(user)
            db.flush() 
            
        otp_code = OtpVerify.generate_otp()
        print(f"Generated OTP for {username}: {otp_code}")
        if user.otp:
            user.otp.otp = otp_code
            user.otp.otp_created_at = datetime.utcnow()
            user.otp.is_verified = False
        else:
            # Create a new OTP entry
            otp_entry = Otp(
                otp=otp_code,
                otp_created_at=datetime.utcnow(),
                user=user
            )
            db.add(otp_entry)

        db.commit()
        return {"username": username, "otp": otp_code}
    
    
    
    
    @staticmethod
    def verify_otp(username, otp_input, db: Session, expiry_minutes=5):
        user = db.query(Users).filter_by(username=username).first()
        
        if not user or not user.otp:
            return False, "User or OTP not found."

        otp_entry = user.otp

        if otp_entry.otp != otp_input:
            return False, "Invalid OTP."

        if datetime.utcnow() - otp_entry.otp_created_at > timedelta(minutes=expiry_minutes):
            return False, "OTP expired."

        otp_entry.is_verified = True
        otp_entry.otp = None  # Invalidate OTP
        db.commit()
        return True, "OTP verified successfully!"
