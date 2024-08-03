import voyageai
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('VOYAGE_API_KEY')
vo = voyageai.AsyncClient(api_key=API_KEY)


class EmbeddingsService:
    def __init__(self):
        self.client = vo

    async def embed(self, content: str):
        response = await self.client.embed(
            [content], model="voyage-code-2", input_type="document"
        )

        if not response.embeddings:
            raise ValueError("No embeddings returned for the provided content")

        return response.embeddings[0]

