from channels.db import database_sync_to_async
from django.contrib.auth.models import User,AnonymousUser
import jwt
from .settings import SECRET_KEY
from jwt.exceptions import InvalidSignatureError
@database_sync_to_async
def get_user(user_id):
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return AnonymousUser()

class JWTAuthentication:
    """
    Custom middleware (insecure) that takes user IDs from the query string.
    """

    def __init__(self, app):
        # Store the ASGI application we were passed
        self.app = app

    async def __call__(self, scope, receive, send):
        # Look up user from query string (you should also do things like
        # checking if it is a valid user ID, or if scope["user"] is already
        # populated).
        
        token = scope['query_string'].decode().split('=')[-1]

        try:
            decoded_token = jwt.decode(token,SECRET_KEY,algorithms=['HS256'])
            scope['user'] = await get_user(decoded_token.get('user_id'))
        except Exception:
            scope['user']=AnonymousUser()
        return await self.app(scope, receive, send)