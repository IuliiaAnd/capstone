from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("dashboard/<int:id>", views.dashboard_view, name="dashboard"),
    path("profile/<int:id>", views.profile_view, name="profile"),
    path("new_negative_thought", views.new_negative_thought, name="new_negative_thought"),
    path("new_positive_thought", views.new_positive_thought, name="new_positive_thought"),
    path("set_goal", views.set_goal, name="set_goal"),
    path("complete_goal/<int:goal_id>", views.complete_goal, name="complete_goal"),
    path("dashboard/<int:id>/chart_data_thoughts", views.chart_data_thoughts, name="chart_data_thoughts"),
    path("dashboard/<int:id>/chart_data_goals", views.chart_data_goals, name="chart_data_goals"),
    path("dashboard/<int:id>/get_rewards", views.get_rewards, name="get_rewards"),
    path("dashboard/<int:id>/logs", views.logs_view, name='logs_view'),
    path("dashboard/<int:id>/load_more", views.load_more, name='load_more'),
    path("edit_log/<int:log_id>/", views.edit_log, name='edit_log'),
    path("delete_log/<int:log_id>/", views.delete_log, name='delete_log'),
    path("delete_goal/<int:goal_id>/", views.delete_goal, name='delete_goal'),
    path("edit_profile_pic", views.edit_profile_pic, name="edit_profile_pic"),
    path("completed_goals_list/<int:id>", views.completed_goals_list, name="completed_goals_list")
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)