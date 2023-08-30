from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer
from utils.jwt_manager import validate_token

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)

        permiso = False

        for rol in data['roles']:
            if rol['name'] == 'Super admin' or rol['name'] == 'Admin':
                permiso = True

        if not permiso:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='No tiene un rol permitido')
    