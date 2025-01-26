from datetime import datetime
from typing import Dict, List
from app.schemas.discussion import Message, Vote

class DiscussionModel:
    def __init__(self):
        self.discussions: Dict[str, dict] = {}
        
    def create_discussion(self, discussion_id: str, topic: str) -> dict:
        discussion = {
            "id": discussion_id,
            "topic": topic,
            "status": "active",
            "messages": [],
            "votes": [],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "conclusion": None
        }
        self.discussions[discussion_id] = discussion
        return discussion
    
    def get_discussion(self, discussion_id: str) -> dict:
        return self.discussions.get(discussion_id)
    
    def list_discussions(self) -> List[dict]:
        return list(self.discussions.values())
    
    def add_message(self, discussion_id: str, message: Message) -> dict:
        discussion = self.discussions[discussion_id]
        discussion["messages"].append(message.dict())
        discussion["updated_at"] = datetime.utcnow()
        return discussion
    
    def add_vote(self, discussion_id: str, vote: Vote) -> dict:
        discussion = self.discussions[discussion_id]
        discussion["votes"].append(vote.dict())
        discussion["updated_at"] = datetime.utcnow()
        return discussion
    
    def set_conclusion(self, discussion_id: str, conclusion: str) -> dict:
        discussion = self.discussions[discussion_id]
        discussion["conclusion"] = conclusion
        discussion["status"] = "concluded"
        discussion["updated_at"] = datetime.utcnow()
        return discussion
