import requests
from django.shortcuts import render
from .models import MonitorResult

def index(request):
    # List of websites to monitor
    targets = [
        "https://google.com",
        "https://youtube.com",
        "https://microsoft.com",
        "https://www.apple.com",  
        "https://store.steampowered.com",
        "https://github.com",
        "https://stackoverflow.com",
        "https://archlinux.org"

    ]

    results_data = []

    for url in targets:
        # Website check
        try:
            response = requests.get(url, timeout=3)  # 3-second timeout
            status_code = response.status_code
            is_up = status_code == 200
            response_time = response.elapsed.total_seconds()
        except Exception:
            status_code = 0
            is_up = False
            response_time = 0.0

        # Saving to the database
        MonitorResult.objects.create(
            url=url,
            status=status_code,
            response_time=response_time,
            is_up=is_up
        )

        # Fetching history (last 5 records)
        history = MonitorResult.objects.filter(url=url).order_by('-timestamp')[:5]

        # Preparing data for the template
        site_info = {
            'url': url,
            'is_up': is_up,
            'status_code': status_code,
            'response_time': f"{response_time:.6f}",
            'history': history
        }
        results_data.append(site_info)

    return render(request, 'monitoring/index.html', {
        'sites': results_data
    })
