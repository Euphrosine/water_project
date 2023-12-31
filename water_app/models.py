from django.db import models

class WaterData(models.Model):
    datetime = models.DateTimeField()
    water_tap = models.FloatField(max_length=20)
    turbidity_value = models.FloatField()
    turbidity_quality = models.CharField(max_length=20)
    ph_value = models.FloatField()
    ph_quality = models.CharField(max_length=20)
    result = models.CharField(max_length=20)

    def save(self, *args, **kwargs):
        # Determine turbidity quality
        if self.turbidity_value < 6:
            self.turbidity_quality = "Low"
        elif self.turbidity_value > 6:
            self.turbidity_quality = "High"
        else:
            self.turbidity_quality = "Invalid input"
        # Determine pH quality
        if 0 <= self.ph_value <= 6:
            self.ph_quality = "Alkalinity"
        elif self.ph_value == 7:
            self.ph_quality = "Neutral"
        else:
            self.ph_quality = "Acidic"

        # Determine overall result
        if self.turbidity_quality == "Low" and 7.9 >= self.ph_value >= 6.1 :
            self.result = "Clean"
        else:
            self.result = "Unclean"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Entry at {self.datetime}"
