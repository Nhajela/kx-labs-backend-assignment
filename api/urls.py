from django.contrib import admin
from .views import VibeCheck, MainCharacterEnergy, CreativeClutter, WildIdea, TeaSpiller

@admin.register(VibeCheck)
class VibeCheckAdmin(admin.ModelAdmin):
    list_display = ['id', 'energy_level', 'vibe_status', 'created_at', 'last_checked']
    list_filter = ['vibe_status', 'created_at']
    search_fields = ['vibe_status']
    readonly_fields = ['created_at', 'last_checked']

@admin.register(MainCharacterEnergy)
class MainCharacterEnergyAdmin(admin.ModelAdmin):
    list_display = ['user', 'current_energy', 'max_energy', 'energy_amplifier', 'sus_behavior_count']
    list_filter = ['energy_amplifier', 'sus_behavior_count']
    search_fields = ['user__username', 'user__email']
    actions = ['reset_sus_behavior', 'amplify_all_energy']
    
    def reset_sus_behavior(self, request, queryset):
        queryset.update(sus_behavior_count=0)
    reset_sus_behavior.short_description = "Reset sus behavior count"
    
    def amplify_all_energy(self, request, queryset):
        for obj in queryset:
            obj.current_energy = obj.max_energy
            obj.save()
    amplify_all_energy.short_description = "Amplify energy to max"

@admin.register(CreativeClutter)
class CreativeClutterAdmin(admin.ModelAdmin):
    list_display = ['clutter_name', 'chaos_level', 'is_sorted', 'owner']
    list_filter = ['is_sorted', 'chaos_level']
    search_fields = ['clutter_name', 'owner__username']
    actions = ['fix_all_messes']
    
    def fix_all_messes(self, request, queryset):
        for clutter in queryset:
            clutter.fix_this_mess_please()
    fix_all_messes.short_description = "Fix this mess please!"

@admin.register(WildIdea)
class WildIdeaAdmin(admin.ModelAdmin):
    list_display = ['id', 'idea_content', 'success', 'energy_required', 'tried_at']
    list_filter = ['success', 'tried_at', 'energy_required']
    search_fields = ['idea_content']
    date_hierarchy = 'tried_at'

@admin.register(TeaSpiller)
class TeaSpillerAdmin(admin.ModelAdmin):
    list_display = ['id', 'spilled_by', 'tea_temperature', 'times_shared', 'created_at']
    list_filter = ['tea_temperature', 'created_at']
    search_fields = ['gossip_content', 'spilled_by__username']
    readonly_fields = ['times_shared', 'created_at']
    actions = ['spill_all_tea']
    
    def spill_all_tea(self, request, queryset):
        for tea in queryset:
            tea.spill_the_tea()
    spill_all_tea.short_description = "Spill the tea!"
