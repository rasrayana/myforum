from django.urls import path, include
from . import views

urlpatterns = [ 
    path('sections/', views.section_list, name='section_list'),
    path('topics/<int:section_id>/', views.topic_list, name='topic_list'),
    path('messages/<int:topic_id>/', views.message_list, name='message_list'),
    path('notifications/', views.notification_list, name='notification_list'),
    path('messages/<int:topic_id>/create/', views.create_message, name='create_message'),
    path('messages/<int:message_id>/edit/', views.edit_message, name = 'edit_message'),
    path('messages/<int:message_id>/edit/', views.delete_message, name = 'delete_message'),
    path('private-messages/', views.private_messages, name='private_messages'),
    path('send-private-message/<int:recipient_id>/', views.send_private_message, name='send_private_message'),
    path('send-message/<int:topic_id>/', views.send_message, name='send_message'),
    path('edit-profile/', views.edit_profile, name = 'edit_profile'),
    path('rate-message//<int:message_id>/<int:value>/', views.rate_message, name = 'rate_message'),
    path('reply-to-message/<int:topic_id>/<int:message_id>/', views.reply_to_message, name='reply_to_message'),
    path('user_register/', views.user_register, name = 'user_register' ),
    path('user_login/', views.user_login, name = 'user_login'),
    path('user_logout/', views.user_logout, name = 'user_logout'),
    path('user-profile/', views.user_profile, name ='user_profile'),
    path('change_password/', views.change_password, name = 'change_password'),
    path('api/', include('forum.api.urls')),
    path('sections/<int:section_id>/topics/<int:topic_id>/close/', views.close_topic, name='close_topic'),
]