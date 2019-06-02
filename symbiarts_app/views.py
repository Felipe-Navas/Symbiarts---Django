from django.shortcuts import render, get_object_or_404, redirect
from .models import Obra, ObraArchivo
from django.utils import timezone
from .forms import ObraForm, ObraArchivosForm
from django.contrib.auth.decorators import login_required


def lista_obras(request):
    obras = Obra.objects.filter(
        fecha_publicacion__lte=timezone.now()).order_by('-fecha_publicacion')
    return render(request, 'symbiarts_app/lista_obras.html', {'obras': obras})


def detalle_obra(request, pk):
    obra = get_object_or_404(Obra, pk=pk)
    archivos_obra = ObraArchivo.objects.filter(obra__pk=pk)
    return render(request, 'symbiarts_app/detalle_obra.html', {
        'obra': obra,
        'archivos_obra': archivos_obra})


#@login_required
def nueva_obra(request):
    if request.method == "POST":
        form = ObraForm(request.POST)
        file_form = ObraArchivosForm(request.POST, request.FILES)
        files = request.FILES.getlist('archivo')
        if form.is_valid() and file_form.is_valid():
            obra = form.save(commit=False)
            #obra.id_usuario = request.user
            obra.save()
            for f in files:
                obra_archivo = ObraArchivo(archivo=f, obra=obra)
                obra_archivo.save()
            return redirect('symbiarts_app:detalle_obra', pk=obra.pk)
    else:
        form = ObraForm()
        file_form = ObraArchivosForm()
    return render(request, 'symbiarts_app/editar_obra.html', {
        'form': form,
        'file_form': file_form,
        'tipos_obra': Obra.tipos_obra})


#@login_required
def editar_obra(request, pk):
    obra = get_object_or_404(Obra, pk=pk)
    if request.method == "POST":
        form = ObraForm(request.POST, instance=obra)
        file_form = ObraArchivosForm(
            request.POST,
            request.FILES,
            instance=obra)
        files = request.FILES.getlist('archivo')
        if form.is_valid() and file_form.is_valid():
            obra = form.save(commit=False)
            #obra.id_usuario = request.user
            obra.save()
            # Ver si borro to lo que tiene relacionado el ObraArchivos
            for f in files:
                obra_archivo = ObraArchivo(archivo=f, obra=obra)
                obra_archivo.save()
            return redirect('symbiarts_app:detalle_obra', pk=obra.pk)
    else:
        form = ObraForm(instance=obra)
        file_form = ObraArchivosForm(instance=obra_archivo)
    return render(request, 'symbiarts_app/editar_obra.html', {
        'form': form,
        'file_form': file_form})


#@login_required
def eliminar_obra(request, pk):
    obra = get_object_or_404(Obra, pk=pk)
    obra.delete()
    return redirect('symbiarts_app:lista_obras')


"""
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)


"""