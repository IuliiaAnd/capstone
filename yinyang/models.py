from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
   badges = models.IntegerField(default=0)
   image = models.ImageField(upload_to="media", default="fallback.png", blank=True)

   def __str__(self):
        return self.username

class Thought(models.Model):

    TAG = (('WORK', 'Work'),
           ('PERSONAL', 'Personal'),
           ('RELATIONSHIP', 'Relationship'),
           ('STUDIES', 'Studies'),
           ('MONEY', 'Money'),
           ('FAMILY', 'Family'),
           ('HEALTH', 'Health'))
    
    TYPE = (('NEGATIVE', 'Negative'),
            ('POSITIVE', 'Positive'))

    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name="user")
    entry = models.CharField(max_length=250, blank=False, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    tag = models.CharField(max_length=50, choices=TAG, default="PERSONAL") 
    thought_type = models.CharField(max_length=50, choices=TYPE, default="NEGATIVE")
    edited = models.BooleanField(default=False)

    def serialize(self):
        return {
            "id": self.id,
            "author": self.author.username,            
            "entry": self.entry,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "tag": self.tag,
            "thought_type": self.thought_type
        }

class Goal(models.Model):

    CATEGORY = (('WORK', 'Work'),
                ('PERSONAL', 'Personal'),
                ('RELATIONSHIP', 'Relationship'),
                ('STUDIES', 'Studies'),
                ('MONEY', 'Money'),
                ('FAMILY', 'Family'),
                ('HEALTH', 'Health'))
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name="goal")
    description = models.CharField(max_length=250, blank=False, null=False)
    category = models.CharField(max_length=50, choices=CATEGORY, default="PERSONAL") 
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s Goal: {self.description}"
    
class Rewards(models.Model):

    REWARD_TYPE = (('BADGE', 'Badge'),
    )

    receiver = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name="reward_receiver")
    timestamp = models.DateTimeField(auto_now_add=True)
    reward_type = models.CharField(max_length=50, choices=REWARD_TYPE, default=None)
    description = models.CharField(max_length=250, default=None, null=False)

    def __str__(self):
        return f"{self.receiver} got a {self.reward_type}"