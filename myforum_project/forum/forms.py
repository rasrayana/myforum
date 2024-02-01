from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import Message, Topic, PrivateMessage, Attachment
from django.urls import reverse

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['title', 'section']

class PrivateMessageForm(forms.ModelForm):
    class Meta:
        model = PrivateMessage
        fields = ['content']

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    next_page = forms.CharField(widget=forms.HiddenInput(), required=False)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['next_page'].initial = reverse('user_profile')

class UserLoginForm(AuthenticationForm):
    next_page = forms.CharField(max_length=100, required=False, widget=forms.HiddenInput())
    class Meta:
        model = User
    

class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ['file']

    def __init__(self, *args, **kwargs):
        super(AttachmentForm, self).__init__(*args, **kwargs)
        self.fields['file'].required = False

class UserProfileForm(forms.Form):
    options = [
        ('section_list', 'Section List'),
        ('message_list', 'Message List'),
        ('notification_list', 'Notification List'),
        ('topic_list', 'Topic List'),
    ]

    selected_option = forms.ChoiceField(choices=options)
    section_id = forms.IntegerField(required=False)  # Добавляем поле section_id
