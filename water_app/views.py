from django.shortcuts import render
from django.http import JsonResponse
from .models import WaterData
from datetime import datetime
from django.db.models import Count
import json
from django.contrib.auth.decorators import login_required


from datetime import datetime
from .models import WaterData

def water_data_api(request):
    turbidity_value = request.GET.get('turbidity_value', None)
    ph_value = request.GET.get('ph_value', None)
    water_tap = request.GET.get('water_tap', None)

    if turbidity_value is not None and ph_value is not None and water_tap is not None:
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

        if turbidity_quality == "Low" and (ph_quality == "Alkalinity" or ph_quality == "Neutral"):
            result = "Clean"
        else:
            result = "Unclean"

        print(f"Result: {result}")

        # Include water_tap in WaterData creation
        water_data = WaterData.objects.create(
            datetime=datetime.now(),
            water_tap=water_tap,
            turbidity_value=turbidity_value,
            turbidity_quality=turbidity_quality,
            ph_value=ph_value,
            ph_quality=ph_quality,
            result=result
        )

        return JsonResponse({'message': 'Data received successfully', 'result': result})
    else:
        return JsonResponse({'error': 'Invalid request. Required parameters are missing.'}, status=400)


@login_required
def water_data_view(request):
    # Retrieve the necessary data from the database
    data = WaterData.objects.all()
   

    # Calculate counts of clean and unclean water entries
    clean_water_count = data.filter(result='Clean').count()
    unclean_water_count = data.filter(result='Unclean').count()



    context = {
        'data': data,
        'clean_water_count': clean_water_count,
        'unclean_water_count': unclean_water_count,

    }

    return render(request, 'water_app/main.html', context)

# chart2
def chart_data(request):
    data = WaterData.objects.values('datetime', 'turbidity_value', 'ph_value')
    return JsonResponse(list(data), safe=False)

from django.shortcuts import render

def taps_table(request):
    table_data = WaterData.objects.all()
    return render(request, 'water_app/water-taps.html', {'table_data':table_data})
