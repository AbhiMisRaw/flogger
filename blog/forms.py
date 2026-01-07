from django import forms 
from .models import Blog

class BlogForm(forms.Form):
    title = forms.CharField(
        label="", 
        widget=forms.TextInput(
            attrs={
                "class": (
                    "w-full bg-transparent text-4xl font-bold "
                    "placeholder:text-indigo-300 "
                    "focus:outline-none"
                ),
                "placeholder": "Your Title"
            }
        )
    )

    content = forms.CharField(
        label="",
        widget=forms.Textarea(
            attrs={
                "class": (
                    "w-full bg-transparent resize-none "
                    "text-lg leading-relaxed "
                    "placeholder:text-indigo-300 "
                    "focus:outline-none mt-6"
                ),
                "placeholder": "Tell your story...",
                "rows": 14
            }
        )
    )


    class Meta:
        model = Blog

class TagsForm(forms.Form):
    tags = forms.CharField(
        label="", 
        widget=forms.TextInput(
            attrs={
                "class": (
                    "w-full bg-transparent border text-md font-bold "
                    "placeholder:text-slate-400 "
                    "focus:outline-none"
                )
            }
        ),
    )