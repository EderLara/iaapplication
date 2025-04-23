from django.shortcuts import render
from .forms import PrediccionForm
from django.views.generic import TemplateView

# Create your views here.
class PrediccionView(TemplateView):
    template_name = 'predicciones/prediccion.html'
    formulario = PrediccionForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'formulario': self.formulario})
    