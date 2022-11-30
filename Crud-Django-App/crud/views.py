from django.shortcuts import get_object_or_404, render, redirect
from .models import Note
from .forms import NoteForm


def note_list(request):
    """Note list view"""
    notes = Note.objects.all()

    context = {
        'notes': notes,
    }

    return render(request, 'crud/list.html', context)


def note_detail(request, pk):
    """Note detail view"""
    note = get_object_or_404(Note, pk=pk)

    if request.method == 'POST':
        form = NoteForm(request.POST or None, instance=note)
        if form.is_valid():
            form.save()
        return redirect('list')

    form = NoteForm(request.POST or None, instance=note)
    
    context = {
        'note': note,
        'form': form,
    }

    return render(request, 'crud/detail.html', context)


def note_create(request):
    """Note edit form view"""
    form = NoteForm(request.POST)

    if form.is_valid():
        form.save()
        return redirect('list')
    
    context = {
        'form': form,
    }

    return render(request, 'crud/create.html', context)


def note_delete(request, pk):
    """Note delete view"""
    note = get_object_or_404(Note, pk=pk)

    if request.method == 'POST':
        note.delete()
        return redirect('list')

    context = {
        'note': note,
    }

    return render(request, 'crud/delete.html', context)