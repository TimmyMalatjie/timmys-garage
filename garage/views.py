# garage/views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
from pathlib import Path

def home(request):
    """Home page view"""
    context = {
        'page_title': 'Home - Where Legends Are Built',
        'hero_title': 'WHERE LEGENDS ARE BUILT',
        'mission_statement': "We're not just a garage; we're the starting line for your next win. From engine swaps to custom paint, we turn street cars into street legends."
    }
    return render(request, 'garage/home.html', context)

def services(request):
    """Services page view"""
    services_data = {
        'Engine & Performance': [
            {'name': 'Engine Swaps', 'desc': 'Drop in legendary engines - 2JZ, RB26, LS series. Raw power, properly installed.'},
            {'name': 'Turbo & Supercharger Installs', 'desc': 'Force-fed power delivery that transforms your ride into a weapon.'},
            {'name': 'Custom ECU Tuning', 'desc': 'Unlock every horse hiding in your engine. More power than you thought possible.'},
            {'name': 'Nitrous Oxide Systems', 'desc': 'N.O.S. systems for that extra kick when you need it most.'},
            {'name': 'Full Exhaust Systems', 'desc': 'Downpipes to tips. Let your engine breathe and roar.'},
            {'name': 'Cold Air Intakes', 'desc': 'Feed your beast the cold air it craves for maximum performance.'},
        ],
        'Aesthetics & Body': [
            {'name': 'Custom Paint Jobs', 'desc': 'Candy colors, pearls, metallics. Make your car impossible to ignore.'},
            {'name': 'Body Kits', 'desc': 'Widebody, drift-style kits that change the game completely.'},
            {'name': 'Carbon Fiber Parts', 'desc': 'Lightweight strength. Hoods, spoilers, mirrors - all race-proven.'},
            {'name': 'Vinyl Graphics & Decals', 'desc': 'Custom artwork that tells your story on the streets.'},
            {'name': 'Underglow & LEDs', 'desc': 'Light up the night. Street presence when you roll up.'},
        ],
        'Handling & Suspension': [
            {'name': 'Coilover Systems', 'desc': 'Adjustable height and dampening. Corner like you\'re on rails.'},
            {'name': 'Sway Bars & Strut Braces', 'desc': 'Chassis reinforcement for serious handling upgrades.'},
            {'name': 'Custom Wheel & Tire Packages', 'desc': 'Rolling on the finest rubber and rims money can buy.'},
            {'name': 'Brake System Upgrades', 'desc': 'Big brake kits. Stop as hard as you accelerate.'},
        ],
        'Interior': [
            {'name': 'Roll Cages & Harnesses', 'desc': 'Safety first, but damn it looks professional.'},
            {'name': 'Racing Seats & Steering Wheels', 'desc': 'Sparco, Recaro - brands that mean business.'},
            {'name': 'Custom Dashboards & Gauges', 'desc': 'Monitor every vital sign of your performance machine.'},
        ]
    }
    
    context = {
        'page_title': 'Services - Performance Modifications',
        'services': services_data
    }
    return render(request, 'garage/services.html', context)

def gallery(request):
    """Gallery page view"""
    # Sample gallery data - you'll replace with real images
    gallery_items = [
        {
            'image': 'images/gallery/skyline-1.jpg',
            'title': 'Nissan Skyline R34',
            'description': 'RB26 twin-turbo, custom widebody kit, full roll cage'
        },
        {
            'image': 'images/gallery/mustang-1.jpg', 
            'title': 'Ford Mustang GT',
            'description': 'Supercharged 5.0L, custom exhaust, racing suspension'
        },
        {
            'image': 'images/gallery/s2000-1.jpg',
            'title': 'Honda S2000',
            'description': 'VeilSide body kit, turbo conversion, custom red pearl paint'
        },
        # Add more gallery items as needed
    ]
    
    context = {
        'page_title': 'Gallery - Our Work',
        'gallery_items': gallery_items
    }
    return render(request, 'garage/gallery.html', context)

def about(request):
    """About page view"""
    context = {
        'page_title': 'About - Built by Passion',
        'owner_name': 'Timmy',
        'garage_story': "I've been building legends since before most people knew what a turbo was. This garage isn't just a business - it's where street dreams become reality.",
        'experience_years': 15,
        'specializations': [
            'Import Performance Tuning',
            'Custom Engine Swaps', 
            'Racing Preparation',
            'Show Car Builds'
        ]
    }
    return render(request, 'garage/about.html', context)

def contact(request):
    """Contact page view with form handling"""
    if request.method == 'POST':
        # Handle contact form submission
        data = {}
        if request.body:
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                data = {}

        if not data:
            data = request.POST

        name = data.get('name')
        email = data.get('email')
        car_info = data.get('car_info')
        message = data.get('message')

        # Simulate successful email handling
        is_json = request.headers.get('Content-Type') == 'application/json'
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        if is_json or is_ajax:
            return JsonResponse({
                'success': True,
                'message': 'Thanks for reaching out! We\'ll get back to you soon.'
            })

        return redirect('garage:contact_success')
    
    context = {
        'page_title': 'Contact - Get Your Build Started',
        'garage_info': {
            'address': '2847 Underground Blvd, Motor City, MC 48201',
            'phone': '(555) TUNE-NOW',
            'email': 'legends@timmysgarage.com',
            'hours': {
                'weekdays': 'Monday - Friday: 9AM - 9PM',
                'saturday': 'Saturday: 10AM - 6PM', 
                'sunday': 'Sunday: Closed'
            }
        }
    }
    return render(request, 'garage/contact.html', context)

def contact_success(request):
    """Contact success page view"""
    context = {
        'page_title': 'Message Sent - We Got You',
        'headline': 'MESSAGE RECEIVED',
        'subhead': 'Your build request is in our system. We will reach out soon.'
    }
    return render(request, 'garage/contact_success.html', context)

def favicon(request):
    """Serve favicon.ico"""
    favicon_path = settings.STATICFILES_DIRS[0] / 'favicon.ico'
    if not favicon_path.exists():
        favicon_path = settings.STATIC_ROOT / 'favicon.ico'
    
    if favicon_path.exists():
        return FileResponse(open(favicon_path, 'rb'), content_type='image/vnd.microsoft.icon')
    
    # Return a 204 No Content response if favicon doesn't exist
    from django.http import HttpResponse
    return HttpResponse(status=204)