from rest_framework import generics
from forum.models import Section, Topic, Message
from .serializers import SectionSerializer, TopicSerializer, MessageSerializer

class SectionList(generics.ListAPIView):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer

class TopicList(generics.ListAPIView):
    serializer_class = TopicSerializer

    def get_queryset(self):
        section_id = self.kwargs['section_id']
        return Topic.objects.filter(section__id=section_id)

class MessageList(generics.ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        topic_id = self.kwargs['topic_id']
        return Message.objects.filter(topic__id=topic_id)