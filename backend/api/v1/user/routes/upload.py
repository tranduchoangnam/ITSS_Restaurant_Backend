from typing import Annotated

from fastapi import APIRouter, Depends, Body, File, UploadFile
from sqlmodel import Session
import backend.api.v1.user.services.dishes as dish_service
from backend.api.v1.dependencies.authentication import authorize_role, get_user_if_logged_in, get_current_user
from backend.core.response import authenticated_api_responses, public_api_responses
from backend.schemas.upload import UploadResponse
from backend.cloudinary.cloudinary import uploadImage
from backend.models.user import User
import datetime
router = APIRouter()

@router.post(
    "",
    response_model=UploadResponse,
    responses=public_api_responses,
)
def upload_image(
    user: Annotated[User, Depends(get_current_user)],
    file: UploadFile = File(...),
):
    # Generate unique filename
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = f"{user.email}_{timestamp}"
    file_content = file.file.read()
    return UploadResponse(url=uploadImage(file_content, file_name))
    