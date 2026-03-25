from google import genai


class GeminiService:
    def __init__(self, api_key: str, model: str):
        self.client = genai.Client(api_key=api_key)
        self.model = model

    def reply(self, message: str) -> str:
        res = self.client.models.generate_content(
            model=self.model, contents=message
        )
        return res.text
