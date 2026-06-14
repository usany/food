from datetime import datetime
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from .models import MenuItem

# RESTAURANT_TITLES = {
#     'ph': '푸른솔 학생식당',
#     'pg': '푸른솔 교직원식당',
#     'ch': '청운관 학생식당',
#     'cg': '청운관 교직원식당',
#     'hi': '한국외대 인문관 식당',
#     'hg': '한국외대 교수회관 식당',
#     'hh': '학생회관 학생식당',
#     'jg': '제2기숙사 식당',
# }
from .constants import MEALS, WEEKDAYS, RESTAURANTS, FIXED_MENU

# def _restaurants_for_campus(campus):
#     return [r for r in RESTAURANTS if r['campus'] == campus]


# def _restaurant_dict_by_path(path):
#     for r in RESTAURANTS:
#         if r['path'] == path:
#             return r
#     return None


def root_redirect(request):
    """Redirect to /gl or /se based on localStorage"""
    html = """<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body>
<script>
  const lang = localStorage.getItem('base')
  const loc = localStorage.getItem('bases');
  if (lang === 'en') {
    if (loc === 'gl') {
        window.location.replace('en/gl/');
    } else {
        window.location.replace('en/se/');
    }
  } else {
    if (loc === 'gl') {
        window.location.replace('ko/gl/');
    } else {
        window.location.replace('ko/se/');
    }
  }
</script>
</body>
</html>"""
    return HttpResponse(html)


def home_menu(request, bases):
    restaurants_items = [r for r in RESTAURANTS if r['campus'] == bases]
    return render(request, 'pages/home.html', {'items': restaurants_items, 'location': bases, 'bases': bases})

def menu_list(request, path, bases):
    """Display menu items for the restaurant selected on the home page."""
    r = next((r for r in RESTAURANTS if r['path'] == path), None)
    if not r:
        from django.http import Http404
        raise Http404("Restaurant not found")
    title = r['title']
    all_meals = r['mealsSemester']
    weekday_names = ['mon', 'tue', 'wed', 'thu', 'fri']
    today_idx = datetime.today().weekday()
    default_day = request.GET.get('day', weekday_names[today_idx] if today_idx < 5 else 'mon')
    hour = datetime.now().hour
    time_to_meal = {'breakfast': [8, 9, 10], 'lunch': [11, 12, 13, 14], 'snack': [15, 16], 'dinner': [17, 18, 19]}
    default_meal_name = next((m for m, hours in time_to_meal.items() if hour in hours), 'breakfast')
    default_meal = request.GET.get('meal', default_meal_name)
    if 'day' not in request.GET or 'meal' not in request.GET:
        from django.shortcuts import redirect
        return redirect(request.path + f'?day={default_day}&meal={default_meal}')
    weekdays = [d for d in WEEKDAYS if d['day'] == default_day]
    meal_tabs = [
        {
            'id': next((meal['time'] for meal in MEALS if meal['name'] == m), None),
            'label': m,
            'meal_time': r['mealsSemesterTime'][r['mealsSemester'].index(m)]
        }
        for m in all_meals
    ]

    # State: which meal tab is active — read from GET param, default to first
    selected_meal = request.GET.get('meal', meal_tabs[0]['id'] if meal_tabs else None)
    selected_day = request.GET.get('day', weekdays[0]['day'] if weekdays else None)

    # Only pass dishes for the selected meal into context
    all_dishes = FIXED_MENU.get(path, [])
    filtered_dishes = [
        d for d in all_dishes
        if selected_meal in d.get('time_category', [])
    ] if selected_meal else all_dishes
    db_qs = MenuItem.objects.filter(place=path, meal=selected_meal, day=selected_day)
    filtered_dishes = list(db_qs) + filtered_dishes


    tabs = list(WEEKDAYS)

    return render(request, 'pages/menu_list.html', {
        'tabs': tabs,
        'restaurant': {'title': title, 'meal_tabs': meal_tabs, 'path': path},
        'selected_meal': selected_meal,
        'selected_day': selected_day,
        'menu': filtered_dishes,
        'bases': bases,
        'path': path
    })


def menu_detail(request, path, meal, bases):
    """Display details for a specific menu item"""
    # menu_item = get_object_or_404(MenuItem, url=path)
    # menu_item = {'title': path, 'meal': meal, 'order': 0}
    location = next((r for r in RESTAURANTS if r['path'] == path), None)
    if not location:
        from django.http import Http404
        raise Http404("Restaurant not found")
    location = location['title']
    menu_item = get_object_or_404(MenuItem, id=meal)
    time = f"{menu_item.date[0:4]}-{menu_item.date[4:6]}-{menu_item.date[6:8]} {menu_item.day} {menu_item.meal}"
    return render(request, 'pages/menu_detail.html', {'menu_item': menu_item, 'image_url': 'https://objectstorage.ap-chuncheon-1.oraclecloud.com/n/ax0ym4amgnfk/b/bucket-20260516-0145/o/'+menu_item.main+'.png', 'time': time, 'bases': bases, 'path': path, 'meal': meal})


# @staff_member_required
def admin_view(request):
    """Custom admin view for managing menu items"""
    items = MenuItem.objects.all()
    return render(request, 'pages/admin_view.html', {'items': items})
