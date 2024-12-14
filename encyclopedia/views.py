import markdown2, random

from django.shortcuts import render, redirect
from django import forms
from django.urls import reverse
from django.contrib import messages

from . import util

class NewAddForm(forms.Form):
    article = forms.CharField(label="Article")
    content = forms.CharField(
        label="Article Content",
        widget=forms.Textarea(attrs={
            "style": "width: 600px; height: 120px",
            "placeholder": "Enter a description",
        }),
        required=False
    )

class EditForm(forms.Form):
    content = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            "style": "width: 600px; height: 120px",
            "placeholder": "Enter a description",
        }),
        required=False
    )

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })

def entry_func(request, title):
    content = util.get_entry(title)

    if content is None:
        return (render(request, "encyclopedia/error.html", {
            "title": title,
        }))

    else:
        html_content = markdown2.markdown(content)

        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })

def search_func(request):
    search_container = request.GET.get('q')
    storage = util.list_entries()
    find_entries = list()

    if search_container in storage:
        return redirect(reverse("entry", kwargs={'title': search_container}))

    for entry in storage:
        if search_container.lower() in entry.lower():   
            find_entries.append(entry)

    if find_entries:
        return render(request, "encyclopedia/search.html", {
            "search_result": find_entries,
            "search": search_container
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "title": search_container
        })

def add(request):
    if request.method == "POST":
        form = NewAddForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["article"]
            content = form.cleaned_data["content"]
            if util.get_entry(title):
                form.add_error('article', "Error: article with this title already exist")
            else:
                util.save_entry(title, content)
                messages.success(request, f"New page {title} created successfully")
                return redirect(reverse('entry', args=[title]))
        else:
            NewAddForm()
        return render(request, "encyclopedia/add.html", {
            "form": form,
        })
                
    return render(request, "encyclopedia/add.html", {
        "form": NewAddForm(),
    })

def edit(request, title):
    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            messages.success(request, f"Entry {title} updated succussfuly")
            return redirect(reverse('entry', args=[title]))
        else:
            messages.error(request, f"Editing form not valid, please try again!")
    else:
        existing_content = util.get_entry(title)
        if existing_content is None:
            messages.error(request, f"{title} not found")
            return redirect(reverse('index'))
        form = EditForm(initial={"content": existing_content})
    return render(request, "encyclopedia/edit.html", {
        "form": form,
        "title": title,
})

def random_title(request):
    titles = util.list_entries()
    title = random.choice(titles)

    return redirect(reverse('entry', args=[title]))