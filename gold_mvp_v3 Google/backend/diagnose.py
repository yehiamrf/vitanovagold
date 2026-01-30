"""
VitaNova Diagnostic Script
===========================
Run this to see the exact error when starting the server
"""

import sys
import os

# Change to backend directory
backend_dir = r'C:\Users\yehia\Downloads\gold_mvp_v2\backend'
os.chdir(backend_dir)
sys.path.insert(0, backend_dir)

print("=" * 70)
print("VITANOVA SERVER DIAGNOSTIC")
print("=" * 70)

print(f"\nWorking Directory: {os.getcwd()}")
print(f"Python Version: {sys.version}")

# Test each import step by step
tests = [
    ("1. Standard Libraries", lambda: __import__('http.client')),
    ("2. Flask", lambda: __import__('flask')),
    ("3. Flask-CORS", lambda: __import__('flask_cors')),
    ("4. Config", lambda: __import__('config')),
    ("5. Models", lambda: __import__('models')),
    ("6. User Registration Logger", lambda: __import__('user_registration_logger')),
    ("7. Auth Routes", lambda: __import__('auth_routes')),
]

all_passed = True

for name, test_func in tests:
    print(f"\n[Testing] {name}...", end=" ")
    try:
        test_func()
        print("✅ PASS")
    except Exception as e:
        print(f"❌ FAIL")
        print(f"  Error: {type(e).__name__}: {e}")
        all_passed = False
        
        # Show traceback for failed imports
        import traceback
        print("\n  Traceback:")
        traceback.print_exc()
        print()

print("\n" + "=" * 70)

if all_passed:
    print("✅ ALL TESTS PASSED!")
    print("\nYour server should start. Try running:")
    print("    python Goldprices.py")
else:
    print("❌ SOME TESTS FAILED!")
    print("\nThe error above shows what's preventing your server from starting.")
    print("Share this output to get help fixing it.")

print("=" * 70)
