from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from random import randrange
from markdown2 import Markdown
from . import util

from django import forms
markdowner = Markdown()


class SearchForm(forms.Form):
    search = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Search Encyclopedia'}))


class NewForm(forms.Form):
    title = forms.CharField(label="title", widget=forms.TextInput(
        attrs={'placeholder': 'Title'}))
    content = forms.CharField(widget=forms.Textarea)


class EditForm(forms.Form):
    title = forms.CharField(label="title")
    content = forms.CharField(widget=forms.Textarea)


def index(request):
    alltop = util.list_entries()

    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data["search"]
            print(query)
            print(util.list_entries())
            results = []
            for top in alltop:
                if query in top:
                    results.append(top)

            if query in alltop:
                return render(request, "encyclopedia/page.html", {
                    "topic": util.get_entry(query),
                    "form": form,
                    "random": alltop[randrange(len(alltop))]
                })
            elif results:
                return render(request, "encyclopedia/results.html", {
                    "form": form,
                    "results": results,
                    "random": alltop[randrange(len(alltop))]

                }

                )

            return render(request, "encyclopedia/index.html", {
                "form": form,
                "entries": util.list_entries(),
                "random": alltop[randrange(len(alltop))]

            })

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": SearchForm(),
        "random": alltop[randrange(len(alltop))]
    })


def get(request, title):
    alltop = util.list_entries()
    topic = util.get_entry(title)
    if not topic:
        return render(request, "encyclopedia/error.html", {
            "code": 404,
            "message": "Topic is not found",
            "random": alltop[randrange(len(alltop))]

        })

    return render(request, "encyclopedia/page.html", {
        "topic": markdowner.convert(topic),
        "title": markdowner.convert(title),
        "random": alltop[randrange(len(alltop))]
    })


def edit(request, title):
    alltop = util.list_entries()

    if request.method == "POST":
        etopic = EditForm(request.POST)  # etopic is the name of the form
        if etopic.is_valid():
            etitle = etopic.cleaned_data["title"]  # extracting the title
            content = etopic.cleaned_data["content"]  # extracting the content

            util.save_entry(etitle, content)  # save entries

            return render(request, "encyclopedia/index.html", {
                "entries": util.list_entries(),
                "form": SearchForm(),
                "random": alltop[randrange(len(alltop))]
            })
    content = util.get_entry(title)
    initial_date = {"title": title, "content": content}

    return render(request, "encyclopedia/edit.html", {
        "form3": EditForm(initial=initial_date),
        "form": SearchForm(),
        "random": alltop[randrange(len(alltop))]
    })


def new(request):

    alltop = util.list_entries()

    if request.method == "POST":
        topicf = NewForm(request.POST)  # topicf is the name of the form
        if topicf.is_valid():
            newt = topicf.cleaned_data["title"]  # extracting the title
            content = topicf.cleaned_data["content"]  # extracting the contact
            if newt in alltop:  # check if the title is already exists
                return render(request, "encyclopedia/error.html", {
                    "code": 403,
                    "message": "This topic is already exists",
                    "random": alltop[randrange(len(alltop))]


                })

            util.save_entry(newt, content)  # save entries

            return render(request, "encyclopedia/index.html", {
                "entries": util.list_entries(),
                "form": SearchForm(),
                "random": alltop[randrange(len(alltop))]
            })

    return render(request, "encyclopedia/new.html", {
        "form2": NewForm(),
        "form": SearchForm(),
        "random": alltop[randrange(len(alltop))]
    })
