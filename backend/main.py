from datetime import datetime, timedelta, timezone
from fastapi import FastAPI, HTTPException, Depends, Request, Form, status
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from jose import JWTError, jwt
from typing import Annotated, Union
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from api.base import api_router
from core.config import engine, get_db, Base, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM
from core.hashing import Hasher
from models.users import Users
from schemas.users import Token


app = FastAPI()

templates = Jinja2Templates(directory="templates")

Base.metadata.create_all(bind=engine)
app.include_router(api_router)


db_dependency = Annotated[Session, Depends(get_db)]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")



@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


def authenticate_user(db: db_dependency, username: str, password: str):
    user = db.query(Users).filter(Users.username == username).first()
    if not user or not Hasher.verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: db_dependency):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"Payload: {payload}")
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        user = db.query(Users).filter(Users.username == username).first()
        if user is None:
            raise credentials_exception
        return user
        # token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    # user = db.query(Users).filter(Users.username == username).first()
    # print(f"User: {user}")
    # if user is None:
    #     raise credentials_exception
    # return user



@app.post("/login")
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()], db: db_dependency) -> Token:
    user = authenticate_user(db, username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    response = RedirectResponse(url="/employees",status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="Authorization", value=f"Bearer {access_token}", secure=True, httponly=True)
    return response
    # return Token(access_token=access_token, token_type="bearer")
    # return {"username": username}



