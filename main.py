from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from schemas import UserCreate, UserResponse, UserLogin, Token
from auth import hash_password, verify_password, create_access_token, get_current_user, get_db
from models import User
from sqlalchemy.orm import Session

# Инициализация FastAPI
app = FastAPI()

# Эндпоинт для регистрации пользователя
@app.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # Хешируем пароль
    hashed_password = hash_password(user.password)
    # Создаём нового пользователя
    db_user = User(username=user.username, password_hash=hashed_password)
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        # Если username уже существует
        db.rollback()
        raise HTTPException(status_code=400, detail="Username already registered")

# Эндпоинт для входа пользователя
@app.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    # Ищем пользователя в базе
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Создаём токен
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Тестовый защищённый эндпоинт
@app.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user