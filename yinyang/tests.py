from django.test import Client, TestCase
from .models import User, Thought, Goal, Rewards
from django.urls import reverse
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
import json
# Create your tests here.

class ModelsTestCase(TestCase):
  MILESTONES = {
    1: "First goal is completed! Congratulations!",
    5: "You completed 5 goals! Keep up the good work!",
    10: "You completed 10 goals!",
    20: "You completed 20 goals!",
    40: "You completed 40 goals!",
    60: "You completed 60 goals!",
    100: "You completed 100 goals! Amazing!"
  }

  def setUp(self):
    self.user = User.objects.create(username="user1")
    #create negative thought with tag
    n1 = Thought.objects.create(author=self.user, entry="nt1", tag="PERSONAL", thought_type="NEGATIVE", edited=False)
    n2 = Thought.objects.create(author=self.user, entry="nt2", tag="HEALTH", thought_type="NEGATIVE", edited=True)

    #create positive thought with tag
    p1 = Thought.objects.create(author=self.user, entry="pt1", tag="PERSONAL", thought_type="POSITIVE", edited=False)
    p2 = Thought.objects.create(author=self.user, entry="pt2", tag="WORK", thought_type="POSITIVE", edited=True) 

    self.goal = Goal.objects.create(user=self.user, description="Complete test", is_completed=False) 

  def test_negative_thoughts_count(self):
    negative_thoughts_count = Thought.objects.filter(thought_type="NEGATIVE").count()
    self.assertEqual(negative_thoughts_count, 2)

  def test_positive_thoughts_count(self):
    positive_thoughts_count = Thought.objects.filter(thought_type="POSITIVE").count()
    self.assertEqual(positive_thoughts_count, 2)

  def test_filter_by_tag_and_type(self):
    negative_thought_by_type = Thought.objects.filter(thought_type="NEGATIVE").count()
    positive_thought_by_type = Thought.objects.filter(thought_type="POSITIVE").count()
    self.assertEqual(negative_thought_by_type, 2)
    self.assertNotEqual(negative_thought_by_type, 1)
    self.assertEqual(positive_thought_by_type, 2)
    self.assertNotEqual(positive_thought_by_type, 1)

    thought_by_tag = Thought.objects.filter(tag="PERSONAL").count()
    self.assertEqual(thought_by_tag, 2)
    self.assertNotEqual(thought_by_tag, 1)

  def test_edited_entry(self):
    n1_is_not_edited = Thought.objects.filter(entry="nt1", edited=False).exists()   
    n2_is_edited = Thought.objects.filter(entry="nt2", edited=True).exists()    
    # Ensure the entry "nt1" is not marked as edited and "nt2" is edited
    self.assertTrue(n1_is_not_edited, "'nt1' should not be marked as edited.")
    self.assertTrue(n2_is_edited, "'nt2' should be marked as edited.")

    p1_is_not_edited = Thought.objects.filter(entry="pt1", edited=False).exists()   
    p2_is_edited = Thought.objects.filter(entry="pt2", edited=True).exists()    
    # Ensure the entry "pt1" is not marked as edited and "pt2" is edited
    self.assertTrue(p1_is_not_edited, "'pt1' should not be marked as edited.")
    self.assertTrue(p2_is_edited, "'pt2' should be marked as edited.")

  def test_create_thought_without_entry(self):
    with self.assertRaises(IntegrityError):
      Thought.objects.create(
        author=self.user, 
        entry=None,
        tag="WORK", 
        thought_type="POSITIVE"
      )
  
  def test_create_goal(self):    
    goal_exists = Goal.objects.filter(description="Complete test").exists()
    self.assertTrue(goal_exists)  

  def test_create_goal_without_description(self):
    with self.assertRaises(IntegrityError):
      Goal.objects.create(
        user=self.user,
        description=None,
        category="PERSONAL"
      )
  
  def test_create_goal_with_invalid_category(self):
    goal = Goal.objects.create(user=self.user, description="Test goal with invalid category", category="TEST")
    with self.assertRaises(ValidationError):
      goal.full_clean()

  def test_goal_completed(self):
    # Check if goal is not completed
    goal = self.goal
    self.assertFalse(goal.is_completed,"goal should be marked as not completed.")
    
    # Change the goal's status to completed
    goal.is_completed = True
    goal.save()
    # Re-fetch goal to verify the change was saved
    goal.refresh_from_db()
    self.assertTrue(goal.is_completed, "goal should be marked as completed.")

  def create_goals(self, count):
    for i in range(count):
      Goal.objects.create(user=self.user, description=f"Completed Goal {i + 1}", is_completed=True)

  def test_badge_reward_1(self):
    Goal.objects.create(user=self.user, description="Completed Goal 1", is_completed=True)
    first_goal = Goal.objects.get(description="Completed Goal 1")
    self.assertTrue(first_goal.is_completed, "The first goal should be marked as completed.")

  def test_badge_reward_2(self):
    self.create_goals(5)
    completed_goals_count = Goal.objects.filter(user=self.user, is_completed=True).count()
    self.assertEqual(completed_goals_count, 5, "The completed goals count should be 5.")
    
    if completed_goals_count in self.MILESTONES:
      Rewards.objects.create(
        receiver=self.user,
       reward_type="BADGE",
        description=self.MILESTONES[completed_goals_count]
      )

    reward_exists = Rewards.objects.filter(description=self.MILESTONES[completed_goals_count]).exists()
    self.assertTrue(reward_exists, "The reward for completing 5 goals should be awarded.")

  def test_badge_reward_3(self):
    self.create_goals(10)
    completed_goals_count = Goal.objects.filter(user=self.user, is_completed=True).count()
    self.assertEqual(completed_goals_count, 10, "The completed goals count should be 10.")

    if completed_goals_count in self.MILESTONES:
      Rewards.objects.create(
        receiver=self.user,
        reward_type="BADGE",
        description=self.MILESTONES[completed_goals_count]
      )

    reward_exists = Rewards.objects.filter(description=self.MILESTONES[completed_goals_count]).exists()
    self.assertTrue(reward_exists, "The reward for completing 10 goals should be awarded.")

  def test_badge_reward_4(self):
    self.create_goals(20)
    completed_goals_count = Goal.objects.filter(user=self.user, is_completed=True).count()
    self.assertEqual(completed_goals_count, 20, "The completed goals count should be 20.")

    if completed_goals_count in self.MILESTONES:
      Rewards.objects.create(
        receiver=self.user,
        reward_type="BADGE",
        description=self.MILESTONES[completed_goals_count]
      )

    reward_exists = Rewards.objects.filter(description=self.MILESTONES[completed_goals_count]).exists()
    self.assertTrue(reward_exists, "The reward for completing 20 goals should be awarded.")

  def test_badge_reward_5(self):
    self.create_goals(40)
    completed_goals_count = Goal.objects.filter(user=self.user, is_completed=True).count()
    self.assertEqual(completed_goals_count, 40, "The completed goals count should be 40.")

    if completed_goals_count in self.MILESTONES:
      Rewards.objects.create(
        receiver=self.user,
        reward_type="BADGE",
        description=self.MILESTONES[completed_goals_count]
      )

    reward_exists = Rewards.objects.filter(description=self.MILESTONES[completed_goals_count]).exists()
    self.assertTrue(reward_exists, "The reward for completing 40 goals should be awarded.")
    
  def test_badge_reward_6(self):
    self.create_goals(60)
    completed_goals_count = Goal.objects.filter(user=self.user, is_completed=True).count()
    self.assertEqual(completed_goals_count, 60, "The completed goals count should be 60.")

    if completed_goals_count in self.MILESTONES:
      Rewards.objects.create(
        receiver=self.user,
        reward_type="BADGE",
        description=self.MILESTONES[completed_goals_count]
      )

    reward_exists = Rewards.objects.filter(description=self.MILESTONES[completed_goals_count]).exists()
    self.assertTrue(reward_exists, "The reward for completing 60 goals should be awarded.")

  def test_badge_reward_7(self):
    self.create_goals(100)
    completed_goals_count = Goal.objects.filter(user=self.user, is_completed=True).count()
    self.assertEqual(completed_goals_count, 100, "The completed goals count should be 100.")

    if completed_goals_count in self.MILESTONES:
      Rewards.objects.create(
        receiver=self.user,
        reward_type='BADGE',
        description=self.MILESTONES[completed_goals_count]
      )

    reward_exists = Rewards.objects.filter(description=self.MILESTONES[completed_goals_count]).exists()
    self.assertTrue(reward_exists, "The reward for completing 100 goals should be awarded.")

class ViewsTestCase(TestCase):

  def setUp(self):
    self.c = Client()
    self.user = User.objects.create_user(username="user1", password="password123")
    self.c.login(username="user1", password="password123")

  def test_index(self):
    response = self.c.get(reverse("index"))
    self.assertEqual(response.status_code, 200)
    
  def test_dashboard(self):
    response = self.c.get(reverse("dashboard", args=[self.user.id]))
    self.assertEqual(response.status_code, 200)

  def test_dashboard_requires_login(self):
    self.c.logout()
    response = self.c.get(reverse("dashboard", args=[self.user.id]))
    self.assertNotEqual(response.status_code, 200)

  def test_profile(self):
    response = self.c.get(reverse("profile", args=[self.user.id]))
    self.assertEqual(response.status_code, 200)

  def test_positive_thought_create_and_view(self):
    url =  reverse("new_positive_thought")
    response = self.c.post(url, {
      "entry": "Test positive thought",
       "tag":"PERSONAL",
      })    
    # Check if positive thought was created successfully
    self.assertEqual(response.status_code, 302)
    # Check if new log is displayed on dashboard
    response = self.c.get(reverse("dashboard", args=[self.user.id]))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "Test positive thought")
    self.assertContains(response, "PERSONAL")

  def test_negative_thought_create_and_view(self):
    url =  reverse("new_negative_thought")
    response = self.c.post(url, {
      "entry": "Test negative thought",
       "tag":"PERSONAL",
      })    
    # Check if negative thought was created successfully
    self.assertEqual(response.status_code, 302)
    # Check if new log is displayed on dashboard
    response = self.c.get(reverse("dashboard", args=[self.user.id]))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "Test negative thought")
    self.assertContains(response, "PERSONAL")

  def test_goal_create_and_view(self):
    url = reverse("set_goal")

    response = self.c.post(url, {
      "description":"Test goals set up",
      "category":"PERSONAL"
      }) 

    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json()['success'], True)   
    # New goal displayed on dashboard
    response = self.c.get(reverse("dashboard", args=[self.user.id]))
    self.assertEqual(response.status_code, 200)
    # New goal is visible on the page
    self.assertContains(response, "Test goals set up")
    self.assertContains(response, "PERSONAL")

  def test_create_6_goals_error(self):
    url = reverse("set_goal")
    # Create 5 goals
    for i in range(5):
      response = self.c.post(url, {
        "description": f"Goal {i+1}",
        "category": "PERSONAL",
        })
      self.assertEqual(response.status_code, 200)
      self.assertEqual(response.json()['success'], True)
    # Create 6th goal
    response = self.c.post(url, {
      'description': 'Goal 6',
      'category': 'Work',
      })
    self.assertEqual(response.status_code, 400)
    self.assertEqual(response.json()['success'], False)
    

  def test_dashboard_displays_thoughts(self):    
    Thought.objects.create(author=self.user, entry="Test thought 1", tag="PERSONAL", thought_type="POSITIVE")
    Thought.objects.create(author=self.user, entry="Test thought 2", tag="WORK", thought_type="NEGATIVE")

    response = self.c.get(reverse("dashboard", args=[self.user.id]))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "Test thought 1")
    self.assertContains(response, "Test thought 2")

  def test_delete_thought_view(self):       
    thought=Thought.objects.create(author=self.user, entry="Test thought", tag="PERSONAL", thought_type="POSITIVE")
    self.assertTrue(Thought.objects.filter(id=thought.id).exists())
    
    response = self.c.delete(reverse("delete_log", args=[thought.id]))
    self.assertEqual(response.status_code, 200)
    self.assertFalse(Thought.objects.filter(id=thought.id).exists())

  def test_edit_thought_view(self):       
    thought=Thought.objects.create(author=self.user, entry="Old entry", tag="PERSONAL", thought_type="POSITIVE")
    self.assertTrue(Thought.objects.filter(id=thought.id).exists())
    #Edit thought
    response = self.c.put(reverse("edit_log", args=[thought.id]), 
                        data=json.dumps({"entry": "New entry","tag": "PERSONAL"}),
                        content_type='application/json')
    self.assertEqual(response.status_code, 200)
    #Update database
    thought.refresh_from_db()
    #Check new entry saved
    self.assertEqual(thought.entry, "New entry")
    self.assertEqual(thought.tag, "PERSONAL")

    # Updated thought is visible on the dashboard
    response = self.c.get(reverse('dashboard', args=[self.user.id]))
    self.assertEqual(response.status_code, 200)      
    self.assertContains(response, "New entry")
    self.assertContains(response, "PERSONAL")

  def test_edit_thought_view_with_empty_entry(self):       
    thought=Thought.objects.create(author=self.user, entry="Old entry", tag="PERSONAL", thought_type="POSITIVE")
    self.assertTrue(Thought.objects.filter(id=thought.id).exists())
    #Edit thought without adding new entry
    response = self.c.put(reverse("edit_log", args=[thought.id]), 
                          data=json.dumps({"entry": " ","tag": "PERSONAL"}),
                          content_type='application/json')
    self.assertEqual(response.status_code, 400)
    thought.refresh_from_db()
    self.assertEqual(thought.entry, "Old entry")

  