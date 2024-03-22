from utils.singleton import Singleton
from fastapi import FastAPI
from fastapi_mail import FastMail, MessageSchema
from pydantic import EmailStr
from typing import List
from config.main import settings
from config.email import conf

class EmailSender(metaclass=Singleton):
    def __init__(self) -> None:
        self.app = FastAPI()
        self.mail = FastMail(conf)

    async def send_email(self, to: List[EmailStr], subject: str, content: str):
        message = MessageSchema(
            subject=subject,
            recipients=to,
            body=content,
            subtype="plain"
        )
        await self.mail.send_message(message)
        return "Email has been sent successfully!"

    def generate_email_content(self, data: dict):
        user_email = data.get("user_email")
        user_name = data.get("user_name")
        user_query = data.get("user_query")
        user_interest = data.get("user_interest")
        content = """
        Hello Matt, 
        A user has requested your help. Here are the details:
        User Name: {}
        User Email: {}
        User Query: {}
        User Interest: {}
        """.format(user_name, user_email, user_query, user_interest)
        return content

    async def send_user_query_as_email(self, data: dict):
        subject = "Someone is looking for your help!"
        to = [settings.MATT_EMAIL]
        content = self.generate_email_content(data)
        return await self.send_email(to, subject, content)
    