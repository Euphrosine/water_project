from django.shortcuts import render
from django.http import JsonResponse
from .models import WaterData
from datetime import datetime
from django.db.models import Count
import json
from django.contrib.auth.decorators import login_required


from datetime import datetime
from .models import WaterData


from django.http import JsonResponse
from datetime import datetime  # Add this import if not already imported
from .models import WaterData  # Import the WaterData model from your app

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

        if turbidity_value < 6:
            turbidity_quality = "Low"
        elif turbidity_value > 6:
            turbidity_quality = "High"
        else:
            turbidity_quality = "Invalid input"

        if 0 <= ph_value <= 6:
            ph_quality = "Alkalinity"
        elif ph_value == 7:
            ph_quality = "Neutral"
        else:
            ph_quality = "Acidic"

        if turbidity_quality == "Low" and 7.9 >= ph_value >= 6.1:
            result = "Clean"
        else:
            result = "Dirty"

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
    unclean_water_count = data.filter(result='Dirty').count()



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


from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def generate_pdf_report(request):
    # Assuming you have Django models for each category
    weather_data = WaterData.objects.all()

    # Create a PDF document
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="System_report.pdf"'
    p = canvas.Canvas(response, pagesize=letter)

    def draw_section(title, data, y_start):
        p.setFont("Helvetica-Bold", 18)
        p.drawCentredString(300, y_start, title)

        p.setFont("Helvetica", 12)
        p.drawCentredString(300, y_start - 20, "-" * 50)

        records_per_page = 25
        for i, item in enumerate(data):
            # Calculate the starting y coordinate for each record
            record_y_start = y_start - 40 - (i % records_per_page) * 20

            # Start a new page for each section or after 25 records
            if i % records_per_page == 0 and i != 0:
                p.showPage()
                p.setFont("Helvetica-Bold", 18)
                p.drawCentredString(300, 770, f"{title} (continued)")
                p.setFont("Helvetica", 12)
                y_start = 780  # Reset y_start for the new page

            p.drawString(70, record_y_start, f"Record {i + 1}: {item.datetime}, {item.water_tap}, {item.turbidity_value}, {item.turbidity_quality}, {item.ph_value}, {item.ph_quality}, {item.result}")

    # Set an initial y_start value
    draw_section("Smart Water Monitoring System for Community Water Wells", weather_data, 770)

    # Save the PDF
    p.showPage()
    p.save()

    return response





def generate_chart_data_report_view(request):
    sensor_data = WaterData.objects.all()
    pdf_response = generate_pdf_report(sensor_data)
    return pdf_response
