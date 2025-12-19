import jwt
import bcrypt
from datetime import datetime, timedelta
from django.conf import settings
from rest_framework import authentication, exceptions
from firebase_admin import firestore
from backend.firebase_init import db


def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


def generate_jwt_token(uid: str, email: str) -> dict:
    """Generate JWT access and refresh tokens"""
    access_payload = {
        'uid': uid,
        'email': email,
        'exp': datetime.utcnow() + timedelta(hours=1),
        'iat': datetime.utcnow(),
        'type': 'access'
    }
    
    refresh_payload = {
        'uid': uid,
        'email': email,
        'exp': datetime.utcnow() + timedelta(days=7),
        'iat': datetime.utcnow(),
        'type': 'refresh'
    }
    
    access_token = jwt.encode(access_payload, settings.SECRET_KEY, algorithm='HS256')
    refresh_token = jwt.encode(refresh_payload, settings.SECRET_KEY, algorithm='HS256')
    
    return {
        'access': access_token,
        'refresh': refresh_token,
        'expires_in': 3600
    }


def decode_jwt_token(token: str) -> dict:
    """Decode and verify JWT token"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        raise exceptions.AuthenticationFailed('Token has expired')
    except jwt.InvalidTokenError:
        raise exceptions.AuthenticationFailed('Invalid token')


class JWTAuthentication(authentication.BaseAuthentication):
    """Custom JWT authentication class for DRF"""
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return None
        
        try:
            prefix, token = auth_header.split(' ')
            if prefix.lower() != 'bearer':
                raise exceptions.AuthenticationFailed('Invalid authorization header format')
            
            payload = decode_jwt_token(token)
            
            if payload.get('type') != 'access':
                raise exceptions.AuthenticationFailed('Invalid token type')
            
            uid = payload.get('uid')
            if not uid:
                raise exceptions.AuthenticationFailed('Invalid token payload')
            
            doctor_ref = db.collection('doctors').document(uid)
            doctor_doc = doctor_ref.get()
            
            if not doctor_doc.exists:
                raise exceptions.AuthenticationFailed('User not found')
            
            doctor_data = doctor_doc.to_dict()
            
            class User:
                def __init__(self, uid, email, data):
                    self.uid = uid
                    self.email = email
                    self.data = data
                    self.is_authenticated = True
            
            user = User(uid, payload.get('email'), doctor_data)
            
            return (user, token)
            
        except ValueError:
            raise exceptions.AuthenticationFailed('Invalid authorization header format')
        except Exception as e:
            raise exceptions.AuthenticationFailed(str(e))
