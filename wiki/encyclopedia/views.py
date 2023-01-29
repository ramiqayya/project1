from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from . import util

from django import forms


class SearchForm(forms.Form):
    search = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Search Encyclopedia'}))


def index(request):

    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data["search"]
            print(query)
            print(util.list_entries())
            results = []
            for top in util.list_entries():
                if query in top:
                    results.append(top)

            if query in util.list_entries():
                return render(request, "encyclopedia/page.html", {
                    "topic": util.get_entry(query),
                    "form": form
                })
            elif results:
                return render(request, "encyclopedia/results.html", {
                    "form": form,
                    "results": results

                }

                )

                return render(request, "encyclopedia/query.html",)

            return render(request, "encyclopedia/index.html", {
                "form": form,
                "entries": util.list_entries()
            })

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": SearchForm()
    })


def get(request, title):

    topic = util.get_entry(title)
    if not topic:
        return render(request, "encyclopedia/error.html")

    return render(request, "encyclopedia/page.html", {
        "topic": topic
    })
