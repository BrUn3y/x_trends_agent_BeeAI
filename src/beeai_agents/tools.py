import smtplib
import os
import httpx
import asyncio
from email.mime.text import MIMEText
from collections.abc import AsyncGenerator
from bs4 import BeautifulSoup
from beeai_framework.tools import Tool
from pydantic import BaseModel, Field

# --- Email Tool --- #

class EmailToolInput(BaseModel):
    to_email: str = Field(..., description="The recipient's email address.")
    subject: str = Field(..., description="The subject of the email.")
    body: str = Field(..., description="The body content of the email.")

class EmailTool(Tool):
    name: str = "EmailSender"
    description: str = "Sends an email to a specified recipient."
    input_schema = EmailToolInput

    def _run(self, to_email: str, subject: str, body: str) -> str:
        host = os.getenv("EMAIL_HOST")
        port = int(os.getenv("EMAIL_PORT", 587))
        user = os.getenv("EMAIL_HOST_USER")
        password = os.getenv("EMAIL_HOST_PASSWORD")
        if not all([host, user, password]):
            return "Error: Email environment variables are not set."
        
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = user
        msg['To'] = to_email

        try:
            with smtplib.SMTP(host, port) as server:
                server.starttls()
                server.login(user, password)
                server.sendmail(user, [to_email], msg.as_string())
            return f"Email successfully sent to {to_email}"
        except Exception as e:
            return f"Failed to send email: {e}"

    async def _create_emitter(self, **kwargs) -> AsyncGenerator[str, None]:
        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(None, lambda: self._run(**kwargs))
        yield result