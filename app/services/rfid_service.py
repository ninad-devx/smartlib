from app.models.user import User

def link_rfid(db,user_id,rfid_uid):
    existing=(
        db.query(User).filter(User.rfid_uid==rfid_uid).first()
    )

    if existing:
        return False,"RFID ALREADY LINKED"
    
    user=db.get(User,user_id)

    if not user:
        return False,"User not found"
    
    user.rfid_uid=rfid_uid
    db.commit()

    return True,"RFID LINKED SUCCESFULLY"