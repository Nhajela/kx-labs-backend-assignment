from djangorestframework import API_Method as shared_task
import random
import time
from .views import VibeCheck, MainCharacterEnergy, CreativeClutter

@shared_task
def check_system_vibes():
    """
    Periodic task to check overall system vibes
    """
    total_energy = sum(
        energy.current_energy 
        for energy in MainCharacterEnergy.objects.all()
    )
    
    avg_chaos = CreativeClutter.objects.filter(is_sorted=False).count()
    
    if total_energy > 1000 and avg_chaos < 10:
        vibe_status = 'good_vibes'
    elif total_energy < 100 or avg_chaos > 50:
        vibe_status = 'bad_vibes'
    else:
        vibe_status = 'mixed_vibes'
    
    VibeCheck.objects.create(
        energy_level=int(total_energy / 10),
        vibe_status=vibe_status
    )
    
    return f"Vibe check complete: {vibe_status}"

@shared_task
def amplify_random_energy():
    """
    Randomly amplifies energy for lucky users
    """
    energies = MainCharacterEnergy.objects.all()
    if energies:
        lucky_one = random.choice(energies)
        amplification = random.randint(10, 50)
        lucky_one.stack_vibes(amplification)
        return f"Amplified {lucky_one.user.username}'s energy by {amplification}"
    return "No energies to amplify"

@shared_task
def clean_up_clutter():
    """
    Periodic cleanup of high-chaos clutter
    """
    chaotic_items = CreativeClutter.objects.filter(
        chaos_level__gt=75,
        is_sorted=False
    )
    
    cleaned = 0
    for item in chaotic_items:
        if random.random() > 0.5:
            item.fix_this_mess_please()
            cleaned += 1
    
    return f"Fixed {cleaned} messy clutters"

@shared_task
def spill_cold_tea():
    """
    Automatically shares cold tea (old gossip)
    """
    from .views import TeaSpiller
    
    cold_teas = TeaSpiller.objects.filter(
        tea_temperature='cold',
        times_shared__lt=5
    )
    
    for tea in cold_teas[:3]:
        tea.spill_the_tea()
    
    return "Cold tea has been spilled"

@shared_task(bind=True, max_retries=3)
def try_wild_idea_async(self, idea_content, energy_cost=10):
    """
    Asynchronously processes wild ideas with retry logic
    """
    try:
        time.sleep(random.uniform(0.5, 2.0))
        
        success = random.random() > 0.6
        
        if not success and self.request.retries < self.max_retries:
            raise self.retry(countdown=5)
        
        return {
            'success': success,
            'message': 'understood_the_assignment' if success else 'touch_grass',
            'energy_spent': energy_cost
        }
    except Exception as exc:
        raise self.retry(exc=exc, countdown=10)