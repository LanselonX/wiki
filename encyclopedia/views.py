import markdown2

from django.shortcuts import render, redirect
from django.http import HttpResponse

from . import util


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
        return redirect(f"/wiki/{search_container}")

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