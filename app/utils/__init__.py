import jwt
from datetime import datetime, timezone, timedelta
from functools import wraps
from flask import request, jsonify
import os

SECRET_KEY = os.environ.get('SECRET_KEY') or 'blueSecrets'
TOKEN_EXPIRATION_HOURS = int(os.environ.get('TOKEN_EXPIRATION_HOURS', 1))

def encode_token(customer_id):
    payload = {
        'exp': datetime.now(timezone.utc) + timedelta(hours=TOKEN_EXPIRATION_HOURS),
        'iat': datetime.now(timezone.utc),
        'sub': str(customer_id)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return {"error": "Token has expired", "status_code": 403}
    except jwt.InvalidSignatureError:
        return {"error": "Invalid token signature", "status_code": 403}
    except jwt.DecodeError:
        return {"error": "Invalid token format", "status_code": 403}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token", "status_code": 403}

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' not in request.headers or not request.headers['Authorization'].startswith('Bearer '):
            print("Authorization header is missing or improperly formatted")
            return jsonify({'error': 'Invalid Authorization header format!'}), 400

        token = request.headers['Authorization'].split()[1]

        if not token:
            print("Token is missing")
            return jsonify({'error': 'Token is missing'}), 403

        decoded_token = decode_token(token)
        if isinstance(decoded_token, dict) and "status_code" in decoded_token:
            print(f"Token validation failed: {decoded_token['error']}")
            return jsonify({'error': decoded_token["error"]}), decoded_token["status_code"]

        customer_id = decoded_token['sub']
        print(f"Token decoded successfully: {decoded_token}")
        return f(customer_id, *args, **kwargs)
    return decorated
'''
import jwt
from datetime import datetime, timezone, timedelta
from functools import wraps
from flask import request, jsonify
import os

SECRET_KEY = os.environ.get('SECRET_KEY') or 'blueSecrets'
TOKEN_EXPIRATION_HOURS = int(os.environ.get('TOKEN_EXPIRATION_HOURS', 1))

def encode_token(customer_id):
    payload = {
        'exp': datetime.now(timezone.utc) + timedelta(hours=TOKEN_EXPIRATION_HOURS),
        'iat': datetime.now(timezone.utc),
        'sub': str(customer_id)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except jwt.InvalidSignatureError:
        raise ValueError("Invalid token signature")
    except jwt.DecodeError:
        raise ValueError("Invalid token format")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' not in request.headers or not request.headers['Authorization'].startswith('Bearer '):
            print("Authorization header is missing or improperly formatted")  # Debug
            return jsonify({'error': 'Invalid Authorization header format!'}), 400
        
        token = request.headers['Authorization'].split()[1]

        if not token:
            print("Token is missing")  # Debug
            return jsonify({'error': 'Token is missing'}), 403

        try:
            data = decode_token(token)
            customer_id = data['sub']
            print(f"Token decoded successfully: {data}")  # Log full payload
        except jwt.ExpiredSignatureError:
            print("Token expired")  # Debug
            return jsonify({'error': 'Token has expired'}), 403
        except jwt.InvalidTokenError as e:
            print(f"Token validation failed: {str(e)}")  # Debug
            return jsonify({'error': 'Invalid token'}), 403

        return f(customer_id, *args, **kwargs)
    return decorated
'''