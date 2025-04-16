from swarm.repl import run_demo_loop
from kiss_agents import triage_agent

from dotenv import load_dotenv

load_dotenv('../config/.keys')

if __name__ == "__main__":
    run_demo_loop(triage_agent)