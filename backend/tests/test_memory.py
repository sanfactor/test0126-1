import asyncio
import os
import sys
import psutil
import signal
import traceback
from pathlib import Path
import logging
from functools import partial
from typing import Optional
from concurrent.futures import ThreadPoolExecutor, TimeoutError

def timeout_handler(signum, frame):
    raise TimeoutError("Operation timed out")

print("Starting test script...")  # Immediate feedback
print(f"Current directory: {os.getcwd()}")
print(f"Python path: {sys.path}")
print("Setting up logging...")

# Set up signal handler for timeout
signal.signal(signal.SIGALRM, timeout_handler)

def import_with_timeout(module_name: str, timeout: int = 10) -> Optional[object]:
    """Import a module with timeout."""
    try:
        signal.alarm(timeout)
        if module_name == "swarms":
            import swarms
            return swarms
        elif module_name == "swarms.components":
            from swarms import Agent, GroupChat, MajorityVoting
            return (Agent, GroupChat, MajorityVoting)
        elif module_name == "round_robin":
            from swarms.structs.groupchat import round_robin
            return round_robin
    except Exception as e:
        log.error(f"Error importing {module_name}: {str(e)}")
        raise
    finally:
        signal.alarm(0)

# Add the project root to Python path
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

try:
    from app.services.agent_service import AgentService
except ImportError as e:
    logging.error(f"Import error: {e}")
    logging.error(f"Python path: {sys.path}")
    logging.error(f"Traceback: {traceback.format_exc()}")
    raise

# Ensure logs directory exists
log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'memory_test.log')

# Configure logging with more detailed format and module-specific levels
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s | %(name)s | %(levelname)s | %(message)s | %(pathname)s:%(lineno)d',
    handlers=[
        logging.FileHandler(log_file, mode='w', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

# Set specific logging levels for key modules
for module in ['swarms', 'app', 'asyncio', '__main__']:
    module_logger = logging.getLogger(module)
    module_logger.setLevel(logging.DEBUG)
    # Ensure all handlers propagate
    module_logger.propagate = True

# Get logger for this module
log = logging.getLogger(__name__)

# Test log file creation
try:
    log.info("Logging initialized successfully")
    log.info(f"Log file location: {log_file}")
    if os.path.exists(log_file):
        log.info("Log file created successfully")
        log.info(f"Log file size: {os.path.getsize(log_file)} bytes")
    else:
        log.error("Failed to create log file")
except Exception as e:
    print(f"Error setting up logging: {str(e)}")
    raise

def get_memory_usage():
    """Get current memory usage of the process."""
    process = psutil.Process(os.getpid())
    mem_usage = process.memory_info().rss / 1024 / 1024  # Convert to MB
    print(f"Current memory usage: {mem_usage:.2f} MB")  # Immediate feedback
    return mem_usage

async def test_discussions():
    try:
        print("Setting up test environment...")  # Immediate feedback
        initial_memory = get_memory_usage()
        log.info(f"Initial memory usage before setup: {initial_memory:.2f} MB")
        
        # Set mock API key for testing
        os.environ["OPENAI_API_KEY"] = "mock-key-for-testing"
        print("Set mock API key")
        
        logging.info("Starting memory usage test with mock API key")
        print("Checking swarms library...")  # Immediate feedback
        logging.info("Checking if swarms library is available...")
        
        try:
            log.info("Starting swarms imports with enhanced logging...")
            pre_import_memory = get_memory_usage()
            log.info(f"Memory before any imports: {pre_import_memory:.2f} MB")
            
            try:
                # Step 1: Import minimal swarms package
                log.info("Step 1: Importing minimal swarms package...")
                import sys
                import importlib
                
                # Clear any existing imports to start fresh
                for mod in list(sys.modules.keys()):
                    if mod.startswith('swarms'):
                        del sys.modules[mod]
                
                # Import mock components
                log.info("Step 1: Importing mock components...")
                from mock_swarms import Agent, GroupChat, MajorityVoting, round_robin
                log.info("Mock components imported successfully")
                mem_after_import = get_memory_usage()
                log.info(f"Memory after mock imports: {mem_after_import:.2f} MB")
                
                # Step 3: Test minimal agent creation
                log.info("Step 3: Testing minimal agent creation...")
                test_agent = Agent(
                    agent_name="test_agent",
                    system_prompt="Test prompt",
                    llm=lambda x: "test response",
                    max_loops=1,
                    verbose=False
                )
                mem_after_agent_creation = get_memory_usage()
                log.info(f"Memory after agent creation: {mem_after_agent_creation:.2f} MB")
                log.info("Basic agent creation successful")
                del test_agent
                
                # Step 4: Import remaining components
                log.info("Step 4: Importing remaining components...")
                from swarms import GroupChat, MajorityVoting
                from swarms.structs.groupchat import round_robin
                
                final_memory = get_memory_usage()
                log.info(f"Final memory usage: {final_memory:.2f} MB")
                log.info(f"Total memory increase: {final_memory - pre_import_memory:.2f} MB")
                
            except ImportError as e:
                log.error(f"Import error: {str(e)}")
                log.error(f"Module search paths: {sys.path}")
                log.error(f"Traceback: {traceback.format_exc()}")
                raise
            except Exception as e:
                log.error(f"Unexpected error: {str(e)}")
                log.error(f"Traceback: {traceback.format_exc()}")
                raise
            
        except ImportError as e:
            log.error(f"Import error: {str(e)}")
            log.error(f"Traceback: {traceback.format_exc()}")
            raise
        except Exception as e:
            log.error(f"Unexpected error during swarms setup: {str(e)}")
            log.error(f"Traceback: {traceback.format_exc()}")
            raise
    except Exception as e:
        logging.error(f"Error during initialization: {str(e)}")
        logging.error(f"Traceback: {traceback.format_exc()}")
        raise
    logging.info("Initializing AgentService...")
    service = AgentService()
    logging.info("AgentService initialized successfully")
    
    topics = [
        'Analysis of Ethereum Layer 2 scaling solutions and their impact on network efficiency',
        'Evaluation of DeFi lending protocols and their risk management strategies',
        'Assessment of NFT marketplace dynamics and future growth potential'
    ]
    
    initial_memory = get_memory_usage()
    log.info(f'Initial memory usage: {initial_memory:.2f} MB')
    log.info('Starting discussion tests...')
    
    for i, topic in enumerate(topics, 1):
        log.info(f'\n=== Test {i}/{len(topics)} ===')
        log.info(f'Topic: {topic}')
        pre_discussion_memory = get_memory_usage()
        log.info(f'Memory before discussion: {pre_discussion_memory:.2f} MB')
        try:
            log.info("Starting discussion phase...")
            messages = await service.discuss_topic(topic)
            post_discussion_memory = get_memory_usage()
            log.info(f'Discussion completed successfully with {len(messages)} messages')
            log.info(f'Memory after discussion: {post_discussion_memory:.2f} MB')
            log.info(f'Memory change during discussion: {post_discussion_memory - pre_discussion_memory:.2f} MB')
            
            log.info("Starting voting phase...")
            pre_voting_memory = get_memory_usage()
            votes = await service.collect_votes(topic)
            post_voting_memory = get_memory_usage()
            log.info(f'Voting completed successfully with {len(votes)} votes')
            log.info(f'Memory after voting: {post_voting_memory:.2f} MB')
            log.info(f'Memory change during voting: {post_voting_memory - pre_voting_memory:.2f} MB')
            
            # Log memory cleanup
            pre_cleanup_memory = get_memory_usage()
            service._cleanup_agents()
            post_cleanup_memory = get_memory_usage()
            log.info(f'Memory after cleanup: {post_cleanup_memory:.2f} MB')
            log.info(f'Memory freed by cleanup: {pre_cleanup_memory - post_cleanup_memory:.2f} MB')
            
        except Exception as e:
            logging.error(f'Error processing topic: {str(e)}')
    
    final_memory = get_memory_usage()
    logging.info('\nAll tests completed')
    logging.info(f'Final memory usage: {final_memory:.2f} MB')
    logging.info(f'Total memory change: {final_memory - initial_memory:.2f} MB')

if __name__ == '__main__':
    try:
        logging.info("Starting test script")
        logging.info(f"Python path: {sys.path}")
        logging.info(f"Current directory: {os.getcwd()}")
        asyncio.run(test_discussions())
    except Exception as e:
        logging.error(f"Error in main: {str(e)}")
        logging.error(f"Traceback: {traceback.format_exc()}")
        raise
