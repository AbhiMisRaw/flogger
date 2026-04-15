from django.conf import settings
import random

from google import genai


class ConversionService:
    def __init__(self):
        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY,
            http_options={'api_version': 'v1alpha'}
        )

    async def transform_blog_to_story(self, title, blog_content, requested_prompt):
        models = settings.GEMINI_AI_MODELS
        response = await self.client.aio.models.generate_content(
            model= random.choice(models),
            contents=f"{requested_prompt}\nTitle:{title},\nContent: {blog_content}"
        )
        return {"story": response.text}

