from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from FacebookApp.models import Like, Post, UserProfile, FollowerCount


# Create your views here.
def index(request):
    if str(request.user) == "AnonymousUser":
        print("anonymousUser")
        return render(request, 'index.html')
    post = Post.objects.all()
    params = {"posts":post}
    return render(request, 'newsfeed.html', params)


def loginController(request):
    #if request method is post then only the user will be logged in to the site i.e user can't login by writing url in browser need to pass a post method form
    if request.method == 'POST':
        username = request.POST['loginUsername']
        password = request.POST['loginPassword']

        #authenticate take two arguments username and password to verify if the user with thes credentials exist and username is unique
        user = authenticate(username = username, password = password)
        print(user)
        #above line of code will give the authenticated user if no user is found it will give None
        check=''
        #login process starts here
        if user is not None:
            if(user.username == 'admin'):
                print("yes user is admin\nyou can not login through normal login panel")
                check='checked'
                messages.error(request, "invalid login credentials")
                params={"checked": check, "invalid_login": "invalid login credentials"}
                return render(request, 'index.html', params)
                
            #login takes two arguments request and authenticated user and it will start the session for the user
            login(request, user)
            messages.success(request, "successfully logged in ")
            return redirect('/')
        check='checked'
        params={"checked": check, "invalid_login": "invalid login credentials"}
        return render(request, 'index.html', params)
    return HttpResponse("error - 404 page not found")

def signupController(request):
    #if request method is post then only the user will sign up to the site i.e user can't signup by writing url in browser need to pass a post method form
    if request.method == 'POST':
        #get the post parameters from the html form
        username = request.POST['username']
        fname = request.POST['fName']
        lname = request.POST['l_Name']
        email = request.POST['email']
        password = request.POST['password']
        cnfpassword = request.POST['cnfpassword']
        #<--handle the errorneous input results
        
        #-------->
        #save user information to database
        user = User.objects.create_user(username, email, password)
        user.first_name = fname
        user.last_name = lname
        user.save()

        #create the user profile
        profile = UserProfile()
        profile.user = user
        profile.save()
        messages.success(request,"your account has been successfully created")
        
        return redirect('/')
    return HttpResponse("error - 404 page not found")


def logoutController(request):
    #if request method is post then only the user will be logged out of the site i.e user can't logout by writing url in browser need to pass a post method form

    if request.method =="POST":
        logout(request)
        messages.success(request, "you are successfully logged out")
        return redirect('/')
    #if request method is not post user will get page not found message
    return HttpResponse('error - 404 : page not found')


def profileController(request):
    return render(request, "profile.html")

def viewProfile(request):
    fn = request.user.first_name
    ln = request.user.last_name
    em = request.user.email
    params = {"firstname":fn, "lastname":ln, "email":em}
    if request.method == 'POST':
        
        fname = request.POST.get('firstName')
        lname = request.POST.get('lastName')
        email = request.POST.get('changeEmail')

        

        # print(fname)
        # print(email)
        if (fname != ""):
            print(fname +" is fname")
            user = request.user
            print(request.user.username)
            
            request.user.first_name = fname
            request.user.last_name = lname
            request.user.email = email
            
            user.save()
        else:
            print(request.user.first_name)
            print(fname +"fname is empty")
    # print(request.user)
    
    return render(request, "viewprofile.html", params)


def forgotPasswordController(request):
    if request.method == 'POST':
        username = request.POST['forgotusername']
        password = request.POST['forgotpassword']
        cnfpassword = request.POST['forgotcnfpassword']
        try:
            user = User.objects.get(username=username)
            user.set_password(password)
            user.save()
            print(user.first_name +" "+user.password)
            messages.success(request, "user found")
        except:
            messages.error(request, "user not found")
            print("user doesn't exist")
        
        return redirect('/')
        print("a")
    return HttpResponse('error - 404 : page not found')


def createPostController(request):
    
    if request.method == 'POST':
        postcontent = request.POST.get('postcontent')
        post_img = request.FILES.get('postimage')
        print(postcontent)
        userprofile = UserProfile.objects.get(user = request.user)
        post = Post.objects.create(post_content = postcontent, post_img = post_img, post_user = request.user, profile_pic = userprofile)
        print("saving form data")
        post.save()
        print("form data saved")
        print(post.post_content)
        return redirect('/')
        
    return render(request, "friendlist.html")


def userprofileController(request, username):
    try:
        followbtntxt = "Follow"
        user = User.objects.get(username = username)
        if FollowerCount.objects.filter(user = user, follower = request.user.username).first():
            followbtntxt = "Unfollow"
        

        profile = UserProfile.objects.get(user = user)
        post = Post.objects.filter(post_user = user)
        for i in post:
            print(i.post_id)
        followingcount = FollowerCount.objects.filter(follower = username)
        followercount = FollowerCount.objects.filter(user = user)
        params = {"post":post, "profile":profile, "follow":followbtntxt, "follower":followercount, "following":followingcount}
        return render(request, "profile.html", params)
    
    except:
        print("user doesn't exists")
        return HttpResponse("user dosen't exists")
    
def likeController(request):
    if request.method == "POST":
        pst_id = request.POST.get('post_id')
        post = Post.objects.get(post_id = pst_id)
        user = request.user
        #unlike the post
        try:
            liked_by = Like.objects.get(post = post, liked_by=user)
            liked_by.delete()
            print("liked already")
            post.no_of_likes = post.no_of_likes - 1
            post.save()
        #like the post
        except:
            print("not liked earlier")
            liked_by = Like.objects.create(post = post, liked_by = user)
            liked_by.save()
            post.no_of_likes = post.no_of_likes + 1
            post.liked_by = user.username
            post.save()
        return redirect('/#post'+pst_id)
    return redirect('/')


def followUnfollow(request):
    if request.method == 'POST':
        user = request.POST.get('username')
        followed_user = User.objects.get(username = user)
        print(followed_user)
        follower = request.user.username
        if FollowerCount.objects.filter(user = followed_user, follower = follower).first():
            remove_follower = FollowerCount.objects.get(user = followed_user, follower = follower)
            remove_follower.delete()
            return redirect('/profile/'+user)
        else :
            new_follower = FollowerCount.objects.create(user = followed_user, follower = follower)
            new_follower.save()
            return redirect('/profile/'+user)
    return redirect('/')