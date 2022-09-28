from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
# Create your models here.

class UserProfile(models.Model):
    profile_pic = models.ImageField(upload_to = "FacebookApp/Profile/profile_picture", default="FacebookApp/Profile/profile_picture/defaultprofilepic.png")
    user = models.OneToOneField(User, on_delete= models.CASCADE)
    bio = models.CharField(max_length=200, default='', blank=True)
    dob = models.DateField(null = True, blank=True)

    def __str__(self):
        return self.user.username

class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    post_content = models.TextField(null=True)
    post_img = models.ImageField(upload_to="FacebookApp/Post/images", default=None)
    post_user = models.ForeignKey(User, on_delete= models.CASCADE)
    post_time = models.DateTimeField(default=now)
    profile_pic = models.ForeignKey(UserProfile, on_delete= models.CASCADE)
    no_of_likes = models.IntegerField(default=0)
    no_of_comments = models.IntegerField(default=0)
    no_of_shares = models.IntegerField(default=0)
    
    def __str__(self):
        return self.post_user.first_name +" says :-  "+ self.post_content[0:30]

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    liked_by = models.ForeignKey(User, on_delete= models.CASCADE)

    def __str__(self):
        return self.post.post_content[0:30] + " ....  -: liked by ... "+ self.liked_by.username

class FollowerCount(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    follower = models.CharField(max_length=100)

    def __str__(self):
        return self.follower+" -> follows -> "+ self.user.username