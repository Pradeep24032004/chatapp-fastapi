"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from .. import models, oauth2
from ..utils import dbAdaptor

router = APIRouter()
db = dbAdaptor.DBAdaptor()

@router.post("/message", response_model=models.MessageOut)
async def post_message(
    message: models.MessageCreate,
    current_user: dict = Depends(oauth2.get_current_user)
):
    user = await db.get_user_by_email(current_user["email"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    posted = await db.post_message(message.content, str(user["_id"]))
    if not posted:
        raise HTTPException(status_code=500, detail="Message could not be posted")
    return posted

@router.get("/messages", response_model=List[models.MessageOut])
async def get_messages(current_user: dict = Depends(oauth2.get_current_user)):
    return await db.get_all_messages()

@router.delete("/delete_message/{message_id}", status_code=204)
async def delete_message(
    message_id: str,
    current_user: dict = Depends(oauth2.get_current_user)
):
    user = await db.get_user_by_email(current_user["email"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    success = await db.delete_user_message(message_id, str(user["_id"]))
    if not success:
        raise HTTPException(status_code=403, detail="Not authorized to delete this message")

    return
""" 
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from .. import models, oauth2
from ..utils import dbAdaptor

router = APIRouter()
db = dbAdaptor.DBAdaptor()

@router.post("/message", response_model=models.MessageOut)
async def post_message(
    message: models.MessageCreate,
    current_user: dict = Depends(oauth2.get_current_user)
):
    user = await db.get_user_by_email(current_user["email"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    posted = await db.post_message(message.content, str(user["_id"]))
    if not posted:
        raise HTTPException(status_code=500, detail="Message could not be posted")
    
    # Add user_id to the response so frontend can identify current user
    posted["user_id"] = str(user["_id"])
    posted["email"] = current_user["email"]  # Add email for identification
    
    return posted

@router.get("/messages", response_model=List[models.MessageOut])
async def get_messages(current_user: dict = Depends(oauth2.get_current_user)):
    messages = await db.get_all_messages()
    
    # Add email information to each message for proper user identification
    for message in messages:
        # Get user info for each message
        user = await db.get_user_by_id(message["user_id"])
        if user:
            message["email"] = user["email"]
    
    return messages

@router.delete("/delete_message/{message_id}", status_code=204)
async def delete_message(
    message_id: str,
    current_user: dict = Depends(oauth2.get_current_user)
):
    user = await db.get_user_by_email(current_user["email"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    success = await db.delete_user_message(message_id, str(user["_id"]))
    if not success:
        raise HTTPException(status_code=403, detail="Not authorized to delete this message")

    return