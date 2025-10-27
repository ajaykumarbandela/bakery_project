import webbrowser
import time

print("=" * 60)
print("🎉 BAKERY WEBSITE - Opening in Browser")
print("=" * 60)
print("\nServer is running at: http://127.0.0.1:8080/")
print("\nOpening pages:")
print("1. Homepage: http://127.0.0.1:8080/")
print("2. Menu Page: http://127.0.0.1:8080/menu/")
print("\nOpening in 2 seconds...")

time.sleep(2)

# Open homepage
print("\n✓ Opening homepage...")
webbrowser.open('http://127.0.0.1:8080/')

time.sleep(1)

# Open menu page
print("✓ Opening menu page...")
webbrowser.open('http://127.0.0.1:8080/menu/')

print("\n" + "=" * 60)
print("✅ Browser windows opened!")
print("=" * 60)
print("\nIf pages don't load, manually visit:")
print("  • http://127.0.0.1:8080/")
print("  • http://127.0.0.1:8080/menu/")
print("\n⚠️  Use HTTP (not HTTPS)")
print("=" * 60)
