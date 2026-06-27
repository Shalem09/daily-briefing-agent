from dotenv import load_dotenv

load_dotenv()

from agents.orchestrator import run

if __name__ == "__main__":
    run()
