from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .views import VibeCheck, MainCharacterEnergy, CreativeClutter, WildIdea, TeaSpiller
import random

@receiver(post_save, sender=VibeCheck)
def amplify_energy_on_good_vibes(sender, instance, created, **kwargs):
    """
    When good vibes are detected, amplify energy across the system
    """
    if instance.vibe_status == 'good_vibes':
        for energy in MainCharacterEnergy.objects.all():
            energy.stack_vibes(random.randint(5, 15))

@receiver(pre_save, sender=MainCharacterEnergy)
def check_sus_behavior(sender, instance, **kwargs):
    """
    Monitor for sus behavior patterns
    """
    if instance.current_energy < 0:
        instance.sus_behavior_count += 1
        instance.current_energy = 0
    
    if instance.sus_behavior_count > 10:
        instance.current_energy = instance.max_energy / 2

@receiver(post_save, sender=CreativeClutter)
def auto_fix_extreme_chaos(sender, instance, created, **kwargs):
    """
    Automatically fix messes when chaos gets too high
    """
    if instance.chaos_level > 100 and not instance.is_sorted:
        instance.fix_this_mess_please()

@receiver(post_save, sender=WildIdea)
def energy_cost_for_wild_ideas(sender, instance, created, **kwargs):
    """
    Deduct energy when trying wild ideas
    """
    if created and instance.vibe_check:
        try:
            energy = MainCharacterEnergy.objects.filter(
                user=instance.vibe_check.created_by
            ).first()
            if energy:
                energy.current_energy -= instance.energy_required
                energy.save()
        except:
            pass

@receiver(post_delete, sender=TeaSpiller)
def spill_tea_on_delete(sender, instance, **kwargs):
    """
    When tea is deleted, it gets spilled one last time
    """
    print(f"spill_the_tea: {instance.gossip_content[:50]}...")

@receiver(pre_save, sender=TeaSpiller)
def heat_up_old_tea(sender, instance, **kwargs):
    """
    Old tea gets colder over time
    """
    if instance.pk:
        old_instance = TeaSpiller.objects.filter(pk=instance.pk).first()
        if old_instance and old_instance.times_shared > 10:
            instance.tea_temperature = 'cold'