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
MEALS = [{'id': 0, 'name': '아침', 'time': 'breakfast'}, {'id': 1, 'name': '점심', 'time': 'lunch'}, {'id': 2, 'name': '간식', 'time': 'snack'}, {'id': 3, 'name': '저녁', 'time': 'dinner'}, {'id': 4, 'name': 'One-Dish', 'time': 'onedish'}, {'id': 5, 'name': '무인판매', 'time': 'unmanned'}]
WEEKDAYS = [{'id': 0, 'name': '월', 'day': 'mon'}, {'id': 1, 'name': '화', 'day': 'tue'}, {'id': 2, 'name': '수', 'day': 'wed'}, {'id': 3, 'name': '목', 'day': 'thu'}, {'id': 4, 'name': '금', 'day': 'fri'}]
RESTAURANTS = [
    {'id': 1, 'title': '청운관 학생식당', 'campus': 'se', 'path': 'ch', 'mealsSemester': ['아침', '점심', '간식', '저녁'], 'mealsSemesterTime': ['08:30~10:00 (간편식: 09:00~10:00)', '11:00~14:30', '15:00~16:00', '17:00~18:30'], 'mealsVacation': ['점심']},
    {'id': 2, 'title': '청운관 교직원식당', 'campus': 'se', 'path': 'cg', 'mealsSemester': ['점심'], 'mealsVacation': ['점심'], 'mealsSemesterTime': ['11:30~14:00']},
    {'id': 3, 'title': '푸른솔 학생식당', 'campus': 'se', 'path': 'ph', 'mealsSemester': ['아침', '점심', 'One-Dish', '무인판매'], 'mealsVacation': ['아침', '점심'], 'mealsSemesterTime': ['08:30~10:00 (간편식: 09:00~10:00)', '11:00~14:30', '08:30~16:00', '14:30~소진시까지']},
    {'id': 4, 'title': '푸른솔 교직원식당', 'campus': 'se', 'path': 'pg', 'mealsSemester': ['점심'], 'mealsVacation': ['점심'], 'mealsSemesterTime': ['11:30~14:00']},
    {'id': 5, 'title': '한국외대 인문관 식당', 'campus': 'se', 'path': 'hi', 'mealsSemester': ['아침', '점심', '저녁'], 'mealsVacation': ['아침', '점심', '저녁'], 'mealsSemesterTime': ['08:30~10:00 (간편식: 09:00~10:00)', '11:00~14:30', '17:00~18:30']},
    {'id': 6, 'title': '한국외대 교수회관 식당', 'campus': 'se', 'path': 'hg', 'mealsSemester': ['점심'], 'mealsVacation': ['점심'], 'mealsSemesterTime': ['11:30~14:00']},
    {'id': 7, 'title': '학생회관 학생식당', 'campus': 'gl', 'path': 'hh', 'mealsSemester': ['아침', '점심', '저녁'], 'mealsVacation': ['아침', '점심', '저녁'], 'mealsSemesterTime': ['08:30~10:00 (간편식: 09:00~10:00)', '11:00~14:30', '17:00~18:30']},
    {'id': 8, 'title': '학생회관 교직원식당', 'campus': 'gl', 'path': 'hg', 'mealsSemester': ['점심'], 'mealsVacation': ['점심'], 'mealsSemesterTime': ['11:30~14:00']},
    {'id': 9, 'title': '제2기숙사 식당', 'campus': 'gl', 'path': 'jg', 'mealsSemester': ['아침', '점심', '저녁'], 'mealsVacation': ['아침', '점심', '저녁'], 'mealsSemesterTime': ['08:30~10:00 (간편식: 09:00~10:00)', '11:00~14:30', '17:00~18:30']},
]
LOCATIONS = {
    'ch': '청운관 학생식당',
    'cg': '청운관 교직원식당',
    'ph': '푸른솔 학생식당',
    'pg': '푸른솔 교직원식당',
    'hi': '한국외대 인문관 식당',
    'hg': '한국외대 교수회관 식당',
    'hh': '학생회관 학생식당',
    'hg': '학생회관 교직원식당',
    'jg': '제2기숙사 식당',
}
FIXED_MENU = {
    'ch' : [
        {
            'id': '만두라면,치즈라면-ch',
            'main': '만두라면, 치즈라면', 
            'enmain': 'Dumpling Ramen, Cheese Ramen',
            'side': None, 
            'enside': None,
            'price': 3000, 
            'day': None, 
            'time_category': ['breakfast', 'snack'], 
            'time_detail': {'breakfast': ['09:00', '10:00'], 'snack': ['15:00', '16:00']}, 
            'place': 'ch', 
            'extra': None,
            'enextra': None,
            'stamp': False,
        },
        {
            "id": "속풀이라면-ch",
            "main": "속풀이라면",
            "enmain": "Sokpul Ramen",
            "side": None,
            "enside": None,
            "price": 3500,
            "day": None,
            "time_category": ["breakfast"],
            "time_detail": {"breakfast": ["09:00", "10:00"]},
            "place": "ch",
            "extra": None,
            "enextra": None,
            "stamp": False,
        },
        {
            "id": '공깃밥-ch',
            "main": "공깃밥",
            "enmain": "Rice",
            "side": None,
            "enside": None,
            "price": 800,
            "day": None,
            "time_category": ["breakfast", "snack"],
            "time_detail": {"breakfast": ["09:00", "10:00"], "snack": ["15:00", "16:00"]},
            "place": "ch", 
            "extra": None,
            "enextra": None,
            "stamp": False,
        },
        {
            'id': '짜계치-ch',
            "main": "짜계치",
            "enmain": "Jja-gye-chi",
            "side": None,
            "enside": None,
            "price": 3800,
            "day": None,
            "time_category": ["snack"],
            "time_detail": {"snack": ["15:00", "16:00"]},
            "place": "ch",
            "extra": None,
            "enextra": None,
            "stamp": False,
        },
        {
            'id': '콘치즈불닭면-ch',
            "main": "콘치즈불닭면",
            "enmain": "Corn Cheese Buldak Noodles",
            "side": None,
            "enside": None,
            "price": 3800,
            "day": None,
            "time_category": ["snack"],
            "time_detail": {"snack": ["15:00", "16:00"]},
            "place": "ch",
            "extra": None,
            "enextra": None,
            "stamp": False,
        },
        {
            'id': '음료(콜라,사이다)-ch',
            "main": "음료(콜라,사이다)",
            "enmain": "Soft Drink (Cola, Cider)",
            "side": None,
            "enside": None,
            "price": 1700,
            "day": None,
            "time_category": ["breakfast"],
            "time_detail": {"breakfast": ["09:00", "10:00"]},
            "place": "ch",
            "extra": None,
            "enextra": None,
            "stamp": False,
        },
        {
            'id': '컵씨리얼&우유-ch',
            "main": "컵씨리얼&우유",
            "enmain": "Cup Cereal & Milk",
            "side": None,
            "enside": None,
            "price": 2000,
            "day": None,
            "time_category": ["breakfast"],
            "time_detail": {"breakfast": ["09:00", "10:00"]},
            "place": "ch",
            "extra": None,
            "enextra": None,
            "stamp": False,
        },
        {
            'id': '우유_딸기우유_초코우유-ch',
            "main": "우유/딸기우유/초코우유",
            "enmain": "Milk / Strawberry Milk / Choco Milk",
            "side": None,
            "enside": None,
            "price": 900,
            "day": None,
            "time_category": ["breakfast"],
            "time_detail": {"breakfast": ["09:00", "10:00"]},
            "place": "ch",
            "extra": None,
            "enextra": None,
            "stamp": False,
        },
    ],
    'ph' : [
        {
            'id': '주먹밥1EA-ph',
            'main': '주먹밥1EA',
            'enmain': 'Rice Ball 1EA',
            'side': None,
            'enside': None,
            'price': 1300,
            'day': None,
            'time_category': ['onedish'],
            'time_detail': {'onedish': ['08:30', '16:00']},
            'place': 'ph',
            'extra': None,
            'enextra': None,
            'stamp': False,
        },
        {
            'id': '주먹밥2EA-ph',
            'main': '주먹밥2EA',
            'enmain': 'Rice Ball 2EA',
            'side': None,
            'enside': None,
            'price': 2500,
            'day': None,
            'time_category': ['onedish', 'unmanned'],
            'time_detail': {'onedish': ['08:30', '16:00'], 'unmanned': ['16:30', '소진시까지']},
            'place': 'ph',
            'extra': None,
            'enextra': None,
            'stamp': False,
        },
        {
            'id': '공기밥-ph',
            'main': '공기밥',
            'enmain': 'Rice',
            'side': None,
            'enside': None,
            'price': 800,
            'day': None,
            'time_category': ['onedish'],
            'time_detail': {'onedish': ['08:30', '16:00']},
            'place': 'ph',
            'extra': None,
            'enextra': None,
            'stamp': False,
        },
        {
            'id': '씨리얼&우유-ph',
            'main': '씨리얼&우유',
            'enmain': 'Cereal & Milk',
            'side': None,
            'enside': None,
            'price': 2000,
            'day': None,
            'time_category': ['onedish'],
            'time_detail': {'onedish': ['08:30', '16:00']},
            'place': 'ph',
            'extra': None,
            'enextra': None,
            'stamp': False,
        },
        {
            'id': '우유-ph',
            'main': '우유',
            'enmain': 'Milk',
            'side': None,
            'enside': None,
            'price': 900,
            'day': None,
            'time_category': ['onedish'],
            'time_detail': {'onedish': ['08:30', '16:00']},
            'place': 'ph',
            'extra': None,
            'enextra': None,
            'stamp': False,
        },
        {
            'id': '탄산음료(콜라,사이다)-ph',
            'main': '탄산음료(콜라,사이다)',
            'enmain': 'Soda (Cola, Sprite)',
            'side': None,
            'enside': None,
            'price': 1700,
            'day': None,
            'time_category': ['onedish'],
            'time_detail': {'onedish': ['08:30', '16:00']},
            'place': 'ph',
            'extra': '토핑 대파쏭쏭 500 왕계란 500',
            'enextra': 'Topping Green Onion 500 King Egg 500',
            'stamp': False,
        },
        {
            'id': '진라면매운_안성탕면(셀프조리)-ph',
            'main': '진라면매운/안성탕면(셀프조리)',
            'enmain': 'Jin Ramen Spicy / Ansung Tangmyun (Self-cook)',
            'side': '김치/무맛김치/단무지/깍두기',
            'enside': 'Kimchi / Mild Kimchi / Pickled Radish / Cubed Radish Kimchi',
            'price': 2000,
            'day': None,
            'time_category': ['onedish'],
            'time_detail': {'onedish': ['08:30', '16:00']},
            'place': 'ph',
            'extra': '토핑 대파쏭쏭 500 왕계란 500',
            'enextra': 'Topping Green Onion 500 King Egg 500',
            'stamp': False,
        },
        {
            'id': '신라면(셀프조리)-ph',
            'main': '신라면(셀프조리)',
            'enmain': 'Shin Ramen (Self-cook)',
            'side': '김치/무맛김치/단무지/깍두기',
            'enside': 'Kimchi / Mild Kimchi / Pickled Radish / Cubed Radish Kimchi',
            'price': 2200,
            'day': None,
            'time_category': ['onedish'],
            'time_detail': {'onedish': ['08:30', '16:00']},
            'place': 'ph',
            'extra': '토핑 대파쏭쏭 500 왕계란 500',
            'enextra': 'Topping Green Onion 500 King Egg 500',
            'stamp': False,
        },
        {
            'id': '너구리_짜파게티(셀프조리)-ph',
            'main': '너구리/짜파게티(셀프조리)',
            'enmain': 'Neoguri / Jjapaghetti (Self-cook)',
            'side': '김치/무맛김치/단무지/깍두기',
            'enside': 'Kimchi / Mild Kimchi / Pickled Radish / Cubed Radish Kimchi',
            'price': 2300,
            'day': None,
            'time_category': ['onedish'],
            'time_detail': {'onedish': ['08:30', '16:00']},
            'place': 'ph',
            'extra': '토핑 대파쏭쏭 500 왕계란 500',
            'enextra': 'Topping Green Onion 500 King Egg 500',
            'stamp': False,
        },
        {
            'id': '오늘의컵밥-ph',
            'main': '오늘의컵밥',
            'enmain': "Today's Cup Rice",
            'side': None,
            'enside': None,
            'price': '2800~5000',
            'day': None,
            'time_category': ['unmanned'],
            'time_detail': {'unmanned': ['16:30', '소진시까지']},
            'place': 'ph',
            'extra': None,
            'enextra': None,
            'stamp': False,
        },
        {
            'id': '김밥-ph',
            'main': '김밥',
            'enmain': 'Gimbap',
            'side': None,
            'enside': None,
            'price': '3000~4000',
            'day': ['mon', 'tue', 'wed', 'thu'],
            'time_category': ['unmanned'],
            'time_detail': {'unmanned': ['16:30', '소진시까지']},
            'place': 'ph',
            'extra': None,
            'enextra': None,
            'stamp': False,
        },
        {
            'id': '소고기유부초밥-ph',
            'main': '소고기유부초밥',
            'enmain': 'Beef Inari Sushi',
            'side': None,
            'enside': None,
            'price': 2700,
            'day': ['mon', 'tue', 'wed', 'thu'],
            'time_category': ['unmanned'],
            'time_detail': {'unmanned': ['16:30', '소진시까지']},
            'place': 'ph',
            'extra': None,
            'enextra': None,
            'stamp': False,
        },
    ],
    'jj' : [
        {
            'id': '오늘의샐러드&드레싱-jj',
            'main': '오늘의샐러드&드레싱',
            'enmain': "Today's Salad & Dressing",
            'side': None,
            'enside': None,
            'price': 6500,
            'day': None,
            'time_category': ['breakfast'],
            'time_detail': {'breakfast': ['08:00', '10:00']},
            'place': 'jj',
            'extra': None,
            'enextra': None,
            'stamp': False,
        },
        {
            'id': '신라면_진라면매운맛_진라면순한맛_너구리_짜파게티_안성탕면_오징어짬뽕(셀프&토핑2종)-jj',
            'main': '신라면/진라면매운맛/진라면순한맛/너구리/짜파게티/안성탕면/오징어짬뽕(셀프&토핑2종)',
            'enmain': 'Shin Ramen / Jin Ramen Spicy / Jin Ramen Mild / Neoguri / Jjapaghetti / Ansung Tangmyun / Squid Jjambbong (Self & 2 Toppings)',
            'side': None,
            'enside': None,
            'price': None,
            'day': None,
            'time_category': ['breakfast', 'lunch', 'dinner'],
            'time_detail': {'breakfast': ['08:00', '10:00'], 'lunch': ['11:00', '14:00'], 'dinner': ['17:00', '18:30']},
            'place': 'jj',
            'extra': None,
            'enextra': None,
            'stamp': False,
        },
    ]
}

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
    time_to_meal = {'breakfast': [8, 9, 10], 'lunch': [11, 12, 13, 14], 'snack': [15, 16], 'dinner': [17, 18, 19], 'onedish': [8, 9, 10, 11, 12, 13, 14, 15, 16], 'unmanned': [14, 15, 16]}
    default_meal_name = next((m for m, hours in time_to_meal.items() if hour in hours and m in [meal['name'] for meal in MEALS]), 'breakfast')
    default_meal = request.GET.get('meal', default_meal_name)
    previous = request.GET.get('previous', 0)
    if 'day' not in request.GET or 'meal' not in request.GET:
        from django.shortcuts import redirect
        return redirect(request.path + f'?day={default_day}&meal={default_meal}&previous={previous}')
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
    previous = request.GET.get('previous', 0)
    
    # Only pass dishes for the selected meal into context
    all_dishes = FIXED_MENU.get(path, [])
    filtered_dishes = [
        d for d in all_dishes
        if selected_meal in d.get('time_category', [])
    ] if selected_meal else all_dishes
    from datetime import timedelta
    today = datetime.today()
    start_of_week = today - timedelta(days=today_idx) - timedelta(weeks=int(previous))
    week = [(start_of_week + timedelta(days=i)).strftime('%Y%m%d') for i in range(5)]
    week_without_year = [(start_of_week + timedelta(days=i)).strftime('%m.%d') for i in range(5)]
    selected_date = week[weekday_names.index(selected_day)]
    db_qs = MenuItem.objects.filter(place=path, meal=selected_meal, day=selected_day, date=selected_date)
    filtered_dishes = list(db_qs) + filtered_dishes


    tabs = []
    for i, w in enumerate(WEEKDAYS):
        t = dict(w)
        t['date'] = week_without_year[i]
        tabs.append(t)

    return render(request, 'pages/menu_list.html', {
        'tabs': tabs,
        'restaurant': {'title': title, 'meal_tabs': meal_tabs, 'path': path},
        'selected_meal': selected_meal,
        'selected_day': selected_day,
        'menu': filtered_dishes,
        'bases': bases,
        'path': path,
        'week': week,
        'previous': previous,
    })


def menu_detail(request, path, meal, bases):
    """Display details for a specific menu item"""
    # menu_item = get_object_or_404(MenuItem, url=path)
    # menu_item = {'title': path, 'meal': meal, 'order': 0}
    location = next((r for r in RESTAURANTS if r['path'] == path), None)
    if not location:
        from django.http import Http404
        raise Http404("Restaurant not found")
    menu_item = get_object_or_404(MenuItem, id=meal)
    lang = 'ko' if request.LANGUAGE_CODE == 'ko' else 'en'
    time = f"{menu_item.date[0:4]}-{menu_item.date[4:6]}-{menu_item.date[6:8]} {menu_item.day} {menu_item.meal}"
    return render(request, 'pages/menu_detail.html', {'menu_item': menu_item, 'image_url': 'https://objectstorage.ap-chuncheon-1.oraclecloud.com/n/ax0ym4amgnfk/b/bucket-20260516-0145/o/'+menu_item.main+'.png', 'time': time, 'bases': bases, 'path': path, 'meal': meal, 'lang': lang})


# @staff_member_required
def admin_view(request):
    """Custom admin view for managing menu items"""
    items = MenuItem.objects.all()
    return render(request, 'pages/admin_view.html', {'items': items})
