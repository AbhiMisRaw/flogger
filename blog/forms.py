from django import forms 
from .models import Blog

class BlogForm(forms.ModelForm):
    title = forms.CharField(
        label="", 
        widget=forms.TextInput(
            attrs={
                "class": (
                    "w-full text-2xl font-bold px-3 py-2 text-slate-900 "
                    "placeholder-slate-300 outline-none rounded-lg bg-transparent"
                ),
                "placeholder": "Post Title..."
            }
        )
    )

    content = forms.CharField(
        label="",
        widget=forms.Textarea(
            attrs={
                "class": (
                    "w-full h-[65vh] p-4 text-slate-700 font-mono text-sm "
                    "leading-relaxed outline-none resize-y placeholder-slate-300 "
                    "bg-transparent"
                ),
                "placeholder": "Write your technical deep dive here...",
            }
        )
    )

    class Meta:
        model = Blog
        fields = ['title', 'content'] # Always explicitly define your fields

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