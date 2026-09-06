from fastapi import APIRouter, status

auth_router = APIRouter(prefix='/auth')

@auth_router.post('/register', status_code = status.HTTP_201_CREATED)
async def register_user():
    return {'message': 'Success registration'}