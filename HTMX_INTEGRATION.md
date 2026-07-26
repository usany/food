# HTMX Integration Guide

This project now uses HTMX for seamless partial page re-rendering without full page reloads.

## What's Implemented

### Dynamic Components
The menu list page now updates smoothly when users interact with:
- **Day tabs** - Switch between weekdays
- **Meal tabs** - Switch between breakfast/lunch/dinner/etc.
- **Week navigation** - Navigate between weeks

### How It Works

Each interaction triggers an HTMX request that:
1. Sends the current filters (day, meal, week) to the server
2. Receives only the updated HTML fragment
3. Swaps the relevant section without a full page reload
4. Preserves URL with `hx-push-url` (browser history support)
5. Re-initializes icons with lucide.js after swap

## Component Files

### Templates
- `templates/pages/menu_list.html` - Main menu page (now uses components)
- `templates/components/menu_panel.html` - Meals list + meal tabs
- `templates/components/week_nav.html` - Week navigation arrows
- `templates/components/day_tabs.html` - Day tabs

### Views (in `restaurants/views.py`)
- `menu_panel_fragment()` - Returns menu items + meal tabs for selected day
- `week_nav_fragment()` - Returns week navigation
- `day_tabs_fragment()` - Returns day tabs

### URLs (in `restaurants/urls.py`)
- `/<lang>/<bases>/<path>/api/menu-panel/` - Menu panel endpoint
- `/<lang>/<bases>/<path>/api/week-nav/` - Week nav endpoint
- `/<lang>/<bases>/<path>/api/day-tabs/` - Day tabs endpoint

## HTMX Attributes Used

### `hx-get`
```html
<a hx-get="?day=mon&meal=lunch">Load content</a>
```
Sends GET request to URL.

### `hx-target`
```html
hx-target="#menu-panel"
```
Specifies which element to update with the response.

### `hx-swap`
```html
hx-swap="innerHTML"
```
How to insert the response (innerHTML, outerHTML, beforeBegin, etc.)

### `hx-push-url`
```html
hx-push-url="?day=mon&meal=lunch"
```
Updates browser URL and history without reloading page.

## JavaScript Integration

After each HTMX swap, icons are re-initialized:
```javascript
document.addEventListener('htmx:afterSwap', function(event) {
    if (window.lucide) {
        lucide.createIcons();
    }
});
```

This ensures lucide icons render properly after content updates.

## Query Parameters

The following query parameters control the menu display:
- `day` - Selected weekday (mon, tue, wed, thu, fri)
- `meal` - Selected meal time (breakfast, lunch, dinner, etc.)
- `previous` - Week offset (0 = current week, 1 = next week)

Example: `?day=mon&meal=lunch&previous=0`

## Performance Benefits

1. **Reduced Data Transfer** - Only HTML fragments are sent, not entire page
2. **Smooth UX** - No flash/blink on content update
3. **Preserves State** - Scroll position maintained, page state preserved
4. **SEO Friendly** - Full page reloads available via normal navigation
5. **Graceful Degradation** - Works without JavaScript for regular links

## How to Extend

To add more HTMX endpoints:

1. **Create a view fragment function** in `views.py`:
```python
def my_fragment(request, path, bases):
    data = {...}
    return render(request, 'components/my_component.html', data)
```

2. **Add URL endpoint** in `urls.py`:
```python
path('<str:bases>/<str:path>/api/my-fragment/', views.my_fragment, name='my_fragment'),
```

3. **Use in template** with HTMX attributes:
```html
<button hx-get="{% url 'my_fragment' bases=bases path=path %}" hx-target="#target">
    Click me
</button>
```

## Testing HTMX Requests

To test HTMX endpoints directly (they return fragments, not full pages):

```bash
# Test menu panel
curl "http://localhost:8000/ko/se/ch/api/menu-panel/?day=mon&meal=lunch"

# Test week nav
curl "http://localhost:8000/ko/se/ch/api/week-nav/?day=mon&previous=0"
```

## Browser Support

HTMX works in all modern browsers. The project gracefully degrades with fallback links for older browsers.
