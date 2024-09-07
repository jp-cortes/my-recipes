from fastapi import status
from fastapi.responses import JSONResponse

def validate_user(user, db, model, hash_password):
    #check if the user already exist
    valid_user = db.query(model).filter(model.email == user.email).first()
    
    # encode the password
    hashed_password = hash_password(user.password)

    # if the user is not registered yet will throw an error
    if not valid_user:
        return JSONResponse(content={"message":"You don't have an account yet"}, status_code=status.HTTP_404_NOT_FOUND)

    # compare the  actual password with passwod in the data base
    elif valid_user.password != hashed_password:
        return JSONResponse(content={"message":"Wrong credentials"}, status_code=status.HTTP_401_UNAUTHORIZED)
        