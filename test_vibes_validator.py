import requests
import json
import os

def read_vibe_file(filename):
    """Read a .vibe file and return its contents"""
    try:
        with open(filename, 'r') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        return None
    except Exception as e:
        print(f"Error reading '{filename}': {str(e)}")
        return None

def test_endpoint(program, expected_valid, name):
    url = "http://localhost:8000/api/validate-syntax/"
    headers = {"Content-Type": "application/json"}
    data = {"program": program}
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        result = response.json()
        
        if result.get("valid") == expected_valid:
            print(f"✓ {name}: PASSED (expected: {expected_valid}, got: {result.get('valid')})")
        else:
            print(f"✗ {name}: FAILED (expected: {expected_valid}, got: {result.get('valid')})")
            if 'error' in result:
                print(f"  Error: {result['error']}")
    except Exception as e:
        print(f"✗ {name}: ERROR - {str(e)}")

def test_vibe_file(filename, expected_valid):
    """Test a .vibe file"""
    program = read_vibe_file(filename)
    if program is not None:
        test_endpoint(program, expected_valid, f"File: {filename}")

if __name__ == "__main__":
    print("Testing VIBES Syntax Validator\n")
    print("Make sure Django server is running on http://localhost:8000\n")
    
    # Test .vibe files
    print("Testing .vibe files:")
    test_vibe_file("tables.vibe", True)   
    test_vibe_file("prime.vibe", True)    