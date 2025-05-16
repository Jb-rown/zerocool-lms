from django.shortcuts import render

import openai
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from courses.models import Course

@csrf_exempt
def ai_tutor(request):
    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        question = request.POST.get('question')
        
        try:
            course = Course.objects.get(id=course_id)
            context = f"Course: {course.title}\nDescription: {course.description}\n"
            
            openai.api_key = settings.OPENAI_KEY
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a knowledgeable teaching assistant for a Harvard-level course. Provide detailed, academic responses."},
                    {"role": "user", "content": context + question}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            return JsonResponse({
                'response': response.choices[0].message.content,
                'sources': [
                    {'title': course.title, 'type': 'course'}
                ]
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)