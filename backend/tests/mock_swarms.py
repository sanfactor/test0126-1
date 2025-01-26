"""Mock implementation of swarms components for testing."""
import logging
from typing import List, Callable, Any, Optional

log = logging.getLogger(__name__)

class Agent:
    """Mock Agent class that simulates the basic behavior we need."""
    def __init__(
        self,
        agent_name: str,
        system_prompt: str,
        llm: Optional[Callable] = None,
        max_loops: int = 1,
        verbose: bool = False,
        output_type: str = "string",
        **kwargs  # Accept any additional kwargs
    ):
        self.agent_name = agent_name
        self.system_prompt = system_prompt
        self.llm = llm or (lambda x: f"Mock response from {agent_name}: Analysis based on {system_prompt}")
        self.max_loops = max_loops
        self.verbose = verbose
        self.output_type = output_type
        log.info(f"Created mock agent: {agent_name}")
        
    def __call__(self, prompt: str) -> str:
        """Simulate agent response."""
        try:
            if self.llm:
                response = self.llm(prompt)
                if self.verbose:
                    log.info(f"{self.agent_name} response: {response}")
                return response
            return f"Mock response from {self.agent_name}"
        except Exception as e:
            log.error(f"Error in {self.agent_name} processing: {str(e)}")
            return f"Error in {self.agent_name} processing: {str(e)}"

class GroupChat:
    """Mock GroupChat class."""
    def __init__(
        self,
        name: str,
        description: str,
        agents: List[Agent],
        speaker_fn: Callable = None,
        max_loops: int = 5
    ):
        self.name = name
        self.description = description
        self.agents = agents
        self.speaker_fn = speaker_fn
        self.max_loops = max_loops
        log.info(f"Created mock group chat: {name}")

def round_robin(agents: List[Agent], **kwargs) -> Agent:
    """Mock round_robin implementation."""
    return agents[0] if agents else None

class MajorityVoting:
    """Mock MajorityVoting class."""
    def __init__(
        self,
        name: str,
        description: str,
        agents: List[Agent],
        verbose: bool = True
    ):
        self.name = name
        self.description = description
        self.agents = agents
        self.verbose = verbose
        log.info(f"Created mock voting system: {name}")
