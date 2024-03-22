import os
import time
import json

from openai import OpenAI

from config.main import settings
from utils.singleton import Singleton
from constants.prompts import SYS_PROMPT_CHATGPT
from constants.paths import WEBSITE_DATA
from .functions import SEND_USER_QUERY_AS_EMAIL
from .email import EmailSender

os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY

class OpenAIGpt(metaclass=Singleton):
    """
    Class to handle all the chat related operations.
    """

    def __init__(self) -> None:
        self.client = OpenAI()
        self.email_sender = EmailSender()
        self.user_to_thread_map = {}
        self.assistant = self.setup_assistant()

    def upload_file(self, file_path):
        response = self.client.files.create(
            file=open(file_path, "rb"), purpose="assistants"
        )
        return response

    async def generate(self, user_email, content):
        return await self.generate_assistant(user_email, content)

    async def generate_assistant(self, user_email, content):
        thread, created = self.create_thread(user_email)
        if created:
            content = f"Hey My email is {user_email} and I am interested in your services." + content
        response = self.client.beta.threads.messages.create(
            thread.id,
            role="user",
            content=content,
        )
        messages = await self.run_assistant(thread.id)
        message_dict = json.loads(messages.model_dump_json())
        response = message_dict["data"][0]["content"][0]["text"]["value"]
        return response

    def setup_assistant(self):
        assistant = None
        if settings.ASSISTANT_ID:
            try:
                assistant = self.client.beta.assistants.retrieve(settings.ASSISTANT_ID)
                assistant = self.client.beta.assistants.update(
                    assistant.id,
                    instructions=SYS_PROMPT_CHATGPT,
                    tools=[
                        {"type": "retrieval"},
                        {"type": "code_interpreter"},
                        SEND_USER_QUERY_AS_EMAIL,
                    ],
                )
            except Exception as e:
                print(e)
                input_file = self.upload_file(WEBSITE_DATA)
                assistant = self.client.beta.assistants.create(
                    name="Share Assistant",
                    instructions=SYS_PROMPT_CHATGPT,
                    tools=[
                        {"type": "retrieval"},
                        {"type": "code_interpreter"},
                        SEND_USER_QUERY_AS_EMAIL,
                    ],
                    model=settings.LLM_MODEL,
                    file_ids=[input_file.id],
                )
        else:
            input_file = self.upload_file(WEBSITE_DATA)
            assistant = self.client.beta.assistants.create(
                name="Share Assistant",
                instructions=SYS_PROMPT_CHATGPT,
                model=settings.LLM_MODEL,
                tools=[
                    {"type": "retrieval"},
                    {"type": "code_interpreter"},
                    SEND_USER_QUERY_AS_EMAIL,
                ],
                file_ids=[input_file.id],
            )
        return assistant

    def create_thread(self, user_email):
        """
        This function creates a new thread
        """
        thread = None
        created = False
        if user_email in self.user_to_thread_map:
            thread = self.client.beta.threads.retrieve(self.user_to_thread_map[user_email])
            created = False
        else:
            thread = self.client.beta.threads.create(metadata={"user_email": user_email})
            self.user_to_thread_map[user_email] = thread.id
            created = True
        return thread, created

    async def run_assistant(self, thread_id):
        # Create a new run for the given thread and assistant
        run = self.client.beta.threads.runs.create(
            thread_id=thread_id, assistant_id=self.assistant.id
        )

        while run.status == "in_progress" or run.status == "queued":
            time.sleep(3)
            run = self.client.beta.threads.runs.retrieve(
                thread_id=thread_id, run_id=run.id
            )

            if run.status == "completed":
                return self.client.beta.threads.messages.list(thread_id=thread_id)
            if run.status == "requires_action":
                tool_call = run.required_action.submit_tool_outputs.tool_calls[0]
                tool_outputs = []
                if tool_call.function.name == "send_user_query_as_email":
                    user_email = json.loads(tool_call.function.arguments).get("user_email")
                    user_name = json.loads(tool_call.function.arguments).get("user_name", "")
                    user_query = json.loads(tool_call.function.arguments).get("user_query", "")
                    user_interest = json.loads(tool_call.function.arguments).get("user_interest", "")
                    result = await self.email_sender.send_user_query_as_email({
                        "user_name": user_name,
                        "user_email": user_email,
                        "user_query": user_query,
                        "user_interest": user_interest,
                    })
                    tool_outputs.append(
                        {
                            "tool_call_id": tool_call.id,
                            "output": str(result),
                        },
                    )
                if tool_outputs:
                    run = self.client.beta.threads.runs.submit_tool_outputs(
                        thread_id=thread_id, run_id=run.id, tool_outputs=tool_outputs
                    )

        return run
