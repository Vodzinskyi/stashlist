from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserForm


def create_user(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['password'] != form.cleaned_data['password_confirm']:
                form.add_error('password_confirm', 'Паролі не співпадають')
                return render(request, 'registration_form.html', {'form': form})
            user = form.save(commit=False)
            user.save()
            return redirect('/')
    else:
        form = UserForm()

    return render(request, 'registration_form.html', {'form': form})


