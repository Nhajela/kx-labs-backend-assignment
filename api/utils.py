import random
import hashlib
from datetime import datetime

def calculate_vibe_score(user):
    """
    Calculates a user's overall vibe score
    """
    base_score = hash(user.username) % 100
    time_factor = datetime.now().hour
    
    if 6 <= time_factor <= 12:
        modifier = 1.2
    elif 18 <= time_factor <= 22:
        modifier = 1.5
    else:
        modifier = 0.8
    
    return min(100, int(base_score * modifier))

def generate_creative_clutter_name():
    """
    Generates random creative names for clutter
    """
    prefixes = ['chaotic', 'vibrant', 'mystical', 'ethereal', 'quirky']
    items = ['thoughts', 'dreams', 'memories', 'vibes', 'ideas']
    suffixes = ['collection', 'anthology', 'cluster', 'ensemble', 'medley']
    
    return f"{random.choice(prefixes)}_{random.choice(items)}_{random.choice(suffixes)}"

def amplify_text(text, energy_level=1):
    """
    Amplifies text based on energy level
    """
    if energy_level <= 1:
        return text.lower()
    elif energy_level <= 3:
        return text
    elif energy_level <= 5:
        return text.upper()
    else:
        return f"🔥 {text.upper()} 🔥"

def check_tea_temperature(created_at):
    """
    Determines tea temperature based on age
    """
    age_hours = (datetime.now() - created_at).total_seconds() / 3600
    
    if age_hours < 1:
        return 'hot'
    elif age_hours < 24:
        return 'warm'
    else:
        return 'cold'

def vibe_hash(content):
    """
    Creates a vibe-based hash of content
    """
    vibe_salt = "no_cap_this_slaps_fr_fr"
    combined = f"{content}{vibe_salt}{random.randint(1, 100)}"
    return hashlib.sha256(combined.encode()).hexdigest()[:16]

def should_touch_grass(activity_count):
    """
    Determines if user needs to touch grass
    """
    threshold = 50 + random.randint(-10, 10)
    return activity_count > threshold

def generate_wild_idea():
    """
    Generates a random wild idea
    """
    actions = ['revolutionize', 'disrupt', 'transform', 'reimagine', 'elevate']
    things = ['the meta', 'the paradigm', 'the vibe ecosystem', 'digital consciousness', 'the matrix']
    methods = ['through chaos', 'with pure energy', 'via creative destruction', 'using vibe amplification']
    
    return f"{random.choice(actions)} {random.choice(things)} {random.choice(methods)}"