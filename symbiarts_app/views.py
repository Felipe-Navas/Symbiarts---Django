from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from .models import Obra, ObraArchivo, Comentario
from django.utils import timezone
from .forms import FormObra, FormObraArchivos, FormComentario
from django.contrib.auth.decorators import login_required


def lista_obras(request):
    queryset = Obra.objects.filter(
        fecha_publicacion__lte=timezone.now()).order_by('-fecha_publicacion')
    page = request.GET.get('page')
    paginator = Paginator(queryset, 21)
    try:
        obras = paginator.page(page)
    except PageNotAnInteger:
        # Volver a la primera página
        obras = paginator.page(1)
    except EmptyPage:
        # Voy a la ultima página si llega una inexistente
        obras = paginator.page(paginator.num_pages)
    return render(request, 'symbiarts_app/lista_obras.html', {'obras': obras})


def detalle_obra(request, pk):
    obra = get_object_or_404(Obra, pk=pk)
    archivos_obra = ObraArchivo.objects.filter(obra__pk=pk)

    queryset = obra.comentarios.all()
    page = request.GET.get('page')
    paginator = Paginator(queryset, 10)
    try:
        comentarios = paginator.page(page)
    except PageNotAnInteger:
        # Volver a la primera página
        comentarios = paginator.page(1)
    except EmptyPage:
        # Voy a la ultima página si llega una inexistente
        comentarios = paginator.page(paginator.num_pages)

    form = FormComentario()
    return render(request, 'symbiarts_app/detalle_obra.html', {
        'obra': obra,
        'archivos_obra': archivos_obra,
        'form': form,
        'comentarios': comentarios})


@login_required
def nueva_obra(request):
    if request.method == "POST":
        form = FormObra(request.POST)
        file_form = FormObraArchivos(request.POST, request.FILES)
        files = request.FILES.getlist('archivo')
        if form.is_valid() and file_form.is_valid():
            obra = form.save(commit=False)
            obra.usuario = request.user
            obra.save()
            for f in files:
                obra_archivo = ObraArchivo(archivo=f, obra=obra)
                obra_archivo.save()
            return redirect('symbiarts_app:detalle_obra', pk=obra.pk)
    else:
        form = FormObra()
        file_form = FormObraArchivos()
    return render(request, 'symbiarts_app/editar_obra.html', {
        'form': form,
        'file_form': file_form})


@login_required
def editar_obra(request, pk):
    obra = get_object_or_404(Obra, pk=pk)
#    obra_archivo = ObraArchivo.objects.filter(obra__pk=pk)
    if request.method == "POST":
        form = FormObra(request.POST, instance=obra)
        file_form = FormObraArchivos(
            request.POST,
            request.FILES,
            instance=obra)
        files = request.FILES.getlist('archivo')
        if form.is_valid() and file_form.is_valid():
            obra = form.save(commit=False)
            obra.id_usuario = request.user
            obra.save()
            # Ver si borro to lo que tiene relacionado el ObraArchivos
            for f in files:
                obra_archivo = ObraArchivo(archivo=f, obra=obra)
                obra_archivo.save()
            return redirect('symbiarts_app:detalle_obra', pk=obra.pk)
    else:
        form = FormObra(instance=obra)
#        file_form = FormObraArchivos(instance=obra_archivo)
        file_form = FormObraArchivos()
    return render(request, 'symbiarts_app/editar_obra.html', {
        'form': form,
        'file_form': file_form})


@login_required
def eliminar_obra(request, pk):
    obra = get_object_or_404(Obra, pk=pk)
    obra.delete()
    return redirect('symbiarts_app:lista_obras')


@login_required
def nuevo_comentario(request, pk):
    obra = get_object_or_404(Obra, pk=pk)
    if request.method == "POST":
        form = FormComentario(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.obra = obra
            comentario.usuario = request.user
            comentario.save()
            return redirect('symbiarts_app:detalle_obra', pk=obra.pk)
    else:
        return redirect('symbiarts_app:detalle_obra', pk=obra.pk)


@login_required
def eliminar_comentario(request, pk):
    comentario = get_object_or_404(Comentario, pk=pk)
    comentario.delete()
    return redirect('symbiarts_app:detalle_obra',
                    pk=comentario.obra.pk)
