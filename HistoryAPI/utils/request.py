from fastapi import Request
from typing import Optional
from schemas.auth import JWTUserData

class CustomRequest(Request):
    def __init__(self, scope, receive, send):
        super().__init__(scope, receive, send)
        self.user: JWTUserData = None
