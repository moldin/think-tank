from google.adk.sessions import InMemorySessionService, Session, DatabaseSessionService
from google.adk.runners import Runner
from google.genai import types
from email_writer.agent import email_writer_agent
import uuid
from pprint import pprint
session_service_stateful = InMemorySessionService()
initial_state = {
    "user_name": "Mats Oldin",
    "user_email": "mats@oldin.se",
    "todays_date": "2025-05-14",
    "user_preferences": """I like to program in Python and develop AI agents.""",

}
APP_NAME = "email_writer"
USER_ID = "matsoldin"
SESSION_ID = str(uuid.uuid4())

stateful_session: Session = session_service_stateful.create_session(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id=SESSION_ID,
    state=initial_state,
)

runner = Runner(
    agent=email_writer_agent,
    app_name=APP_NAME,
    session_service=session_service_stateful,
)

new_message = types.Content(
    role="user",
    parts=[types.Part(text="Write a mail to jessica@oldin.se about the project we are working on.")]
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
        pprint(event)
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
