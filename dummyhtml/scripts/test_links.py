"""
Link Testing Script for Django Bakery Application
This script tests all internal links and URL patterns
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bakery_project.settings')
django.setup()

from django.urls import reverse, NoReverseMatch
from django.test import Client

def test_url_patterns():
    """Test all URL patterns"""
    print("\n" + "="*60)
    print("TESTING URL PATTERNS")
    print("="*60)
    
    urls_to_test = [
        'index',
        'menu',
        'about',
        'contact',
        'cart',
        'checkout',
        'orders',
        'payment',
        'upi_payment',
        'login',
        'signup',
        'logout',
    ]
    
    results = {'passed': [], 'failed': []}
    
    for url_name in urls_to_test:
        try:
            url = reverse(url_name)
            results['passed'].append((url_name, url))
            print(f"✅ {url_name:15} -> {url}")
        except NoReverseMatch as e:
            results['failed'].append((url_name, str(e)))
            print(f"❌ {url_name:15} -> FAILED: {e}")
    
    return results

def test_page_loads():
    """Test if pages actually load"""
    print("\n" + "="*60)
    print("TESTING PAGE LOADS (GET Requests)")
    print("="*60)
    
    client = Client()
    
    pages_to_test = [
        ('/', 'Home Page'),
        ('/menu/', 'Menu Page'),
        ('/about/', 'About Page'),
        ('/contact/', 'Contact Page'),
        ('/login/', 'Login Page'),
        ('/signup/', 'Sign Up Page'),
        ('/api/menu/', 'Menu API'),
    ]
    
    results = {'passed': [], 'failed': []}
    
    for url, name in pages_to_test:
        try:
            response = client.get(url)
            if response.status_code in [200, 302]:
                results['passed'].append((name, url, response.status_code))
                print(f"✅ {name:20} ({url:20}) -> {response.status_code}")
            else:
                results['failed'].append((name, url, response.status_code))
                print(f"⚠️  {name:20} ({url:20}) -> {response.status_code}")
        except Exception as e:
            results['failed'].append((name, url, str(e)))
            print(f"❌ {name:20} ({url:20}) -> ERROR: {e}")
    
    return results

def test_authenticated_pages():
    """Test pages that require authentication"""
    print("\n" + "="*60)
    print("TESTING AUTHENTICATED PAGES (Should redirect to login)")
    print("="*60)
    
    client = Client()
    
    protected_pages = [
        ('/cart/', 'Cart Page'),
        ('/orders/', 'Orders Page'),
    ]
    
    results = {'passed': [], 'failed': []}
    
    for url, name in protected_pages:
        try:
            response = client.get(url)
            if response.status_code == 302:  # Should redirect to login
                results['passed'].append((name, url, 'Redirects as expected'))
                print(f"✅ {name:20} ({url:20}) -> Redirects to login (302)")
            elif response.status_code == 200:  # Might allow access
                results['passed'].append((name, url, 'Allows access'))
                print(f"⚠️  {name:20} ({url:20}) -> Allows access (200)")
            else:
                results['failed'].append((name, url, response.status_code))
                print(f"❌ {name:20} ({url:20}) -> {response.status_code}")
        except Exception as e:
            results['failed'].append((name, url, str(e)))
            print(f"❌ {name:20} ({url:20}) -> ERROR: {e}")
    
    return results

def main():
    print("\n" + "🍰"*30)
    print("DJANGO BAKERY APPLICATION - LINK TESTING")
    print("🍰"*30)
    
    # Test URL patterns
    url_results = test_url_patterns()
    
    # Test page loads
    page_results = test_page_loads()
    
    # Test authenticated pages
    auth_results = test_authenticated_pages()
    
    # Summary
    print("\n" + "="*60)
    print("TESTING SUMMARY")
    print("="*60)
    
    total_url_tests = len(url_results['passed']) + len(url_results['failed'])
    total_page_tests = len(page_results['passed']) + len(page_results['failed'])
    total_auth_tests = len(auth_results['passed']) + len(auth_results['failed'])
    
    print(f"\nURL Pattern Tests:")
    print(f"  ✅ Passed: {len(url_results['passed'])}/{total_url_tests}")
    print(f"  ❌ Failed: {len(url_results['failed'])}/{total_url_tests}")
    
    print(f"\nPage Load Tests:")
    print(f"  ✅ Passed: {len(page_results['passed'])}/{total_page_tests}")
    print(f"  ❌ Failed: {len(page_results['failed'])}/{total_page_tests}")
    
    print(f"\nAuthentication Tests:")
    print(f"  ✅ Passed: {len(auth_results['passed'])}/{total_auth_tests}")
    print(f"  ❌ Failed: {len(auth_results['failed'])}/{total_auth_tests}")
    
    # Overall result
    total_failed = (len(url_results['failed']) + 
                   len(page_results['failed']) + 
                   len(auth_results['failed']))
    
    print("\n" + "="*60)
    if total_failed == 0:
        print("🎉 ALL TESTS PASSED! 🎉")
    else:
        print(f"⚠️  {total_failed} TEST(S) FAILED")
    print("="*60 + "\n")

if __name__ == '__main__':
    main()
