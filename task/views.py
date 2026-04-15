import asyncio
import logging
from urllib.parse import quote
from django.shortcuts import render, redirect
from asgiref.sync import sync_to_async
from django.urls import reverse

from django.views import View
from django.http import HttpResponse

from blog.models import Blog
from .models import BlogConversionTask
from .service import ConversionService


# Get an instance of a logger
logger = logging.getLogger(__name__)

class BlogConversionView(View):
    service = ConversionService()

    async def get(self, request, task_id):
        # Wrap sync call for Django 6
        task = await sync_to_async(BlogConversionTask.objects.select_related('blog').get)(id=task_id)
        
        if task.status == "completed":
            return render(request, "blogs/partial/ai_result.html", {"task": task})
        
        elif task.status == "failed":
            return render(request, "blogs/partial/ai_error.html", {"task_id": str(task.id), "error_log":str(task.error_log)})
        
        # If still 'pending' or 'processing', return the polling partial
        # HTMX will see this and hit the GET endpoint again in 2 seconds
        return render(request, "blogs/partial/ai_polling.html", {"task_id": str(task.id)})

    async def post(self, request):
        """
            AI-Conversion Blog.
        """
        is_authenticated = await sync_to_async(lambda: request.user.is_authenticated)()
        if not is_authenticated:
            login_url = reverse('user_profile:login')
            next_path = quote(request.path)
            
            if request.htmx:
                response = HttpResponse(status=204)
                response['HX-Redirect'] = f"{login_url}?next={next_path}"
                return response
            
            return redirect(f"{login_url}?next={next_path}")

        # Now proceed with your logic...
        prompt = request.POST.get("prompt")
        blog_id = request.POST.get("blog_id")
        
        blog = await sync_to_async(Blog.objects.get)(id=blog_id)

        task = await sync_to_async(BlogConversionTask.objects.create)(
            user=request.user if request.user.is_authenticated else None,
            blog=blog,
            prompt=prompt,
            status="processing"
        )

        asyncio.create_task(self._run_conversion_logic(task.id, blog.title, blog.content, prompt))
        return render(request, "blogs/partial/ai_polling.html", {"task_id": str(task.id)})
    

    async def _run_conversion_logic(self, task_id, title, content, prompt):
        try:
            # 1. Get the AI Story
            result = await self.service.transform_blog_to_story(title, content, prompt)
            
            await sync_to_async(self._save_success, thread_sensitive=False)(task_id, result["story"])
            logging.info(f"✅ Task {task_id} completed successfully.")

        except Exception as e:
            logging.error(f"❌ Background Task Failed: {e}")
            await sync_to_async(self._save_failure, thread_sensitive=False)(task_id, e.message)


    # Helpers to keep the async logic clean
    def _save_success(self, task_id, story):
        BlogConversionTask.objects.filter(id=task_id).update(result=story, status="completed")

    def _save_failure(self, task_id, error):
        BlogConversionTask.objects.filter(id=task_id).update(status="failed", error_log=error)