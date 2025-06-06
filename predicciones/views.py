from django.shortcuts import render
from .forms import PrediccionForm
from django.views.generic import TemplateView
from .models import Prediccion
from tensorflow import keras
from PIL import Image
import numpy as np
import os
import io
from django.conf import settings  # Importa la configuración de Django
from django.core.files.base import ContentFile

# cargar el modelo:
model = keras.models.load_model('core/model/best_mnist_model.h5') 

# Create your views here.
class PrediccionView(TemplateView):
    template_name = 'predicciones/prediccion.html'
    formulario = PrediccionForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'formulario': self.formulario})
    
    def post(self, request, *args, **kwargs):

        form = PrediccionForm(request.POST, request.FILES)

        if form.is_valid():
            image_file = form.cleaned_data['imagen']
            prediccion = Prediccion(imagen = image_file)
            prediccion.save()

            # Preprocesar la imagen:
            try:
                img = Image.open(prediccion.imagen.path).convert('L')                               # Convertir a escala de grises
                img = img.resize((28, 28))
                img_array = np.array(img) / 255.0
                img_array = img_array.reshape(1, 784)

                img_array_reshaped = img_array.reshape(28, 28) # Reshape para visualización

                # Realizar la predicción
                predictions = model.predict(img_array)
                predicted_class = np.argmax(predictions[0])
                confidence = np.max(predictions[0]) * 100

                # Actualizar la predicción en la base de datos
                prediccion.prediccion = predicted_class
                prediccion.confianza = confidence
                prediccion.save()

                # Renderizar el template nuevamente con los resultados y el posible mensaje de la URL
                context = {
                    'formulario': self.formulario,
                    'prediccion': predicted_class,
                    'confianza': confidence,
                    'imagen_url': prediccion.imagen.url,
                }
                mensaje_url = request.GET.get('prediccion')
                if mensaje_url:
                    context['mensaje_url'] = f"Mensaje desde la URL: {mensaje_url}"
                return render(request, self.template_name, context)
            
            except Exception as e:
                    prediccion.delete()
                    error_message = f"Error al procesar la imagen: {e}"
                    return render(request, self.template_name, {'formulario': self.formulario, 'error': error_message})

        # Si el formulario no es válido, vuelve a renderizar el formulario con los errores y el posible mensaje de la URL
        context = {'formulario': form}
        mensaje_url = request.GET.get('prediccion')
        if mensaje_url:
            context['mensaje_url'] = f"Mensaje desde la URL: {mensaje_url}"
        return render(request, self.template_name, context)