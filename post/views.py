from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Post, Following, Like
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
import json
from notifications.signals import notify

def createPostView(request):
    return render(request, 'post/create_post.html',{'create_post_page':True})



def create_post(request):
    if request.method == 'POST':
        title = request.POST['title']
        body = request.POST['body']
        image = request.FILES.get('i')
        if title == '' and body == '' and image is None:
            messages.warning(request, 'please fill atleast one field.')
            return redirect('index')
        post = Post(title=title,
                    body=body,
                    image=image,
                    author=request.user
                    )
        post.save()
        print('post created ')
        messages.success(request, 'post created successfully.')
        return redirect('index')
    else:
        return redirect('index')


@login_required
def your_post(request):
    # your post
    post = Post.objects.filter(author=request.user).order_by('-id')
    post_count = post.count()
    # follower and following count
    following_obj = Following.objects.get(user=request.user)
    followers_count, followings_count = following_obj.follower.count(), following_obj.followed.count()

    context = {'post': post, 'post_count':post_count,
               'follower_count': followers_count,
               'followings_count': followings_count
               }

    return render(request, 'post/your_post.html', context)


def single_post(request,id):
    post = Post.objects.get(id=id)
    context = {'post': post}
    return render(request, 'post/single_post.html', context)

from post.forms import AddPostForm
def edit_post(request, id):
    post = Post.objects.get(id=id)
    if post.author == request.user:
        if request.method == 'POST':
            title = request.POST['title']
            body = request.POST['body']
            image = request.FILES.get('i')

            post.title = title
            post.body = body
            if image is not None:
                post.image = image

            post.author = request.user
            post.save()
            print('post updated ')
            messages.success(request, 'post edited successfully.')
            return redirect('your_post')
        else:
            context = {'post': post,'form':AddPostForm(request.POST or None,instance=post)}
            return render(request, 'post/edit_post.html', context)
    else:
        return redirect('/page_not_found')

def delete_post(request, id):
    post = Post.objects.get(id=id)
    post.delete()
    messages.success(request, 'post deleted.')
    return redirect('your_post')

#for follow the user
def follow(request, username):
    main_user = request.user
    to_follow = User.objects.get(username=username)

    #check if already following
    following = Following.objects.filter(user=main_user, followed=to_follow)
    is_following = True if following else False

    if is_following:
        Following.unfollow(main_user, to_follow)
        is_following = False
    else:
        Following.follow(main_user, to_follow)
        notify.send(sender=request.user, recipient=to_follow, verb=f'http://localhost:8000/post/followers',description=f'{request.user} started following you')
    is_following = True

    resp = {
        "following": is_following,
    }

    response = json.dumps(resp)
    return HttpResponse(response, content_type="application/json")


def followers(request):
    following_obj = Following.objects.get(user=request.user)
    # print(following_obj)
    followers_count, followings_count = following_obj.follower.count(),following_obj.followed.count()

    followers = following_obj.follower.all()
    followeds = following_obj.followed.all()
    # print(followers, followeds)
    # print(followers_count,followings_count)

    context = {'followers': followers,
               'followings': followeds,
               'follower_count': followers_count,
               'followings_count': followings_count}
    return render(request, 'post/followers.html', context)

def remove_follower(request,username):
    me = Following.objects.get(user=request.user)
    mera_follower = Following.objects.get(user=User.objects.get(username=username),followed=request.user)
    # print(me)
    # print(mera_follower)

    follower_user = me.follower.get(username=username)
    followed_user = mera_follower.followed.get(username=request.user.username)
    # print(follower_user)
    # print(followed_user)

    me.follower.remove(follower_user)
    mera_follower.followed.remove(followed_user)
    # print('removed')
    return redirect('followers')


def followings(request):
    following_obj = Following.objects.get(user=request.user)
    # print(following_obj)
    followers_count, followings_count = following_obj.follower.count(), following_obj.followed.count()

    followers = following_obj.follower.all()
    followeds = following_obj.followed.all()
    # print(followers, followeds)
    # print(followers_count, followings_count)
    # is_following = Following.objects.filter(user=request.user, followed=user_d)

    context = {'followers': followers,
               'followings': followeds,
               'follower_count': followers_count,
               'followings_count': followings_count}
    return render(request, 'post/followings.html', context)


def other_user_post(request,username):
    # your post
    post = Post.objects.filter(author=User.objects.get(username=username)).order_by('-id')
    post_count = post.count()
    # follower and following count
    following_obj = Following.objects.get(user=User.objects.get(username=username))
    followers_count, followings_count = following_obj.follower.count(), following_obj.followed.count()

    context = {'user_d':User.objects.get(username=username),
               'post':post,'post_count':post_count,
               'follower_count': followers_count,
               'followings_count': followings_count
               }

    return render(request,'post/other_user_post.html',context)


def other_user_followings(request,username):

    following_obj = Following.objects.get(user=User.objects.get(username=username))
    # print(following_obj)
    followers_count, followings_count = following_obj.follower.count(), following_obj.followed.count()

    # followers = following_obj.follower.all()
    followeds = following_obj.followed.all()

    context = {'user_d':User.objects.get(username=username),
               'followings': followeds,
               'follower_count': followers_count,
               'followings_count': followings_count}
    return render(request, 'post/other_user_followings.html', context)


def other_user_followers(request,username):

    following_obj = Following.objects.get(user=User.objects.get(username=username))
    # print(following_obj)
    followers_count, followings_count = following_obj.follower.count(), following_obj.followed.count()

    followers = following_obj.follower.all()
    # followeds = following_obj.followed.all()

    context = {'user_d':User.objects.get(username=username),
               'followers': followers,
               'follower_count': followers_count,
               'followings_count': followings_count,
               }
    return render(request, 'post/other_user_followers.html', context)



# for like the post
def post_like(request):
    post_id = request.POST.get('post_id')
    post = get_object_or_404(Post, id=post_id)

    if post.liked.filter(id=request.user.id).exists():
        post.liked.remove(request.user)
        is_liked = False
    else:
        post.liked.add(request.user)#href="http://localhost:8000/post/single_post/{post.id}"
        if str(request.user.username) != str(post.author):
            print('sss')
            notify.send(sender=request.user, recipient=post.author, verb=f'http://localhost:8000/post/single_post/{post.id}',description=f'{request.user} liked your post')
        is_liked = True

    like, created = Like.objects.get_or_create(user=request.user, post_id=post_id)
    # print(created)
    if not created:
        if like.value == 'Like':
            like.value = 'Unlike'
        else:
            like.value = 'Like'
    like.save()

    data = {
        'value': like.value,
        'likes': post.liked.all().count()
    }

    return JsonResponse(data, safe=False)

# for user's all liked post
def liked_post(request):
    liked_post = Post.objects.filter(liked=request.user).order_by('-id')
    liked_post_count = liked_post.count()
    context = {'post':liked_post,
               'post_count':liked_post_count,
               'like_page':True
               }
    return render(request,'post/liked_post.html',context)



@ login_required
def saved_post(request):
    id = request.POST.get('post_id')
    post = get_object_or_404(Post, id=id)
    if post.saved_post.filter(id=request.user.id).exists():
        post.saved_post.remove(request.user)
        is_saved = 'false'
    else:
        post.saved_post.add(request.user)
        is_saved = 'true'

    data = {'is_saved': is_saved}
    return JsonResponse(data, safe=False)

    # used for refresh current page
    # return HttpResponseRedirect(request.META['HTTP_REFERER'])


def all_saved_post(request):
    saved_postt = Post.objects.filter(saved_post=request.user).order_by('-id')
    saved_post_count = saved_postt.count()

    context = {'saved_postt': saved_postt,
               'saved_post_count': saved_post_count,
               'saved_post_page':True
              }
    return render(request, 'post/all_saved_post.html', context)