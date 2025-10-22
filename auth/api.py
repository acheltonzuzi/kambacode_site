from ninja import Router, Schema
from ninja.security import HttpBearer
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.conf import settings
from ninja.errors import HttpError
import jwt
import datetime
from ninja_jwt.authentication import JWTAuth
# ---------------------------
# Configurações de token
# ---------------------------
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

# ---------------------------
# Schemas
# ---------------------------
class UserSchema(Schema):
    username: str
    password: str

class TokenSchema(Schema):
    access: str
    refresh: str

class RefreshSchema(Schema):
    refresh: str

class UserResponse(Schema):
    username:str
    is_authenticated:bool
    email:str=None
# ---------------------------
# Funções auxiliares
# ---------------------------
def create_access_token(user_id: int) -> str:
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        "iat": datetime.datetime.utcnow()
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

def create_refresh_token(user_id: int) -> str:
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
        "iat": datetime.datetime.utcnow()
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

# ---------------------------
# Router
# ---------------------------
router = Router()

# ---------------------------
# Login (gera access + refresh token)
# ---------------------------
@router.post("/login", response=TokenSchema)
def login_view(request, data: UserSchema):
    user = authenticate(username=data.username, password=data.password)
    if not user:
        raise HttpError(401, "Credenciais inválidas")

    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)
    return {"access": access_token, "refresh": refresh_token}

# ---------------------------
# Refresh token
# ---------------------------
@router.post("/refresh", response=TokenSchema)
def refresh_view(request, data: RefreshSchema):
    try:
        payload = jwt.decode(data.refresh, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("user_id")
        # Verifica se o usuário ainda existe
        get_object_or_404(User, id=user_id)

        access_token = create_access_token(user_id)
        refresh_token = create_refresh_token(user_id)  # opcional: gerar novo refresh token
        return {"access": access_token, "refresh": refresh_token}

    except jwt.ExpiredSignatureError:
        raise HttpError(401, "Refresh token expirado")
    except jwt.InvalidTokenError:
        raise HttpError(401, "Refresh token inválido")

# ---------------------------
# Authenticator para protected routes
# ---------------------------
class BearerAuth(HttpBearer):
    def authenticate(self, request, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user = get_object_or_404(User, id=payload["user_id"])
            return user
        except jwt.ExpiredSignatureError:
            raise HttpError(401, "Access token expirado")
        except jwt.InvalidTokenError:
            raise HttpError(401, "Access token inválido")

# ---------------------------
# Protected route
# ---------------------------
@router.get("/me",response=UserResponse, auth=JWTAuth())
def protected_view(request):
    return request.user
