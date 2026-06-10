import os

# Create locale directories
os.makedirs('locale\\en\\LC_MESSAGES', exist_ok=True)
os.makedirs('locale\\ko\\LC_MESSAGES', exist_ok=True)

# Create English translation file
en_content = '''# English translations for restaurants project.
# Copyright (C) 2026
# This file is distributed under the same license as the restaurants project.
#
msgid ""
msgstr ""
"Project-Id-Version: restaurants\\n"
"Report-Msgid-Bugs-To: \\n"
"POT-Creation-Date: 2026-06-10 16:37+0000\\n"
"PO-Revision-Date: 2026-06-10 16:37+0000\\n"
"Last-Translator: \\n"
"Language-Team: English\\n"
"Language: en\\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=UTF-8\\n"
"Content-Transfer-Encoding: 8bit\\n"

#: restaurants/templates/base.html:8
msgid "App"
msgstr "App"

#: restaurants/templates/base.html:31
msgid "Switch campus"
msgstr "Switch campus"

#: restaurants/templates/base.html:32
msgid "campus"
msgstr "campus"

#: restaurants/templates/base.html:35
msgid "Switch language"
msgstr "Switch language"

#: restaurants/templates/base.html:36
msgid "language"
msgstr "language"

#: restaurants/templates/base.html:40
msgid "Toggle dark mode"
msgstr "Toggle dark mode"

#: restaurants/templates/base.html:41
msgid "theme"
msgstr "theme"

#: restaurants/templates/base.html:53
msgid "Home"
msgstr "Home"

#: restaurants/templates/base.html:61
msgid "Menus"
msgstr "Menus"

#: restaurants/templates/pages/home.html:7
msgid "Welcome to restaurants"
msgstr "Welcome to restaurants"

#: restaurants/templates/pages/home.html:22
msgid "This is the main page."
msgstr "This is the main page."

#: restaurants/templates/pages/menu_list.html:7
msgid "Back"
msgstr "Back"

#: restaurants/templates/pages/menu_list.html:77
msgid "No menu available for this time."
msgstr "No menu available for this time."

#: restaurants/templates/pages/menu_detail.html:14
msgid "No image available"
msgstr "No image available"

#: restaurants/templates/pages/menu_detail.html:53
msgid "No pork"
msgstr "No pork"
'''

# Create Korean translation file
ko_content = '''# Korean translations for restaurants project.
# Copyright (C) 2026
# This file is distributed under the same license as the restaurants project.
#
msgid ""
msgstr ""
"Project-Id-Version: restaurants\\n"
"Report-Msgid-Bugs-To: \\n"
"POT-Creation-Date: 2026-06-10 16:37+0000\\n"
"PO-Revision-Date: 2026-06-10 16:37+0000\\n"
"Last-Translator: \\n"
"Language-Team: Korean\\n"
"Language: ko\\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=UTF-8\\n"
"Content-Transfer-Encoding: 8bit\\n"

#: restaurants/templates/base.html:8
msgid "App"
msgstr "앱"

#: restaurants/templates/base.html:31
msgid "Switch campus"
msgstr "캠퍼스 전환"

#: restaurants/templates/base.html:32
msgid "campus"
msgstr "캠퍼스"

#: restaurants/templates/base.html:35
msgid "Switch language"
msgstr "언어 전환"

#: restaurants/templates/base.html:36
msgid "language"
msgstr "언어"

#: restaurants/templates/base.html:40
msgid "Toggle dark mode"
msgstr "다크 모드 전환"

#: restaurants/templates/base.html:41
msgid "theme"
msgstr "테마"

#: restaurants/templates/base.html:53
msgid "Home"
msgstr "홈"

#: restaurants/templates/base.html:61
msgid "Menus"
msgstr "메뉴"

#: restaurants/templates/pages/home.html:7
msgid "Welcome to restaurants"
msgstr "맛집에 오신 것을 환영합니다"

#: restaurants/templates/pages/home.html:22
msgid "This is the main page."
msgstr "이것은 메인 페이지입니다."

#: restaurants/templates/pages/menu_list.html:7
msgid "Back"
msgstr "뒤로"

#: restaurants/templates/pages/menu_list.html:77
msgid "No menu available for this time."
msgstr "이 시간대 메뉴가 없습니다."

#: restaurants/templates/pages/menu_detail.html:14
msgid "No image available"
msgstr "이용 가능한 이미지가 없습니다."

#: restaurants/templates/pages/menu_detail.html:53
msgid "No pork"
msgstr "돼지 없음"
'''

with open('locale\\en\\LC_MESSAGES\\django.po', 'w', encoding='utf-8') as f:
    f.write(en_content)

with open('locale\\ko\\LC_MESSAGES\\django.po', 'w', encoding='utf-8') as f:
    f.write(ko_content)

print("Translation files created successfully!")
