from django.core.management.base import BaseCommand
import os
import random
from dotenv import load_dotenv
import requests
import re

MENU_ITEMS = {
    'ch': [
        {
            'id': '만두라면,치즈라면-ch',
            'main': '만두라면, 치즈라면', 
            'enmain': 'Dumpling Ramen, Cheese Ramen',
        },
        {
            "id": "속풀이라면-ch",
            "main": "속풀이라면",
            "enmain": "Sokpul Ramen",
        },
        {
            "id": '공깃밥-ch',
            "main": "공깃밥",
            "enmain": "Rice",
        },
        {
            'id': '짜계치-ch',
            "main": "짜계치",
            "enmain": "Jja-gye-chi",
        },
        {
            'id': '콘치즈불닭면-ch',
            "main": "콘치즈불닭면",
            "enmain": "Corn Cheese Buldak Noodles",
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
            'id': '우유/딸기우유/초코우유-ch',
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
    'ph': [
        {
            'id': '주먹밥1EA-ph',
            'main': '주먹밥1EA',
            'enmain': 'Rice Ball 1EA',
        },
        {
            'id': '주먹밥2EA-ph',
            'main': '주먹밥2EA',
            'enmain': 'Rice Ball 2EA',
        },
        {
            'id': '공기밥-ph',
            'main': '공기밥',
            'enmain': 'Rice',
        },
        {
            'id': '씨리얼&우유-ph',
            'main': '씨리얼&우유',
            'enmain': 'Cereal & Milk',
        },
        {
            'id': '우유-ph',
            'main': '우유',
            'enmain': 'Milk',
        },
        {
            'id': '탄산음료(콜라,사이다)-ph',
            'main': '탄산음료(콜라,사이다)',
            'enmain': 'Soda (Cola, Sprite)',
        },
        {
            'id': '진라면매운/안성탕면(셀프조리)-ph',
            'main': '진라면매운/안성탕면(셀프조리)',
            'enmain': 'Jin Ramen Spicy / Ansung Tangmyun (Self-cook)',
        },
        {
            'id': '신라면(셀프조리)-ph',
            'main': '신라면(셀프조리)',
            'enmain': 'Shin Ramen (Self-cook)',
        },
        {
            'id': '너구리/짜파게티(셀프조리)-ph',
            'main': '너구리/짜파게티(셀프조리)',
            'enmain': 'Neoguri / Jjapaghetti (Self-cook)',
        },
        {
            'id': '오늘의컵밥-ph',
            'main': '오늘의컵밥',
            'enmain': "Today's Cup Rice",
        },
        {
            'id': '김밥-ph',
            'main': '김밥',
            'enmain': 'Gimbap',
        },
        {
            'id': '소고기유부초밥-ph',
            'main': '소고기유부초밥',
            'enmain': 'Beef Inari Sushi',
        },
    ],
    'jj': [
        {
            'id': '오늘의샐러드&드레싱-jj',
            'main': '오늘의샐러드&드레싱',
            'enmain': "Today's Salad & Dressing",
        },
        {
            'id': '신라면/진라면매운맛/진라면순한맛/너구리/짜파게티/안성탕면/오징어짬뽕(셀프&토핑2종)-jj',
            'main': '신라면/진라면매운맛/진라면순한맛/너구리/짜파게티/안성탕면/오징어짬뽕(셀프&토핑2종)',
            'enmain': 'Shin Ramen / Jin Ramen Spicy / Jin Ramen Mild / Neoguri / Jjapaghetti / Ansung Tangmyun / Squid Jjambbong (Self & 2 Toppings)',
        },
    ],
}


class Command(BaseCommand):
    help = 'Generate images for ph and jj fixed menu items'

    def add_arguments(self, parser):
        parser.add_argument(
            '--place',
            type=str,
            choices=['ph', 'jj', 'all'],
            default='all',
            help='Which place to generate images for: ph, jj, or all (default: all)',
        )

    def handle(self, *args, **options):
        place = options.get('place', 'all')

        if place == 'all':
            places = ['ph', 'jj']
        else:
            places = [place]

        for p in places:
            items = MENU_ITEMS.get(p, [])
            self.stdout.write(self.style.NOTICE(f'Generating images for {p} ({len(items)} items)...'))
            for item in items:
                main = item['main']
                enmain = item['enmain']
                self.stdout.write(f'  Generating: {main} ({enmain})')
                self.generate_image(main, enmain)
            self.stdout.write(self.style.SUCCESS(f'Done with {p}.'))

        self.stdout.write(self.style.SUCCESS('All image generation complete.'))

    def generate_image(self, main, enmain):
        """Generate an image using Cloudflare AI API"""
        load_dotenv()
        account_id = os.getenv('CFACCOUNTID')
        api_token = os.getenv('CFAPITOKEN')

        if not account_id or not api_token:
            self.stderr.write(self.style.ERROR('Cloudflare credentials not found in environment variables.'))
            return

        # Step 1: Use the English dish name directly
        translated_text = enmain

        # Step 2: Generate image using translated text
        imageurl = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/@cf/bytedance/stable-diffusion-xl-lightning"
        headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json",
        }

        image_prompt = f"Create a picture of single {translated_text} dish in a fancy restaurant"
        image_payload = {
            "prompt": image_prompt,
            "seed": random.randint(0, 1000000),
        }

        # Sanitize filename: remove characters invalid on Windows
        safe_main = re.sub(r'[\\/*?:"<>|]', '+', main)

        try:
            image_response = requests.post(imageurl, headers=headers, json=image_payload)

            if image_response.status_code == 200:
                with open(f"{safe_main}.png", "wb") as f:
                    f.write(image_response.content)
                self.stdout.write(self.style.SUCCESS(f"Image saved as {safe_main}.png"))
                self.upload_to_storage(f"{safe_main}.png", f"{main}.png")
            else:
                self.stderr.write(self.style.ERROR(f"Image generation API error: {image_response.status_code} {image_response.text}"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error generating image: {str(e)}"))

    def upload_to_storage(self, file_path, object_name):
        """Upload image to storage using PUT with PAR token"""
        load_dotenv()

        url = f"https://objectstorage.ap-chuncheon-1.oraclecloud.com/p/_jTGcQoC5j9SBp5Q9iVJ4U7y0oilMttgFhVFrPo90gFeMwUn2JQVeAjTQetS6HNh/n/ax0ym4amgnfk/b/bucket-20260516-0145/o/{object_name}"
        if not os.path.exists(file_path):
            self.stderr.write(self.style.ERROR(f'File not found: {file_path}'))
            return

        try:
            with open(file_path, 'rb') as f:
                file_data = f.read()
                response = requests.put(url, data=file_data, timeout=10)

            if response.status_code in [200, 201]:
                self.stdout.write(self.style.SUCCESS(f'Successfully uploaded {file_path} to storage'))
            else:
                self.stderr.write(self.style.ERROR(f'Failed to upload: {response.status_code} {response.text}'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error uploading to storage: {str(e)}'))
