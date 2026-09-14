from typing import Annotated
from fastapi import APIRouter, File, Form, UploadFile, status


resource_plan_router = APIRouter(prefix='/resource-plans')

@resource_plan_router.post('', status_code = status.HTTP_201_CREATED)
def create_resource_plan(target_name: Annotated[str, Form(min_length=2, strip_whitespace=True)], target_quantity: Annotated[int, Form(gt=0)], player_file: Annotated[UploadFile, File()]):
    return {'input_data': target_name}