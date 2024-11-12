from django.contrib import admin
from .models import User, Thought, Goal, Rewards
# Register your models here.
admin.site.register(User)
admin.site.register(Thought)
admin.site.register(Goal)
admin.site.register(Rewards)
