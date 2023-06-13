from typing import Any, Dict
from django.db.models.query import QuerySet
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Post,Author
from django.views.decorators.csrf import csrf_protect
from .forms import CommentForm
#from .models import Review
from django.views import View
from django.views.generic import ListView,DetailView
from django.views import View
# Create your views here.


class StartingPageView(ListView):
    template_name = "blog/starting-page.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "posts"
    
    def get_queryset(self):
        queryset = super().get_queryset()
        data = queryset[:4]
        return data




# def starting_page(request):
#     posts = post.objects.all().order_by('-date')[:4]
#     #sorted_posts = sorted(posts,key=get_date)
#     #latest_posts = sorted_posts[-4:]
#     return render(request,'blog/starting-page.html',{'posts':posts})

class AllPostsView(ListView):
    template_name = "blog/all-posts.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "posts"



# def posts(request):
#     posts = post.objects.all().order_by('-date')
#     return render(request,'blog/all-posts.html',{
#         'posts':posts
#     })


# class ReviewView(View):
#     def get(self,request):
#         form = ReviewForm()
#         identified_post = get_object_or_404(post)
#         return render(request,'blog/post-detail.html',{
#                                 'post':identified_post,
#                                 "post_tags":identified_post.tags.all(),
#                                 'form':form
#                                 })        


    # def post(self,request,slug):
    #     form = ReviewForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return HttpResponseRedirect('/thank-you') 
        
    #     identified_post = get_object_or_404(post,slug)
    #     return render(request,'blog/post-detail.html',{
    #                 'post':identified_post,
    #                 "post_tags":identified_post.tags.all(),
    #                 'form':form
    #                     })

class SinglePostView(View):
    template_name = "blog/post-detail.html"
    model = Post

    def is_stored_post(self,request, post_id):
        stored_posts = request.session.get("stored_posts")
        if stored_posts is not None:
            is_saved_for_later = post_id in stored_posts
        else:
            is_saved_for_later = False
        return is_saved_for_later

    def get(self,request,slug):
        Comment_Form = CommentForm()
        post = Post.objects.get(slug=slug)
        
        context ={
            "post":post,
            "post_tags":post.tags.all(),
            "Comment_Form":CommentForm(),
            "comments":post.comments.all().order_by("-id"),
            "saved_for_later":self.is_stored_post(request,post.id),
        }
        return render(request, "blog/post-detail.html",context)

    def post(self,request,slug):
        Comment_Form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)

        if Comment_Form.is_valid():
            comment = Comment_Form.save(commit=False)
            comment.post = post
            comment.save()
            #return render(request,'blog/post-detail.html')
            return HttpResponseRedirect(reverse("single-post-page",args=[slug]))
        context ={
            "post":post,
            "post_tags":post.tags.all(),
            "Comment_Form":CommentForm(),
            "comments":post.comments.all().order_by("-id"),
            "saved_for_later":self.is_stored_post(request,post.id),
        }
        return render(request,"blog/post-detail.html",context)
    # def get_context_data(self, **kwargs):
    #     context =  super().get_context_data(**kwargs)
    #     context['post_tags'] = self.object.tags.all()
    #     context["CommentForm"] = CommentForm()
    #     return context

    

# @csrf_protect
# def single_post(request,slug):
#     if request.method =="POST":
#         form = ReviewForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect('/thank-you')
#     else:
#         form = ReviewForm()
#     identified_post = get_object_or_404(post, slug=slug)
#     return render(request,'blog/post-detail.html',{
#          'post':identified_post,
#          "post_tags":identified_post.tags.all(),
#         'form':form
#     })

def thank_you(request):
    return render(request,'blog/thankyou.html')


class ReadLater(View):
    def get(self,request):
        stored_posts = request.session.get("stored_posts")
        context = {}
        if stored_posts is None or len(stored_posts) == 0:
            context["posts"] = []
            context["has_posts"] = False
        else:
            posts = Post.objects.filter(id__in = stored_posts)    
            context['posts'] = posts
            context["has_posts"] = True

        return render(request,'blog/stored-posts.html',context)
    

    def post(self,request):
        stored_posts = request.session.get("stored_posts")

        if stored_posts is None:
            stored_posts = []

        post_id = int(request.POST["post_id"])

        if post_id not in stored_posts:
            stored_posts.append(post_id)
            request.session["stored_posts"] = stored_posts
        else:
            stored_posts.remove(post_id)
        request.session["stored_posts"] = stored_posts
        return HttpResponseRedirect("/")