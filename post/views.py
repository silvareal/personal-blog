from django.contrib import messages
from django.shortcuts import render, get_object_or_404, Http404,redirect, HttpResponseRedirect
from django.views.generic import ListView
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from . models import Post
from . forms import PostForm, PostEmail

# Create your views here.
'''def lists(request):
    post_list = Post.publishs.all()
    if request.user.is_superuser or request.user.is_staff:
        post_list = Post.objects.all()
    
    post_var = "post"
    paginator = Paginator(post_list, 2)
    page = request.GET.get(post_var)
    try:
        posts = paginator.page(page)    
    except PageNotAnInteger:
        # If page is not an integer deliver the first page        
        posts = paginator.page(1)    
    except EmptyPage:
        # If page is out of range deliver last page of results        
        posts = paginator.page(paginator.num_pages)
    context    = {
        'Posts':posts,
        'post_var':post_var
    }
    return render(request, 'post/list.html', context)'''

class PostList(ListView):
    model = Post
    paginate_by = 5
    context_object_name = 'posts'
    def get_queryset(self):
        post_list = Post.publishs.all()
        if self.request.user.is_superuser or self.request.user.is_staff:
            post_list = Post.objects.all()
        return post_list
    template_name = 'post/list.html'


def detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug = post,
                                    publish__year=year,
                                    publish__month = month,
                                    publish__day = day)
    print(post)
    context = {
        'post':post,
        'title': post.slug
    }
    return render(request, 'post/detail.html', context)

def post_create(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.user = request.user
        post.save()
        messages.success(request, "post succesfully created")
        return HttpResponseRedirect(post.get_absolute_url())
    context = {
        'form':form
    }
    return render(request, 'post/post_form.html', context)

def delete(request, year, month, day, post):
    post = get_object_or_404(Post, slug = post,
                                    publish__year=year,
                                    publish__month = month,
                                    publish__day = day)
    post.delete()
    messages.success(request, 'successfully deleted')
    return redirect('post:lists')

def post_update(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                                    publish__year = year,
                                    publish__month = month,
                                    publish__day = day)
    form = PostForm(request.POST or None,request.FILES or None, instance=post)
    if form.is_valid():
        post = form.save(commit=False)
        post.user = request.user
        post.save()
        messages.success(request, "successfully updated")
        return HttpResponseRedirect(post.get_absolute_url())
    context = {
        'title':post.title,
        "post":post,
        "form":form
    }
    return render(request, 'post/post_form.html', context)

def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == Post:
        form = PostEmail(request.Post)
        if form.is_valid():
            cd = form.cleaned_data
            post_uri = request.build_absolute_uri(post.get.
                get_absolute_url())
            subject = "{} ({}) recommends you reading {}".format(cd['name'], cd['email'],post.title)
            message = "Read {} at {}/n/n{}\'s comments:{}".format(
                post.title, post_uri,cd['name'],cd['comment']
            )
            send_mail(subject, message, akubosylvernus@gmail.com, [cd['to']])
            sent = True
    else:
        form = PostEmail()
    context = {
        'post':post,
        'form':form,
        'sent':sent,    }
    return render(request, 'post/form.html', context)

def resume_form(request):
    sent = False
    if request.method == Post:
        form = ResumeMail(request.Post)
        if form.is_valid():
            cd = form.cleaned_data
            subject = "{} say\'s /n {}".format(cd['name'], cd['subject'])
            send_mail(subject, cd['message'], cd['email'], [akubosylvernus@gmail.com])
            sent = True
    else:
        form = ResumeMail()
    context = {
        'form':form,
        'sent':sent,
    }
    return render(request, 'resume/form.html', context)

    
