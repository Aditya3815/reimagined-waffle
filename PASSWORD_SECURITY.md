# Password Encryption & Security Guide

## How Password Encryption Works in Your System

Your application uses **bcrypt** for password hashing, which is one of the most secure password hashing algorithms available.

---

## Password Encryption Flow

### 1. **Registration (Password Storage)**

When a user registers (doctor or patient):

```python
# In doctors/auth.py and patients/views.py

import bcrypt

def hash_password(password):
    """Hash password using bcrypt"""
    salt = bcrypt.gensalt()  # Generate a random salt
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

# During registration:
password_hash = hash_password(user_password)
# Store password_hash in Firestore, NOT the plain password
```

**What happens:**
1. User enters password: `"Doctor123"`
2. bcrypt generates a random salt
3. Password + salt = hashed password
4. Result stored in database: `$2b$12$abcdef...xyz` (60 characters)
5. **Original password is NEVER stored!**

---

### 2. **Login (Password Verification)**

When a user logs in:

```python
# In doctors/auth.py

def verify_password(plain_password, hashed_password):
    """Verify password against hash"""
    return bcrypt.checkpw(
        plain_password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )

# During login:
is_valid = verify_password(entered_password, stored_hash)
if is_valid:
    # Generate JWT token
    # Login successful
else:
    # Login failed
```

**What happens:**
1. User enters password: `"Doctor123"`
2. System retrieves stored hash from database
3. bcrypt compares entered password with hash
4. Returns True/False (password match or not)
5. **Password is never decrypted - only compared!**

---

## Why bcrypt is Secure

### 1. **One-Way Hashing**
- You CANNOT reverse a bcrypt hash to get the original password
- Even if database is stolen, passwords are safe

### 2. **Salt**
- Each password gets a unique random salt
- Same password = different hashes for different users
- Prevents rainbow table attacks

### 3. **Adaptive Cost**
- bcrypt is intentionally slow (configurable)
- Makes brute-force attacks impractical
- Can increase difficulty as computers get faster

---

## Example in Your Code

### Doctor Registration (doctors/views.py)

```python
class DoctorRegistrationView(APIView):
    def post(self, request):
        # Get password from request
        password = validated_data['password']
        
        # Hash the password using bcrypt
        password_hash = hash_password(password)
        
        # Store in Firestore
        doctor_data = {
            'email': email,
            'password_hash': password_hash,  # Hashed, not plain!
            'first_name': first_name,
            # ... other fields
        }
        
        db.collection('doctors').document(doctor_uid).set(doctor_data)
```

### Doctor Login (doctors/views.py)

```python
class DoctorLoginView(APIView):
    def post(self, request):
        # Get doctor from database
        doctor_data = doctor_doc.to_dict()
        stored_hash = doctor_data['password_hash']
        
        # Verify password
        if not verify_password(password, stored_hash):
            return Response({'error': 'Invalid credentials'}, 401)
        
        # Generate JWT tokens
        access_token = generate_access_token(doctor_data)
        refresh_token = generate_refresh_token(doctor_data)
        
        return Response({
            'tokens': {
                'access': access_token,
                'refresh': refresh_token
            }
        })
```

---

## Password Hash Format

A bcrypt hash looks like this:
```
$2b$12$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p92ldGxad68LJZdL17lhWy
```

Breaking it down:
- `$2b$` - bcrypt algorithm version
- `12$` - cost factor (2^12 iterations)
- `N9qo8uLOickgx2ZMRZoMye` - salt (22 characters)
- `IjZAgcfl7p92ldGxad68LJZdL17lhWy` - hash (31 characters)

---

## Security Best Practices Implemented

### ✅ 1. Password Hashing
- Using bcrypt (industry standard)
- Passwords never stored in plain text
- Each password has unique salt

### ✅ 2. Password Requirements
- Minimum 8 characters (enforced in serializers)
- Password confirmation on registration

### ✅ 3. JWT Tokens
- Access tokens for authentication
- Refresh tokens for renewal
- Tokens expire after set time

### ✅ 4. HTTPS (Production)
- All data encrypted in transit
- Passwords never sent unencrypted

---

## How to Test Password Security

### 1. Check Database
```python
# In Firestore, you'll see:
{
  "email": "dr.smith@hospital.com",
  "password_hash": "$2b$12$abc...xyz",  # Hashed!
  "first_name": "John"
}
```

### 2. Try Same Password for Different Users
```python
# User 1 registers with "Password123"
# Hash: $2b$12$abc...xyz

# User 2 registers with "Password123"  
# Hash: $2b$12$def...uvw  # Different hash!
```

### 3. Verify Login Works
```bash
# Register
curl -X POST http://127.0.0.1:8000/api/doctors/register/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"Test123","password_confirm":"Test123",...}'

# Login with same password
curl -X POST http://127.0.0.1:8000/api/doctors/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"Test123"}'

# Returns JWT tokens if password matches!
```

---

## Common Questions

### Q: Can I recover a user's password?
**A: No!** Passwords are hashed, not encrypted. You can only reset them, not recover them.

### Q: Why does the same password create different hashes?
**A: Salt!** Each password gets a unique random salt, making each hash unique.

### Q: Is bcrypt better than SHA256?
**A: Yes!** bcrypt is designed for passwords. It's slower (good for security) and includes salt automatically.

### Q: What if someone steals the database?
**A: Passwords are still safe!** Without the original password, the hashes are useless. Brute-forcing bcrypt takes years.

---

## Code Locations

**Password Hashing Functions:**
- `backend/doctors/auth.py` - Lines 15-25

**Doctor Registration:**
- `backend/doctors/views.py` - DoctorRegistrationView

**Doctor Login:**
- `backend/doctors/views.py` - DoctorLoginView

**Patient Registration:**
- `backend/patients/views.py` - PatientRegistrationView

**Patient Login:**
- `backend/patients/views.py` - PatientLoginView

---

## Additional Security Measures

### 1. Rate Limiting (Recommended for Production)
```python
# Add to settings.py
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',  # Limit login attempts
    }
}
```

### 2. Account Lockout (Future Enhancement)
- Lock account after 5 failed login attempts
- Require email verification to unlock

### 3. Password Strength Validation (Future Enhancement)
- Require uppercase, lowercase, numbers, special chars
- Check against common password lists

---

## Summary

✅ **Your passwords are secure!**
- Hashed with bcrypt (industry standard)
- Unique salt for each password
- Cannot be reversed or decrypted
- Safe even if database is compromised

✅ **Login process is secure!**
- Passwords verified without decryption
- JWT tokens for session management
- Tokens expire automatically

✅ **Best practices followed!**
- No plain text passwords
- Secure comparison
- Modern encryption standards
