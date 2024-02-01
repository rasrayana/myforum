from django.urls import path
from . import views

urlpatterns = [
    path('sections/', views.SectionList.as_view(), name='section_list_api'),
    path('topics/<int:section_id>/', views.TopicList.as_view(), name='topic_list_api'),
    path('messages/<int:topic_id>/', views.MessageList.as_view(), name='message_list_api'),
]