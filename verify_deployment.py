#!/usr/bin/env python3
"""
Verify that Uglier is ready for Railway deployment
"""

import os
import sys

def check_file(filename, must_contain=None):
    """Check if file exists and optionally contains required text"""
    if not os.path.exists(filename):
        print(f"❌ MISSING: {filename}")
        return False
    
    if must_contain:
        with open(filename, 'r') as f:
            content = f.read()
            for required in must_contain:
                if required not in content:
                    print(f"❌ {filename} missing: {required}")
                    return False
    
    print(f"✅ {filename}")
    return True

def main():
    print("="*60)
    print("UGLIER RAILWAY DEPLOYMENT VERIFICATION")
    print("="*60)
    print()
    
    all_good = True
    
    # Check required files
    print("Checking required files...")
    all_good &= check_file('server.py', ['os.environ.get("PORT"', 'Flask'])
    all_good &= check_file('uglier.py', ['execute_block', 'variables'])
    all_good &= check_file('index.html', ['Uglier', 'textarea'])
    all_good &= check_file('requirements.txt', ['Flask', 'gunicorn'])
    all_good &= check_file('Procfile', ['gunicorn', 'server:app'])
    
    # Optional but recommended
    print("\nChecking optional files...")
    check_file('nixpacks.toml')
    check_file('runtime.txt')
    check_file('RAILWAY_DEPLOYMENT.md')
    
    print("\n" + "="*60)
    
    if all_good:
        print("✅ ALL REQUIRED FILES PRESENT AND CORRECT!")
        print("\nYou're ready to deploy to Railway!")
        print("\nNext steps:")
        print("1. Push these files to GitHub")
        print("2. Deploy on Railway from your GitHub repo")
        print("3. Railway will auto-detect and deploy")
        print("\n" + "="*60)
        return 0
    else:
        print("❌ SOME FILES ARE MISSING OR INCORRECT")
        print("\nPlease fix the issues above before deploying.")
        print("\n" + "="*60)
        return 1

if __name__ == "__main__":
    sys.exit(main())
