from google.adk.sessions import InMemorySessionService, Session, DatabaseSessionService
from google.adk.runners import Runner
from google.genai import types
from think_tank.agent import problem_solver_agent
import uuid
from pprint import pprint

initial_state = {
    "user_name": "Mats Oldin",
    "user_email": "mats@oldin.se",
    "todays_date": "2025-05-14",
    "user_language": "Swedish",
    "user_preferences": """I am an experienced python devloper and PHD in mathematics.""",

}
APP_NAME = "think_tank"
USER_ID = "matsoldin"
SESSION_ID = str(uuid.uuid4())
db_url = "sqlite:///./agent_data.db"
#session_service_stateful = InMemorySessionService()
session_service_stateful = DatabaseSessionService(db_url=db_url)
stateful_session: Session = session_service_stateful.create_session(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id=SESSION_ID,
    state=initial_state,
)

runner = Runner(
    agent=problem_solver_agent,
    app_name=APP_NAME,
    session_service=session_service_stateful,
)

question = """
I want to make a workshop to facilitate the use of AI agents in our company. And help
people understand how to transition from microservices to AI agents.

What are the key topics I should cover? How should I structure the workshop?
"""

new_message = types.Content(
    role="user",
    parts=[types.Part(text=question)]
)

for event in runner.run(
    user_id=USER_ID,
    session_id=SESSION_ID,
    new_message=new_message,
):
    
    if event.is_final_response():
        print(f"---- Final Response ----")
        pprint(event.content.parts[0].text)
        print(f"---- End of Final Response ----")
        # if event.content and event.content.parts:
        #     print(f"Final response: {event.content.parts[0].text}")
        # # pretty print the event
        #     pprint(f"Final response: {event}")
    else:
        print(f"---- Event ----")
        print(event)
        print(f"---- End of Event ----")
    
# print(f"--- Examining Session Properties ---")
# print(f"Session ID: {SESSION_ID}")
# print(f"App Name: {APP_NAME}")
# print(f"User ID: {USER_ID}")
# print(f"Events: {stateful_session.events}")
# print(f"State: {stateful_session.state}")
# print(f"My email: {stateful_session.state['user_email']}")
# print(f"Last update: {stateful_session.last_update_time:.2f}")

# print(f"--- End of Session Properties ---")
