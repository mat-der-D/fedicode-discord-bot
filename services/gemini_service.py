import os

from google import genai


class GeminiService:
    def __init__(self, api_key: str, model: str):
        self.client = genai.Client(api_key=api_key)
        self.model = model

    async def build_prompt(self, channel, history_limit: int = 30):
        lines = []

        async for msg in channel.history(limit=history_limit):
            if not msg.content:
                continue

            name = msg.author.display_name
            text = msg.content.replace("\n", " ")

            lines.append(f"[{name}] {text}")

        lines.reverse()

        header_file = f"{os.path.dirname(__file__)}/gemini-header.txt"
        with open(header_file, "r") as f:
            header = f.read()

        return header + "\n".join(lines) + "\n[Bot]"

    async def chat_from_channel(self, channel, user_message, user_name):
        prompt = await self.build_prompt(channel)

        prompt += f"\n[{user_name}] {user_message}\n[Bot]"

        res = self.client.models.generate_content(model=self.model, contents=prompt)

        return res.text
