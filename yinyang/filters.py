import django_filters
from .models import Thought

class ThoughtFilter(django_filters.FilterSet):
    tag = django_filters.ChoiceFilter(choices=Thought.TAG)
    thought_type = django_filters.ChoiceFilter(choices=Thought.TYPE)

    class Meta:
        model = Thought
        fields = ['tag', 'thought_type']