from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
from bs4 import BeautifulSoup
import re
import html
# Create your views here.

def main(request):
    
    return render(request,"main/main.html",{});
@csrf_exempt
def panel(request):
    if request.method != 'POST':
        return render(request,"panel/panel.html")

    url = request.POST.get('url')
    if not url:
        return JsonResponse({'status': 'error', 'message': 'لینک محصول وارد نشده است'}, status=400)

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = response.apparent_encoding or 'utf-8'
  # برای پشتیبانی بهتر از فارسی
        print(response.text[:1000])  # برای مشاهده‌ی پیش‌نمایش فارسی

        if response.status_code != 200:
            return JsonResponse({'status': 'error', 'message': f'خطا در دریافت محتوا: {response.status_code}'}, status=500)

        soup = BeautifulSoup(response.text, 'html.parser')

        # 🏷️ استخراج عنوان
        def extract_title():
            tag = soup.find("meta", property="og:title") or soup.find("title") or soup.find("h1")
            if tag:
                return tag.get("content") if tag.has_attr("content") else tag.get_text(strip=True)
            return None

        # 🖼️ استخراج تصویر
        def extract_image():
            tag = soup.find("meta", property="og:image") or soup.find("img")
            if tag:
                return tag.get("content") if tag.has_attr("content") else tag.get("src")
            return None

        # 💰 استخراج قیمت
        def extract_price():
            price_tags = soup.find_all(text=re.compile(r'\d[\d\.,]*\s?(تومان|ریال|﷼|\$|€|₺)', flags=re.UNICODE))
            for tag in price_tags:
                text = tag.strip()
                clean_text = html.unescape(text)
                return clean_text
            return None

        result = {
            'title': extract_title(),
            'image': extract_image(),
            'price': extract_price(),
            'url': url
        }

        return render(request, "panel/panel_result.html", result)

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'خطا: {str(e)}'}, status=500)