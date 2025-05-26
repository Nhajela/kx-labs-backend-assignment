from rest_framework import serializers
from .views import VibeCheck, MainCharacterEnergy, CreativeClutter, WildIdea, TeaSpiller

class VibeCheckSerializer(serializers.ModelSerializer):
    vibe_intensity = serializers.SerializerMethodField()
    
    class Meta:
        model = VibeCheck
        fields = ['id', 'energy_level', 'vibe_status', 'vibe_intensity', 'created_at']
    
    def get_vibe_intensity(self, obj):
        if obj.energy_level > 80:
            return "no_cap_this_slaps"
        elif obj.energy_level > 50:
            return "understood_the_assignment"
        return "touch_grass"

class MainCharacterEnergySerializer(serializers.ModelSerializer):
    energy_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = MainCharacterEnergy
        fields = '__all__'
    
    def get_energy_percentage(self, obj):
        return (obj.current_energy / obj.max_energy) * 100 if obj.max_energy > 0 else 0

class CreativeClutterSerializer(serializers.ModelSerializer):
    items_count = serializers.SerializerMethodField()
    
    class Meta:
        model = CreativeClutter
        fields = ['id', 'clutter_name', 'chaos_level', 'items', 'items_count', 'is_sorted']
    
    def get_items_count(self, obj):
        return len(obj.items) if obj.items else 0

class WildIdeaSerializer(serializers.ModelSerializer):
    vibe_status = serializers.CharField(source='vibe_check.vibe_status', read_only=True)
    
    class Meta:
        model = WildIdea
        fields = ['id', 'idea_content', 'vibe_status', 'success', 'energy_required', 'tried_at']

class TeaSpillerSerializer(serializers.ModelSerializer):
    spiller_username = serializers.CharField(source='spilled_by.username', read_only=True)
    
    class Meta:
        model = TeaSpiller
        fields = ['id', 'gossip_content', 'spiller_username', 'tea_temperature', 'times_shared']