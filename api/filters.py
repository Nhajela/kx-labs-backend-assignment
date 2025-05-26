from django_filters import rest_framework as filters
from .views import VibeCheck, MainCharacterEnergy, CreativeClutter, WildIdea, TeaSpiller

class VibeCheckFilter(filters.FilterSet):
    min_energy = filters.NumberFilter(field_name='energy_level', lookup_expr='gte')
    max_energy = filters.NumberFilter(field_name='energy_level', lookup_expr='lte')
    vibe_type = filters.ChoiceFilter(field_name='vibe_status', choices=[
        ('good_vibes', 'Good Vibes'),
        ('bad_vibes', 'Bad Vibes'),
        ('mixed_vibes', 'Mixed Vibes'),
    ])
    recent = filters.BooleanFilter(method='filter_recent')
    
    class Meta:
        model = VibeCheck
        fields = ['vibe_status', 'created_at']
    
    def filter_recent(self, queryset, name, value):
        if value:
            from datetime import datetime, timedelta
            cutoff = datetime.now() - timedelta(hours=24)
            return queryset.filter(created_at__gte=cutoff)
        return queryset

class MainCharacterEnergyFilter(filters.FilterSet):
    high_energy = filters.BooleanFilter(method='filter_high_energy')
    sus_detected = filters.BooleanFilter(field_name='sus_behavior_count', lookup_expr='gt', exclude=False)
    amplified = filters.NumberFilter(field_name='energy_amplifier', lookup_expr='gt')
    
    class Meta:
        model = MainCharacterEnergy
        fields = ['user', 'energy_amplifier']
    
    def filter_high_energy(self, queryset, name, value):
        if value:
            return queryset.filter(current_energy__gte=80)
        return queryset.filter(current_energy__lt=80)

class CreativeClutterFilter(filters.FilterSet):
    chaos_range = filters.RangeFilter(field_name='chaos_level')
    needs_fixing = filters.BooleanFilter(method='filter_needs_fixing')
    owner_username = filters.CharFilter(field_name='owner__username', lookup_expr='icontains')
    
    class Meta:
        model = CreativeClutter
        fields = ['is_sorted', 'owner']
    
    def filter_needs_fixing(self, queryset, name, value):
        if value:
            return queryset.filter(is_sorted=False, chaos_level__gt=50)
        return queryset

class TeaSpillerFilter(filters.FilterSet):
    temperature = filters.MultipleChoiceFilter(
        field_name='tea_temperature',
        choices=[('hot', 'Hot'), ('warm', 'Warm'), ('cold', 'Cold')]
    )
    viral = filters.BooleanFilter(method='filter_viral')
    spiller = filters.CharFilter(field_name='spilled_by__username', lookup_expr='iexact')
    
    class Meta:
        model = TeaSpiller
        fields = ['tea_temperature', 'created_at']
    
    def filter_viral(self, queryset, name, value):
        if value:
            return queryset.filter(times_shared__gte=10)
        return queryset.filter(times_shared__lt=10)