#!/usr/bin/env python
"""
Generate a secure SECRET_KEY for Django production
Run this and copy the output to your environment variables
"""

from django.core.management.utils import get_random_secret_key

print("\n" + "="*60)
print("🔐 DJANGO SECRET KEY GENERATOR")
print("="*60)
print("\nYour new SECRET_KEY:")
print("\n" + get_random_secret_key())
print("\n" + "="*60)
print("\n📋 Instructions:")
print("1. Copy the key above")
print("2. Set it as SECRET_KEY environment variable on your hosting platform")
print("3. Never commit this to Git!")
print("="*60 + "\n")
