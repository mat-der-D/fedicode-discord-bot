from google import genai
from google.genai import types


class GeminiService:
    def __init__(self, api_key: str, model: str):
        self.client = genai.Client(api_key=api_key)
        self.model = model

    def reply(
        self,
        message: str,
        images: list[tuple[bytes, str]] | None = None,
    ) -> str:
        contents: list = []
        if message:
            contents.append(types.Part.from_text(text=message))
        if images:
            for data, mime_type in images:
                contents.append(types.Part.from_bytes(data=data, mime_type=mime_type))
        res = self.client.models.generate_content(
            model=self.model, contents=contents
        )
        return res.text
