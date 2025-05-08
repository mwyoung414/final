from functools import wraps
from quart import request, jsonify, current_app, render_template
import jwt

def token_required(f):
    @wraps(f)
    async def decorated(*args, **kwargs):
        token = None
        
        # Get token from cookies or Authorization header
        if 'access_token' in request.cookies:
            token = request.cookies.get('access_token')
        elif request.headers.get('Authorization'):
            auth_header = request.headers.get('Authorization')
            if auth_header.startswith('Bearer '):
                token = auth_header[7:]
        
        if not token:
            return jsonify({'message': 'Authentication required'}), 401
            
        try:
            # Get jwt_service from app
            jwt_service = current_app.JWT 
            
            # Verify token
            payload = jwt_service.verify_token(token)
            
            if not payload:
                return jsonify({'message': 'Token is invalid or expired'}), 401
                
            # Add user info to request
            request.user_id = payload.get('user_id')
            request.username = payload.get('username')
            request.role = payload.get('role')
            
        except Exception as e:
            return jsonify({'message': f'Authentication error: {str(e)}'}), 401
            
        return await f(*args, **kwargs)
    
    return decorated