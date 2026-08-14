import time
from langchain.agents.middleware import AgentMiddleware

class LoggingMiddleware(AgentMiddleware):

    def before_agent(self, state, runtime):
        print("\n" + "=" * 60)
        print("AGENT STARTED")
        print("=" * 60)

        print("Messages:", state.get("messages", []))

        return None

    def after_agent(self, state, runtime):
        print("\n" + "=" * 60)
        print("AGENT FINISHED")
        print("=" * 60)

        return None