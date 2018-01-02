from django.contrib import messages
from django.shortcuts import render, get_object_or_404, Http404,redirect, HttpResponseRedirect
from django.views.generic import ListView
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from taggit.models import Tag
from django.contrib.auth.decorators import login_required
from django.db.models import Q


from . models import Post
from .models import Profile
from . forms import PostForm, PostEmail, UserRegistrationForm, UserEditForm, ProfileEditForm

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

def post_list(request, tag_slug=None):
    post_list = Post.publishs.all()
    if request.user.is_staff or request.user.is_superuser:
        post_list = Post.objects.all()
    if tag_slug:
        tag = get_object_or_404(Tag, tag_slug)
        post_list = post_list.filter(Tags__in[tag])
    query = request.GET.get("q")
    if query:
        post_list = post_list.filter(
            Q(title__icontains=query)|
            Q(username__icontains=query)|
            Q(content__icontains=query)).distinct()
    paginator = Paginator(post_list, 3) # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
       # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
       # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request, 'post/list.html', locals())




def registration(request):
    if request.method == 'Post':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # set the given password
            new_user.set_password(
                 user_form.cleaned_data['password'])
            # save the user object
            new_user.save()
            profile = Profile.objects.create(user=new_user)
            return render(request, 'register_done.html', {'new_user': new_user})
    else:
            user_form = UserRegistrationForm()
            return render(request, 'register.html', {'user_form': user_form})
    


@login_required
def edit(request):
    if request.method == 'Post':
        user_form = UserEditForm(instance=request.user,
                                data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                        data=request.POST,
                                        files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success("profile updated successfuly")
        else:
            messages.error("profile update failed")
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    context = {
        'user_form':user_form,
        'profile_form':profile_form,
    }
    return render(request,'registration/edit.html', context)
    
