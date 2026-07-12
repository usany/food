import re
from datetime import datetime
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import MenuItem
from .constants import * 
import os

def root_redirect(request):
    """Redirect to default locale. Client-side JS on the target page further redirects based on localStorage."""
    from django.shortcuts import redirect
    lang = request.COOKIES.get('base', 'ko')
    loc = request.COOKIES.get('bases', 'se')
    resp = redirect(f'{lang}/{loc}/')
    resp.set_cookie('base', lang)
    resp.set_cookie('bases', loc)
    return resp


def home_menu(request, bases):
    restaurants_items = [r for r in RESTAURANTS if r['campus'] == bases]
    return render(request, 'pages/home.html', {'items': restaurants_items, 'bases': bases})

def menu_list(request, path, bases):
    """Display menu items for the restaurant selected on the home page."""
    r = next((r for r in RESTAURANTS if r['path'] == path), None)
    if not r:
        from django.http import Http404
        raise Http404("Restaurant not found")
    title = r['title']
    weekday_names = ['mon', 'tue', 'wed', 'thu', 'fri']
    from datetime import timedelta
    today = datetime.today()
    hour = datetime.now().hour
    today_idx = datetime.today().weekday()
    current_idx = today_idx + 1 if hour > 18 else today_idx
    default_day = request.GET.get('day', weekday_names[current_idx] if current_idx < 5 else 'mon')
    time_to_meal = {'breakfast': [8, 9, 10], 'lunch': [11, 12, 13, 14], 'snack': [15, 16], 'dinner': [17, 18, 19], 'onedish': [8, 9, 10, 11, 12, 13, 14, 15, 16], 'unmanned': [14, 15, 16]}
    previous = request.GET.get('previous', 0)
    weekdays = [d for d in WEEKDAYS if d['day'] == default_day]
    selected_day = request.GET.get('day', weekdays[0]['day'] if weekdays else None)
    start_of_week = today - timedelta(days=today_idx) - timedelta(weeks=int(previous)) if today_idx < 5 else today + timedelta(days=7-today_idx)
    week = [(start_of_week + timedelta(days=i)).strftime('%Y%m%d') for i in range(5)]
    week_without_year = [(start_of_week + timedelta(days=i)).strftime('%m.%d') for i in range(5)]
    selected_date = week[weekday_names.index(selected_day)]
    issemester = MenuItem.objects.filter(place='his', meal='breakfast', date=selected_date).exists() if path in ['his', 'hgs'] else MenuItem.objects.filter(place='ch', meal='dinner', date=selected_date).exists()
    all_meals = r['mealsSemester'] if issemester else r['mealsVacation']
    default_meal_name = next((m for m, hours in time_to_meal.items() if hour in hours and m in [meal['time'] for meal in MEALS if meal['name'] in all_meals]), 'breakfast' if '아침' in all_meals else 'lunch')
    default_meal = request.GET.get('meal', default_meal_name)
    if 'day' not in request.GET or 'meal' not in request.GET:
        from django.shortcuts import redirect
        return redirect(request.path + f'?day={default_day}&meal={default_meal}&previous={previous}')
    meal_tabs = [
        {
            'id': next((meal['time'] for meal in MEALS if meal['name'] == m), None),
            'label': m,
            'meal_time': r['mealsSemesterTime'][r['mealsSemester'].index(m)] if issemester else r['mealsVacationTime'][r['mealsVacation'].index(m)]
        }
        for m in all_meals
    ]
    selected_meal = request.GET.get('meal', meal_tabs[0]['id'] if meal_tabs else None)
    
    all_dishes = FIXED_MENU.get(path, [])
    filtered_dishes = [
        d for d in all_dishes
        if selected_meal in d.get('time_category', [])
    ] if selected_meal else all_dishes
    db_qs = MenuItem.objects.filter(place=path, meal=selected_meal, day=selected_day, date=selected_date)
    filtered_dishes = list(db_qs) + filtered_dishes
    # Enrich FIXED_MENU dicts with safe_main so the template can use dish.safe_main
    # MenuItem model instances have safe_main as a property
    filtered_dishes = [
        {**d, 'safe_main': re.sub(r'[\\/*?:"<>|]', '+', d.get('main', '') or '')}
        if isinstance(d, dict) else d
        for d in filtered_dishes
    ]


    tabs = []
    for i, w in enumerate(WEEKDAYS):
        t = dict(w)
        t['date'] = week_without_year[i]
        tabs.append(t)

    return render(request, 'pages/menu_list.html', {
        'tabs': tabs,
        'title': title, 
        'meal_tabs': meal_tabs,
        'selected_meal': selected_meal,
        'selected_day': selected_day,
        'menu': filtered_dishes,
        'bases': bases,
        'path': path,
        'week': week,
        'previous': previous,
        'storage_url': os.getenv('STORAGE_URL')
    })


def menu_detail(request, path, meal, bases):
    """Display details for a specific menu item"""
    restaurant = next((r for r in RESTAURANTS if r['path'] == path), None)
    title = restaurant['title']
    meal_tabs = restaurant['mealsSemester']
    if not restaurant:
        from django.http import Http404
        raise Http404("Restaurant not found")
    fixed_menu = next((fixed for fixed in FIXED_MENU.get(path, []) if fixed['id'] == meal), None)
    menu_item = get_object_or_404(MenuItem, id=meal) if fixed_menu is None else fixed_menu
    time = f"{menu_item.date[0:4]}.{menu_item.date[4:6]}.{menu_item.date[6:8]}" if fixed_menu is None else ''
    day = next((w['name'] for w in WEEKDAYS if w['day'] == menu_item.day), None) if fixed_menu is None else ('월~목' if path == 'ph' else '평일')
    meal = next((m['name'] for m in MEALS if m['time'] == menu_item.meal), None) if fixed_menu is None else ", ".join(m['name'] for tc in fixed_menu.get('time_category', []) for m in MEALS if m['time'] == tc)
    item_main = menu_item.safe_main if fixed_menu is None else menu_item['main']
    return render(request, 'pages/menu_detail.html', {'title': title, 'day': day, 'meal': meal, 'menu_item': menu_item, 'image_url': os.getenv('STORAGE_URL')+item_main, 'time': time, 'bases': bases, 'path': path})


# @staff_member_required
def admin_view(request):
    """Custom admin view for managing menu items"""
    items = MenuItem.objects.all()
    return render(request, 'pages/admin_view.html', {'items': items})
