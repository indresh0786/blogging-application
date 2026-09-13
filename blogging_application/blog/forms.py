from django import forms
from django.contrib.auth.models import User
from .models import Post,Comment

class RegisterForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput)
    email=forms.EmailField()
    class Meta:
        model=User
        fields=["username","email","password"]
    def save(self,commit=True):
        user=super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:user.save()
        return user

class PostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=["title","category","excerpt","content","image_url","status"]
        widgets={"excerpt":forms.Textarea(attrs={"rows":3}),"content":forms.Textarea(attrs={"rows":12})}

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=["body"]
        widgets={"body":forms.Textarea(attrs={"rows":4,"placeholder":"Write a comment..."})}
