from django.db import models

# Create your models here.

def subir_imagen(instance, filename):
    return f"predicciones/{instance.fecha}/{filename}"


class Prediccion(models.Model):
    imagen = models.ImageField(upload_to=subir_imagen, null=True, blank=True)
    fecha = models.DateField(auto_now_add=True)
    prediccion = models.IntegerField(null=True, blank=True)
    confianza = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Predicción para {self.imagen} a las {self.fecha}"