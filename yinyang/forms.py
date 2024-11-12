from django import forms
from .models import Thought, Goal, User

class CreateThought(forms.ModelForm):
  class Meta:
    model = Thought
    fields = ['entry', 'tag']

class GoalForm(forms.ModelForm):
  class Meta:
      model = Goal
      fields = ["description", "category"]
      widgets = {
        "description": forms.TextInput(attrs={
          "placeholder": "e.g. Take an online course"
        }),
      }

class EditProfilePicForm(forms.ModelForm):
  class Meta:
    model = User
    fields = ['image']
