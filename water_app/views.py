from django.shortcuts import render
from django.http import JsonResponse
from .models import WaterData
from datetime import datetime
from django.db.models import Count
import json


def water_data_api(request):
    turbidity_value = request.GET.get('turbidity_value', None)
    ph_value = request.GET.get('ph_value', None)

    if turbidity_value is not None and ph_value is not None:
        turbidity_value = float(turbidity_value)
        ph_value = float(ph_value)

        turbidity_quality = None
        ph_quality = None
        result = None

        if turbidity_value <= 5:
            turbidity_quality = "Low"
        elif 6 <= turbidity_value <= 25:
            turbidity_quality = "Medium"
        else:
            turbidity_quality = "High"

        if 0 <= ph_value <= 6:
            ph_quality = "Alkalinity"
        elif ph_value == 7:
            ph_quality = "Neutral"
        else:
            ph_quality = "Acidic"

        if turbidity_quality == "Low" and  (ph_quality == "Alkalinity" or ph_quality == "Neutral"):
            result = "Clean"
        else:
            result = "Unclean"
        
        print(f"Result: {result}")
        water_data = WaterData.objects.create(
            datetime=datetime.now(),
            turbidity_value=turbidity_value,
            turbidity_quality=turbidity_quality,
            ph_value=ph_value,
            ph_quality=ph_quality,
            result=result
        )


        return JsonResponse({'message': 'Data received successfully', 'context': {'ph_value': ph_value, 'turbidity_value': turbidity_value, 'turbidity_quality': turbidity_quality, 'ph_quality': ph_quality, 'result': result}})
    else:
        return JsonResponse({'error': 'Invalid request. turbidity_value or ph_value parameter is missing or not valid.'}, status=400)



def water_data_view(request):
    # Retrieve the necessary data from the database
    data = WaterData.objects.all()

    # Calculate counts of clean and unclean water entries
    clean_water_count = data.filter(result='Clean').count()
    unclean_water_count = data.filter(result='Unclean').count()

    # Retrieve cleanliness data for the chart (clean_data and unclean_data)
    # Calculate clean and unclean data
    # clean_data, unclean_data = get_cleanliness_data()

    context = {
        'data': data,
        'clean_water_count': clean_water_count,
        'unclean_water_count': unclean_water_count,

    }

    return render(request, 'water_app/main.html', context)
