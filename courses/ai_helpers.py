import openai
from django.conf import settings

def generate_quiz_from_lesson(lesson_content):
    """Use AI to generate quiz questions from lesson content"""
    openai.api_key = settings.OPENAI_KEY
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Generate 3 quiz questions based on this lesson content:\n\n{lesson_content}",
        max_tokens=150
    )
    return response.choices[0].text.strip()