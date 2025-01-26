from typing import List, Dict
import os
import logging
import traceback
from openai import OpenAI

# Get logger for this module
log = logging.getLogger(__name__)

try:
    if os.getenv("USE_MOCK_SWARMS", "false").lower() == "true":
        log.info("Using mock swarms implementation for testing...")
        from tests.mock_swarms import Agent, GroupChat, MajorityVoting, round_robin
    else:
        # Import components directly from their modules to avoid initialization issues
        log.info("Importing swarms components directly from modules...")
        from swarms.structs.agent import Agent
        from swarms.structs.groupchat import GroupChat, round_robin
        from swarms.structs.majority_voting import MajorityVoting
    
    log.info("All required components imported successfully")
except ImportError as e:
    log.error(f"Error importing components: {str(e)}")
    log.error(f"Traceback: {traceback.format_exc()}")
    raise
except Exception as e:
    log.error(f"Unexpected error during import: {str(e)}")
    log.error(f"Traceback: {traceback.format_exc()}")
    raise

from app.schemas.discussion import AgentRole

# Initialize OpenAI client
try:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        log.warning("No OpenAI API key found. Using dummy responses for testing.")
        # For testing without API key, we'll return mock responses
        client = None
    else:
        log.info("Initializing OpenAI client with provided API key")
        client = OpenAI(api_key=api_key)
except Exception as e:
    log.error(f"Error initializing OpenAI client: {str(e)}")
    logger.error(f"Traceback: {traceback.format_exc()}")
    client = None

class AgentService:
    def __init__(self):
        self._agent_cache = {}
        self._agent_configs = {
            AgentRole.MARKET_ANALYST: "Analyzes market trends and token performance metrics",
            AgentRole.SECURITY_EXPERT: "Evaluates technical security aspects of blockchain projects",
            AgentRole.TOKEN_ECONOMIST: "Assesses token economics and monetary policies",
            AgentRole.COMPLIANCE_SPECIALIST: "Reviews regulatory compliance and legal implications",
            AgentRole.GOVERNANCE_EXPERT: "Analyzes governance mechanisms and DAO structures",
            AgentRole.RISK_ASSESSOR: "Evaluates investment risks and potential vulnerabilities",
            AgentRole.INFRASTRUCTURE_ANALYST: "Reviews blockchain infrastructure and scalability",
            AgentRole.MEMECOIN_STRATEGIST: "Specializes in memecoin dynamics and social impact",
            AgentRole.ECOSYSTEM_EVALUATOR: "Assesses overall ecosystem health and integration"
        }
        
    def get_agent(self, role: AgentRole) -> Agent:
        """Get an agent for the specified role, creating it if it doesn't exist."""
        try:
            if role not in self._agent_cache:
                log.info(f"Creating new agent for role: {role.value}")
                description = self._agent_configs[role]
                role_completion_fn = self._create_completion_fn(role.value, description)
                
                log.info(f"Initializing agent with role: {role.value}")
                self._agent_cache[role] = Agent(
                    agent_name=role.value,
                    system_prompt=description,
                    llm=role_completion_fn,
                    max_loops=1,
                    verbose=True
                )
                log.info(f"Successfully created agent for role: {role.value}")
            else:
                log.info(f"Using cached agent for role: {role.value}")
            
            return self._agent_cache[role]
        except Exception as e:
            log.error(f"Error creating agent for role {role.value}: {str(e)}")
            log.error(f"Traceback: {traceback.format_exc()}")
            raise
        
    def _create_completion_fn(self, role: str, description: str):
        """Create a completion function for the specified role."""
        try:
            # Use OpenAI client directly
            model_name = os.getenv("MODEL_NAME", "gpt-4-1106-preview")
            temperature = float(os.getenv("TEMPERATURE", "0.7"))
            
            def completion_fn(prompt: str) -> str:
                try:
                    system_prompt = f"""You are a Web3 expert specializing as a {role}. {description}.
                    Your role is to analyze Web3 and blockchain projects objectively, focusing on your area of expertise.
                    
                    Guidelines:
                    1. Stay focused on your specific area of expertise
                    2. Provide clear, factual analysis
                    3. Support arguments with specific examples
                    4. Consider both advantages and risks
                    5. Be objective and professional
                    6. Communicate clearly in English
                    
                    When voting:
                    - Clearly state APPROVE or REJECT
                    - Provide detailed reasoning based on your expertise
                    - Consider long-term implications"""
                    
                    if client is None:
                        # Return mock response for testing
                        log.info(f"Generating mock response for {role}")
                        return f"Mock response from {role}: Analysis of the topic based on {description}"
                    
                    log.info(f"Making OpenAI API call for {role}")
                    response = client.chat.completions.create(
                        model=model_name,
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=temperature
                    )
                    return response.choices[0].message.content
                except Exception as e:
                    log.error(f"Error in OpenAI completion for {role}: {str(e)}")
                    return f"Error in processing request for {role}"
            
            return completion_fn
        except Exception as e:
            log.error(f"Error creating completion function: {str(e)}")
            raise

    def _get_active_agents(self) -> List[Agent]:
        """Get a list of all currently initialized agents."""
        return list(self._agent_cache.values())

    def _setup_group_chat(self, agents: List[Agent]) -> GroupChat:
        """Create a new group chat with the specified agents."""
        return GroupChat(
            name="TokenCourt Discussion",
            description="A roundtable discussion of Web3 and blockchain topics by specialized agents",
            agents=agents,
            speaker_fn=round_robin,
            max_loops=5
        )

    def _setup_voting(self, agents: List[Agent]) -> MajorityVoting:
        """Create a new voting instance with the specified agents."""
        return MajorityVoting(
            name="TokenCourt Voting",
            description="Voting system for Web3 and blockchain topic evaluation",
            agents=agents,
            verbose=True
        )

    async def discuss_topic(self, topic: str) -> List[dict]:
        try:
            log.info(f"Starting discussion for topic: {topic}")
            messages = []
            
            # Process each role sequentially to minimize memory usage
            for role in self._agent_configs.keys():
                try:
                    agent = self.get_agent(role)
                    discussion_prompt = f"""Please analyze the following topic from your perspective as a {role.value}:
                    
                    Topic: {topic}
                    
                    Consider:
                    - Technical feasibility and implementation
                    - Market potential and adoption
                    - Security implications
                    - Regulatory compliance
                    - Economic sustainability
                    - Risk factors
                    - Infrastructure requirements
                    - Social impact
                    
                    Focus on aspects most relevant to your expertise as {role.value}.
                    Provide a clear, concise analysis in 2-3 paragraphs."""

                    log.info(f"Getting response from agent: {role.value}")
                    response = agent.llm(discussion_prompt)
                    
                    messages.append({
                        "agent_id": role.value,
                        "content": response.strip() if response else "No response provided",
                        "role": role
                    })
                    log.info(f"Received response from {role.value}")
                    
                except Exception as e:
                    log.error(f"Error getting response from {role.value}: {str(e)}")
                    messages.append({
                        "agent_id": role.value,
                        "content": f"Error in analysis: {str(e)}",
                        "role": role
                    })
            
            log.info(f"Completed discussion with {len(messages)} responses")
            # Clean up resources after discussion
            self._cleanup_agents()
            return messages
        except Exception as e:
            log.error(f"Error in discuss_topic: {str(e)}")
            raise

    async def collect_votes(self, topic: str) -> List[dict]:
        try:
            log.info(f"Starting voting process for topic: {topic}")
            votes = []
            
            # Process each role sequentially to minimize memory usage
            for role in self._agent_configs.keys():
                try:
                    agent = self.get_agent(role)
                    voting_prompt = f"""Based on your analysis as a {role.value} of the topic: {topic}

                    Please vote on whether to APPROVE or REJECT this proposal.
                    
                    Your response MUST follow this exact format:
                    VOTE: [APPROVE or REJECT]
                    REASONING: [Your detailed explanation supporting your vote from your perspective as {role.value}]
                    
                    Keep your reasoning focused on your area of expertise."""
                    
                    log.info(f"Getting vote from agent: {role.value}")
                    response = agent.llm(voting_prompt)
                    
                    # Parse the response
                    lines = response.lower().split('\n')
                    vote_line = next((line for line in lines if 'vote:' in line), '')
                    reasoning_line = next((line for line in lines if 'reasoning:' in line), '')
                    
                    choice = 'approve' if 'approve' in vote_line else 'reject'
                    reasoning = reasoning_line.split('reasoning:', 1)[1].strip() if 'reasoning:' in reasoning_line else "No reasoning provided"
                    
                    votes.append({
                        "agent_id": role.value,
                        "choice": choice,
                        "reasoning": reasoning
                    })
                    log.info(f"Received vote from {role.value}: {choice}")
                    
                except Exception as e:
                    log.error(f"Error getting vote from {role.value}: {str(e)}")
                    votes.append({
                        "agent_id": role.value,
                        "choice": "reject",
                        "reasoning": f"Error in voting process: {str(e)}"
                    })
            
            log.info(f"Completed voting with {len(votes)} votes")
            # Clean up agents after voting is complete
            self._cleanup_agents()
            return votes
        except Exception as e:
            log.error(f"Error in collect_votes: {str(e)}")
            raise
            
    def _cleanup_agents(self):
        """Clean up agent resources to free memory.
        
        This method:
        1. Clears the agent cache to free memory
        2. Ensures proper cleanup of any cached states
        3. Logs cleanup operations for monitoring
        """
        log.info("Starting agent resource cleanup")
        
        # Clean up each agent's resources individually
        for role, agent in self._agent_cache.items():
            try:
                # Clear any cached states or memory
                if hasattr(agent, 'llm') and hasattr(agent.llm, '__closure__'):
                    agent.llm = None
                log.info(f"Cleaned up agent resources for {role.value}")
            except Exception as e:
                log.error(f"Error cleaning up agent {role.value}: {str(e)}")
        
        # Clear the entire cache
        self._agent_cache.clear()
        log.info("Completed agent resource cleanup")
