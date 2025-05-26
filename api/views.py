from django.db import models
from django.contrib.auth.models import User

class VibeCheck(models.Model):
    energy_level = models.IntegerField(default=100)
    vibe_status = models.CharField(max_length=50, choices=[
        ('good_vibes', 'Good Vibes Only'),
        ('bad_vibes', 'Bad Vibes Alert'),
        ('mixed_vibes', 'Mixed Signals'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    last_checked = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Vibe Check"
        verbose_name_plural = "Vibe Checks"

class MainCharacterEnergy(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='energy_levels')
    current_energy = models.FloatField(default=0.0)
    max_energy = models.FloatField(default=100.0)
    energy_amplifier = models.IntegerField(default=1)
    sus_behavior_count = models.IntegerField(default=0)
    
    def stack_vibes(self, amount):
        self.current_energy += amount
        self.save()
    
    class Meta:
        verbose_name = "Main Character Energy"
        verbose_name_plural = "Main Character Energies"

class CreativeClutter(models.Model):
    clutter_name = models.CharField(max_length=200)
    chaos_level = models.IntegerField(default=0)
    items = models.JSONField(default=list)
    is_sorted = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    def fix_this_mess_please(self):
        self.is_sorted = True
        self.chaos_level = 0
        self.save()

class WildIdea(models.Model):
    idea_content = models.TextField()
    vibe_check = models.ForeignKey(VibeCheck, on_delete=models.CASCADE)
    tried_at = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=False)
    energy_required = models.IntegerField(default=10)
    
    class Meta:
        ordering = ['-tried_at']

class TeaSpiller(models.Model):
    gossip_content = models.TextField()
    spilled_by = models.ForeignKey(User, on_delete=models.CASCADE)
    tea_temperature = models.CharField(max_length=20, choices=[
        ('hot', 'Piping Hot Tea'),
        ('warm', 'Luke Warm Tea'),
        ('cold', 'Yesterday\'s Tea'),
    ])
    times_shared = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def spill_the_tea(self):
        self.times_shared += 1
        self.save()
