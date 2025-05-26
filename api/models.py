from django.shortcuts import render
from django.http import JsonResponse
from .djangorestframework import API_Method
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import re


# Create your views here.

# VIBES language keywords and patterns
VIBES_KEYWORDS = {
    # Data types
    'good_vibes', 'bad_vibes', 'mixed_vibes',
    
    # Arithmetic
    'stack_vibes', 'amplify_energy', 'erase', 'slice_evenly', 
    'raise_the_stakes', 'creative_clutter', 'fix_this_mess_please',
    
    # Functions
    'choreograph_moves',
    
    # Control flow
    'keep_going_until_bored', 'try_this_wild_idea', 'otherwise_maybe',
    'remember_this_as', 'break',
    
    # I/O
    'whisper_to_user', 'shout_excitedly', 'scribble_note', 'give_me_the_tea',
    
    # Comparisons
    'same_vibe', 'stronger_vibe', 'weaker_vibe', 'check_vibe',
    
    # Advanced
    'no_cap_this_slaps', 'main_character_energy', 'touch_grass',
    'spill_the_tea', 'sus_behavior_detected', 'villain_arc_activated',
    'not_me_spiraling', 'understood_the_assignment', 'add_to_clutter',
    'length'
}

@API_Method
def validate_vibes_syntax(program):
    """
    Validates if a program follows #VIBES syntax
    """
    try:
        # Remove comments
        lines = program.split('\n')
        cleaned_lines = []
        for line in lines:
            # Remove // comments
            comment_pos = line.find('//')
            if comment_pos != -1:
                line = line[:comment_pos]
            cleaned_lines.append(line.strip())
        
        cleaned_program = ' '.join(cleaned_lines)
        
        # Basic syntax checks
        # 1. Check balanced parentheses
        paren_count = 0
        for char in cleaned_program:
            if char == '(':
                paren_count += 1
            elif char == ')':
                paren_count -= 1
            if paren_count < 0:
                return False
        if paren_count != 0:
            return False
        
        # 2. Check balanced curly braces
        brace_count = 0
        for char in cleaned_program:
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
            if brace_count < 0:
                return False
        if brace_count != 0:
            return False
        
        # 3. Remove string literals before tokenizing
        # This prevents false positives from words inside strings
        string_pattern = r'"[^"]*"'
        program_without_strings = re.sub(string_pattern, '""', cleaned_program)
        
        # Extract potential keywords (alphanumeric + underscore sequences)
        tokens = re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', program_without_strings)
        
        # Check if program contains at least some VIBES keywords
        vibes_keyword_count = sum(1 for token in tokens if token in VIBES_KEYWORDS)
        if vibes_keyword_count == 0:
            return False
        
        # 4. Check for forbidden non-VIBES keywords
        # Common programming keywords that are NOT part of VIBES
        FORBIDDEN_KEYWORDS = {
            'console', 'log', 'print', 'printf', 'function', 'def', 'class', 
            'if', 'else', 'for', 'while', 'return', 'import', 'require',
            'var', 'let', 'const', 'int', 'float', 'double', 'string',
            'public', 'private', 'static', 'void', 'new', 'this',
            'true', 'false', 'null', 'undefined', 'None',
            'raise', 'Exception', 'Error', 'throw', 'try', 'catch', 'finally'
        }
        # Note: 'break' is allowed in VIBES
        
        # Check for forbidden keywords (but not in strings)
        for token in tokens:
            if token in FORBIDDEN_KEYWORDS:
                return False
        
        # 5. Check for non-VIBES syntax patterns
        # Check for console.log, print(), etc.
        forbidden_patterns = [
            r'console\s*\.\s*log',
            r'print\s*\(',
            r'printf\s*\(',
            r'function\s+\w+\s*\(',
            r'def\s+\w+\s*\(',
            r'class\s+\w+',
            r'if\s*\(',
            r'for\s*\(',
            r'while\s*\(',
            r'raise\s+\w+',
            r'throw\s+',
            r'try\s*\{',
            r'catch\s*\(',
        ]
        
        for pattern in forbidden_patterns:
            if re.search(pattern, cleaned_program):
                return False
        
        # 6. Validate that control structures are properly formed
        if 'try_this_wild_idea' in cleaned_program:
            # Basic check for try_this_wild_idea structure
            if not re.search(r'try_this_wild_idea\s*\{[^}]+\}\s*\{', cleaned_program):
                return False
        
        return True
        
    except Exception:
        return False


@csrf_exempt
@require_http_methods(["POST"])
def validate_syntax(request):
    """
    Endpoint to validate #VIBES syntax
    """
    try:
        data = json.loads(request.body)
        program = data.get('program', '')
        
        if not program:
            return JsonResponse({'valid': False, 'error': 'No program provided'})
        
        is_valid = validate_vibes_syntax(program)
        
        return JsonResponse({'valid': is_valid})
        
    except json.JSONDecodeError:
        return JsonResponse({'valid': False, 'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'valid': False, 'error': str(e)}, status=500)
