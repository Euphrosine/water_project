from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime
from .models import WaterData
from django.contrib.auth.decorators import login_required

def water_data_api(request):
    # Assuming 'status' and 'ph_value' are passed in the request
    ph_value = request.GET.get('ph_value', None)

    if ph_value is not None:
        ph_value = int(ph_value)  # Convert ph_value to a float

        if ph_value > 30:
            quality = "Clean Water"
        elif ph_value < 29:
            quality = "Unclean Water"
        else:
            quality = ""  # Set a default quality if neither condition is met

        water_data = WaterData.objects.create(datetime=datetime.now(), ph_value=ph_value, quality=quality)

        return JsonResponse({'message': 'Data received successfully', 'context': {'ph_value': ph_value, 'quality': quality}})
    else:
        return JsonResponse({'error': 'Invalid request. ph_value parameter is missing or not valid.'}, status=400)


@login_required
def water_data_view(request):
    latest_entry = WaterData.objects.latest('datetime')
    ph_value = latest_entry.ph_value  # Corrected line
    quality = latest_entry.quality  # Corrected line

    return render(request, 'water_app/schair_data_view.html', {'ph_value': ph_value, 'quality': quality})

def update_data(request):
    latest_entry = WaterData.objects.latest('datetime')
    ph_value = latest_entry.ph_value  # Corrected line
    quality = latest_entry.quality  # Corrected line

    return JsonResponse({'ph_value': ph_value, 'quality': quality})

