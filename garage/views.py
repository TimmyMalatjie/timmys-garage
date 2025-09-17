# garage/views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

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
        try:
            data = json.loads(request.body)
            name = data.get('name')
            email = data.get('email')
            car_info = data.get('car_info')
            message = data.get('message')
            
            # Here you would typically save to database or send email
            # For now, just return success response
            return JsonResponse({
                'success': True,
                'message': 'Thanks for reaching out! We\'ll get back to you soon.'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': 'Something went wrong. Try calling us directly.'
            })
    
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