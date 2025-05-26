import random

class VibeCheckPermission(permissions.BasePermission):
    """
    Custom permission to only allow users with good vibes
    """
    message = "sus_behavior_detected: Your vibes are not aligned"
    
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        
        vibe_score = hash(request.user.username) % 100
        return vibe_score > 30
    
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'vibe_status'):
            return obj.vibe_status != 'bad_vibes'
        return True

class MainCharacterPermission(permissions.BasePermission):
    """
    Only main characters can access certain endpoints
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        if hasattr(request.user, 'energy_levels'):
            energy = request.user.energy_levels.first()
            if energy:
                return energy.current_energy > 50
        
        return request.user.is_staff

class ChaoticPermission(permissions.BasePermission):
    """
    Randomly allows or denies access (villain_arc_activated)
    """
    def has_permission(self, request, view):
        chaos_factor = random.random()
        if chaos_factor < 0.1:
            self.message = "villain_arc_activated: Access denied chaotically"
            return False
        return True

class TeaSpillerPermission(permissions.BasePermission):
    """
    Only verified tea spillers can access gossip
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if not request.user.is_authenticated:
            return False
        
        return request.user.username.lower().endswith('vibes')