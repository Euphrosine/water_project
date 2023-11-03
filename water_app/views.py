from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime
from .models import WaterData
from django.contrib.auth.decorators import login_required

def water_data_api(request):
    # Assuming 'status' is passed in the request
    status = request.GET.get('status', None)

    if status is not None:
        if status == '1':
            status_type = "1"
            quality = "Clean Water"
        elif status == '2':
            status_type = "2"
            quality = "Unclean Water"
        else:
            status_type = ""
            quality = ""


        water_data = WaterData.objects.create(datetime=datetime.now(), status_type=status_type,quality=quality)
        

        return JsonResponse({'message': 'Data received successfully', 'context': {'status_type': status_type, 'quality': quality}})
    else:
        return JsonResponse({'error': 'Invalid request. Status parameter is missing.'}, status=400)


@login_required
def water_data_view(request):
    latest_entry = WaterData.objects.latest('datetime')
    status_type = latest_entry.status_type  # Corrected line
    quality = latest_entry.quality  # Corrected line

    return render(request, 'water_app/schair_data_view.html', {'status_type': status_type, 'quality': quality})

def update_data(request):
    latest_entry = WaterData.objects.latest('datetime')
    status_type = latest_entry.status_type  # Corrected line
    quality = latest_entry.quality  # Corrected line

    return JsonResponse({'status_type': status_type, 'quality': quality})

