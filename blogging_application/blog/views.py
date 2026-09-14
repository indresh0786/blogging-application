import json

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404,redirect,render
from django.views.decorators.http import require_POST
from .forms import RegisterForm,PostForm,CommentForm
from .models import Post,Category
import json
import os 
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def home(request):
    return render(request,"blog/home.html",{"posts":Post.objects.filter(status="published")[:6],"categories":Category.objects.all()[:6]})

def register(request):
    if request.user.is_authenticated:return redirect("home")
    form=RegisterForm(request.POST or None)
    if request.method=="POST" and form.is_valid():
        user=form.save();login(request,user);messages.success(request,"Account created.");return redirect("home")
    return render(request,"registration/register.html",{"form":form})

def post_list(request):
    posts=Post.objects.filter(status="published")
    q=request.GET.get("q","").strip()
    category=request.GET.get("category","").strip()
    if q: posts=posts.filter(Q(title__icontains=q)|Q(excerpt__icontains=q)|Q(content__icontains=q)|Q(author__username__icontains=q))
    if category: posts=posts.filter(category__name__iexact=category)
    return render(request,"blog/post_list.html",{"posts":posts,"q":q,"categories":Category.objects.all()})

def post_detail(request,pk):
    post=get_object_or_404(Post,pk=pk,status="published")
    post.views+=1;post.save(update_fields=["views"])
    form=CommentForm()
    if request.method=="POST":
        if not request.user.is_authenticated:return redirect("login")
        form=CommentForm(request.POST)
        if form.is_valid():
            c=form.save(commit=False);c.post=post;c.user=request.user;c.save();messages.success(request,"Comment added.");return redirect("post_detail",pk=pk)
    liked=request.user.is_authenticated and post.likes.filter(pk=request.user.pk).exists()
    return render(request,"blog/post_detail.html",{"post":post,"form":form,"liked":liked})

@login_required
def dashboard(request):
    posts=Post.objects.filter(author=request.user)
    return render(request,"blog/dashboard.html",{"posts":posts,"total":posts.count(),
                                                 "published":posts.filter(status="published").count(),
                                                 "drafts":posts.filter(status="draft").count(),
                                                 "total_views":sum(p.views for p in posts)})

@login_required
def create_post(request):
    form=PostForm(request.POST or None)
    if request.method=="POST" and form.is_valid():
        p=form.save(commit=False);p.author=request.user;p.save();messages.success(request,"Post saved.");return redirect("dashboard")
    return render(request,"blog/post_form.html",{"form":form,"title":"Write a New Story"})

@login_required
def edit_post(request,pk):
    p=get_object_or_404(Post,pk=pk,author=request.user);form=PostForm(request.POST or None,instance=p)
    if request.method=="POST" and form.is_valid():
        form.save();messages.success(request,"Post updated.");return redirect("dashboard")
    return render(request,"blog/post_form.html",{"form":form,"title":"Edit Story"})

@login_required
@require_POST
def delete_post(request,pk):
    get_object_or_404(Post,pk=pk,author=request.user).delete();messages.success(request,"Post deleted.");return redirect("dashboard")

@login_required
@require_POST
@csrf_exempt
def subscribe_push(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)

    try:
        data = json.loads(request.body)

        endpoint = data.get("endpoint")
        keys = data.get("keys", {})

        if not endpoint:
            return JsonResponse({"error": "Invalid subscription"}, status=400)

        from .models import PushSubscription

        PushSubscription.objects.update_or_create(
            endpoint=endpoint,
            defaults={
                "p256dh": keys.get("p256dh", ""),
                "auth": keys.get("auth", ""),
            }
        )

        return JsonResponse({"success": True})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


def vapid_public_key(request):
    return JsonResponse({
        "publicKey": os.environ.get("VAPID_PUBLIC_KEY", "")
    })
def toggle_like(request,pk):
    p=get_object_or_404(Post,pk=pk,status="published")
    if p.likes.filter(pk=request.user.pk).exists():p.likes.remove(request.user)
    else:p.likes.add(request.user)
    return redirect("post_detail",pk=pk)
