from django import forms 
from .models import Blog

class BlogForm(forms.Form):
    title = forms.CharField(
        label="", 
        widget=forms.TextInput(
            attrs={
                "class": (
                    "w-full bg-transparent text-4xl font-bold "
                    "text-slate-700 placeholder:text-slate-400 "
                    "focus:outline-none"
                ),
                "placeholder": "your title"
            }
        )
    )

    content = forms.CharField(
        label="",
        widget=forms.Textarea(
            attrs={
                "class": (
                    "w-full bg-transparent resize-none "
                    "text-lg text-slate-800 leading-relaxed "
                    "placeholder:text-slate-400 "
                    "focus:outline-none mt-6"
                ),
                "placeholder": "Tell your story...",
                "rows": 14
            }
        )
    )


    class Meta:
        model = Blog