from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ContactoForm

@login_required
def enviar_mensaje_soporte(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            # Aquí se procesaría el envío de correo o guardado en BD
            messages.success(request, 'Tu mensaje ha sido enviado exitosamente al equipo de soporte.')
            return redirect('contacto')
    else:
        form = ContactoForm()
    return render(request, 'contacto.html', {'form': form})