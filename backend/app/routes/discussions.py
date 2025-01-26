from fastapi import APIRouter, HTTPException
from typing import List
import uuid
from datetime import datetime
from loguru import logger

from app.schemas.discussion import Discussion, Message, Vote
from app.models.discussion import DiscussionModel
from app.services.agent_service import AgentService

router = APIRouter()
discussion_model = DiscussionModel()
agent_service = AgentService()

from pydantic import BaseModel

class TopicRequest(BaseModel):
    topic: str

@router.post("/discussions", response_model=Discussion)
async def create_discussion(request: TopicRequest):
    discussion_id = str(uuid.uuid4())
    logger.info(f"Creating new discussion with ID: {discussion_id}")
    discussion = discussion_model.create_discussion(discussion_id, request.topic)
    
    try:
        # Start the discussion among agents
        logger.info(f"Starting discussion for topic: {request.topic}")
        messages = await agent_service.discuss_topic(request.topic)
        logger.info(f"Received {len(messages)} messages from agents")
        
        for msg in messages:
            try:
                message = Message(
                    agent_id=msg["agent_id"],
                    content=msg["content"],
                    role=msg["role"],
                    timestamp=datetime.utcnow()
                )
                discussion_model.add_message(discussion_id, message)
            except Exception as msg_error:
                logger.error(f"Error processing message: {str(msg_error)}, Message: {msg}")
                continue
        
        # Collect votes after discussion
        logger.info("Collecting votes from agents")
        votes = await agent_service.collect_votes(request.topic)
        logger.info(f"Received {len(votes)} votes from agents")
        
        for vote in votes:
            try:
                vote_obj = Vote(
                    agent_id=vote["agent_id"],
                    choice=vote["choice"],
                    reasoning=vote["reasoning"],
                    timestamp=datetime.utcnow()
                )
                discussion_model.add_vote(discussion_id, vote_obj)
            except Exception as vote_error:
                logger.error(f"Error processing vote: {str(vote_error)}, Vote: {vote}")
                continue
                
        # Determine conclusion based on majority vote
        approve_count = sum(1 for v in votes if v["choice"] == "approve")
        total_votes = len(votes)
        conclusion = f"Proposal {'APPROVED' if approve_count > total_votes/2 else 'REJECTED'}"
        discussion_model.set_conclusion(discussion_id, conclusion)
        
        logger.info(f"Discussion {discussion_id} completed successfully")
        return discussion_model.get_discussion(discussion_id)
        
    except Exception as e:
        logger.error(f"Error in discussion process: {str(e)}")
        # Create a minimal valid response even in case of error
        discussion_model.set_conclusion(discussion_id, "ERROR: Discussion could not be completed")
        return discussion_model.get_discussion(discussion_id)

@router.get("/discussions", response_model=List[Discussion])
async def list_discussions():
    return discussion_model.list_discussions()

@router.get("/discussions/{discussion_id}", response_model=Discussion)
async def get_discussion(discussion_id: str):
    discussion = discussion_model.get_discussion(discussion_id)
    if not discussion:
        raise HTTPException(status_code=404, detail="Discussion not found")
    return discussion

@router.get("/debug/agents")
async def debug_agents():
    """Debug endpoint to verify agent initialization"""
    try:
        agents = agent_service.agents
        return {
            "status": "success",
            "agent_count": len(agents),
            "agent_roles": [role.value for role in agents.keys()]
        }
    except Exception as e:
        logger.error(f"Error in debug endpoint: {str(e)}")
        return {
            "status": "error",
            "message": str(e)
        }
