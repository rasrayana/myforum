from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import Section, Topic, Message, PrivateMessage, Attachment, Rating
from .forms import MessageForm, TopicForm, PrivateMessageForm, UserRegistrationForm, UserLoginForm, UserCreationForm, AttachmentForm, UserProfileForm
from django.contrib.auth import logout 
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.http import JsonResponse
from .models import Message, MessageRating, Notification


def section_list(request):
    sections = Section.objects.all()
    return render(request, 'section_list.html', {'sections': sections})

def topic_list(request, section_id):
    section = get_object_or_404(Section, pk=section_id)
    topics = Topic.objects.filter(section=section)
    return render(request, 'topic_list.html', {'section': section, 'topics': topics})

def message_list(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    messages = Message.objects.filter(topic=topic)
    return render(request, 'message_list.html', {'topic': topic, 'messages': messages})

@login_required
def notification_list(request):
    notifications = Notification.objects.filter(user=request.user, is_read=False)
    return render(request, 'notification_list.html', {'notifications': notifications})


@login_required
def create_message(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.topic = topic
            message.created_by = request.user
            message.save()
            return redirect('message_list', topic_id=topic_id)
    else:
        form = MessageForm()

    return render(request, 'create_message.html', {'topic': topic, 'form': form})

@login_required
def create_topic(request, section_id):
    section = get_object_or_404(Section, pk=section_id)

    if request.method == 'POST':
        topic_form = TopicForm(request.POST)
        message_form = MessageForm(request.POST)

        if topic_form.is_valid() and message_form.is_valid():
            topic = topic_form.save(commit=False)
            topic.section = section
            topic.created_by = request.user
            topic.save()

            message = message_form.save(commit=False)
            message.topic = topic
            message.created_by = request.user
            message.save()

            return redirect('topic_list', section_id=section_id)
    else:
        topic_form = TopicForm()
        message_form = MessageForm()

    return render(request, 'create_topic.html', {'section': section, 'topic_form': topic_form, 'message_form': message_form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})


@login_required
def user_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            selected_option = form.cleaned_data['selected_option']
            section_id = form.cleaned_data.get('section_id')

            if selected_option == 'topic_list':
                return redirect('topic_list', section_id=2)
            elif selected_option == 'message_list':
                return redirect('message_list', topic_id=1  )
            elif selected_option == 'notification_list':
                return redirect('notification_list')
            elif selected_option == 'section_list':
                return redirect('section_list')
    else:
        form = UserProfileForm()

    return render(request, 'user_profile.html', {'form': form})  # Удалено из контекста section_id, так как он не используется в шаблоне



@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('edit_profile')
    else:
        form = UserChangeForm(instance=request.user)

    return render(request, 'edit_profile.html', {'form': form})

def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            next_page = 'user_profile'
            return redirect(next_page)
    else:
        form = UserRegistrationForm()
    return render(request, 'user_register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_page = 'user_profile'
            return redirect(next_page)
    else:
        form = UserLoginForm()
    return render(request, 'user_login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return render(request, 'user_logout.html')

def message_list(request, topic_id):
    """Выводит список сообщений для определенной темы."""
    # Извлекает тему из базы данных по ее идентификатору, возвращая ошибку 404, если не найдена
    topic = get_object_or_404(Topic, pk=topic_id)
    # Фильтрует сообщения, принадлежащие заданной теме
    messages = Message.objects.filter(topic=topic)
    # Отрисовывает шаблон, передавая информацию о теме и сообщениях
    return render(request, 'message_list.html', {'topic': topic, 'messages': messages})


@login_required
def edit_message(request, message_id):
    message = get_object_or_404(Message, pk=message_id)

    if request.method == 'POST':
        form = MessageForm(request.POST, instance=message)
        if form.is_valid():
            form.save()
            return redirect('message_list', topic_id=message.topic.id)
    else:
        form = MessageForm(instance=message)

    return render(request, 'edit_message.html', {'message': message, 'form': form})

@login_required
def delete_message(request, message_id):
    message = get_object_or_404(Message, pk=message_id)
    topic_id = message.topic.id
    message.delete()
    return redirect('message_list', topic_id=topic_id)


@login_required
def send_private_message(request, recipient_id):
    recipient = get_object_or_404(User, pk=recipient_id)

    if request.method == 'POST':
        form = PrivateMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.recipient = recipient
            message.save()
            return redirect('private_messages')
    else:
        form = PrivateMessageForm()

    return render(request, 'private_messages.html', {'recipient': recipient, 'form': form})

@login_required
def private_messages(request):
    user = request.user
    received_messages = PrivateMessage.objects.filter(recipient=user)
    sent_messages = PrivateMessage.objects.filter(sender=user)
    return render(request, 'private_messages.html', {'received_messages': received_messages, 'sent_messages': sent_messages})



@login_required
def send_message(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)

    if request.method == 'POST':
        message_form = MessageForm(request.POST)
        attachment_form = AttachmentForm(request.POST, request.FILES)

        if message_form.is_valid() and attachment_form.is_valid():
            message = message_form.save(commit=False)
            message.topic = topic
            message.created_by = request.user
            message.save()

            attachment = attachment_form.save(commit=False)
            attachment.message = message
            attachment.uploaded_by = request.user
            attachment.save()

            return redirect('message_list', topic_id=topic_id)
    else:
        message_form = MessageForm()
        attachment_form = AttachmentForm()

    return render(request, 'send_message.html', {'topic': topic, 'message_form': message_form, 'attachment_form': attachment_form})

@login_required
def reply_to_message(request, topic_id, message_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    original_message = get_object_or_404(Message, pk=message_id)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            reply_message = form.save(commit=False)
            reply_message.topic = topic
            reply_message.created_by = request.user
            reply_message.save()

            return redirect('message_list', topic_id=topic_id)
    else:
        form = MessageForm()

    return render(request, 'reply_to_message.html', {'topic': topic, 'original_message': original_message, 'form': form})



def rate_message(request, message_id, rating):
    message = get_object_or_404(Message, pk=message_id)

    existing_rating = MessageRating.objects.filter(user=request.user, message=message).first()

    if existing_rating:
        existing_rating.rating = rating
        existing_rating.save()
    else:
        new_rating = MessageRating(user=request.user, message=message, rating=rating)
        new_rating.save()

    return JsonResponse({'success': True})


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='section_list')  # Только администратор может закрыть тему
def close_topic(request, section_id, topic_id):
    section = get_object_or_404(Section, pk=section_id)
    topic = get_object_or_404(Topic, pk=topic_id, section=section)

    if request.method == 'POST':
        topic.is_closed = True
        topic.save()
        return redirect('topic_list', section_id=section_id)

    return render(request, 'close_topic.html', {'section': section, 'topic': topic})

