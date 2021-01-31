from django.shortcuts import render, redirect
from django import forms
from . import util

import markdown2
import re
import random

class EntryForm(forms.Form):
    title = forms.CharField(label='title', required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Enter Title',
        'class': 'form-control rounded-input',
        'id': 'title',
        'aria-describedby': 'title-help',
        'maxlength': '50',
    }))
    content = forms.CharField(label='content', required=False, widget=forms.Textarea(attrs={
        'placeholder': 'Enter Content',
        'class': 'form-control rounded-input',
        'id': 'content',
        'aria-describedby': 'content-help',
        'rows': '10'
    }))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = ''
    if title.lower() in map(lambda x:x.lower(), util.list_entries()):
        content = markdown2.markdown(util.get_entry(title))
        page_title = title
        found = True
    else:
        content = markdown2.markdown('#404 PAGE NOT FOUND')
        page_title = "404 Not Found"
        found = False
    return render(request, "encyclopedia/entry.html", {
        "content": content,
        "title": page_title,
        "found": found
    })

def create_entry(request):

    if request.method == 'POST':
        form = EntryForm(request.POST)
        error = ''

        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']

            if title == '':
                error = 'Title cannot be left blank'
            elif len(title) > 50:
                error = 'Title cannot be more than 50 characters'
            elif title.lower() in map(lambda x:x.lower(), util.list_entries()):
                error = 'An entry with that title already exists'
            elif content == '':
                error = 'Content cannot be blank'
        
            if error != '':
                return render(request, 'encyclopedia/create.html', {
                    'error': error,
                    'form': form,
                })
            else:
                util.save_entry(title, content)
                return redirect('entry', title=title)

        else:
            return render(request, 'encyclopedia/create.html', {
                'form': form,
                'error': 'Bad data'
            })
        
    else:
        form = EntryForm()
        return render(request, 'encyclopedia/create.html', {
            'form': form
        })

def find_entry(request):
    entries = list(map(lambda x:x.lower(), util.list_entries()))
    query = request.POST.get('q').lower()
    if query in entries:
        return redirect('entry', title=request.POST.get('q'))
    else:
        matches = []
        for entry in util.list_entries():
            if query in entry.lower():
                matches.append(entry)
     
        return render(request, "encyclopedia/index.html", {
            "entries": matches,
            "searched": True,
            "query": request.POST.get('q'),
        })

def random_entry(request):
    return redirect('entry', title=random.choice(util.list_entries()))

def edit_entry(request, title):
    entries = util.list_entries()
    match = ''
    for entry in entries:
        if title.lower() == entry.lower():
            match = entry
            break

    if match == '':
        return redirect('entry', title="404")
    else:
        if request.method == 'POST':
            form = EntryForm(request.POST)
            error = ''
            if form.is_valid():
                if form.cleaned_data['content'] == '':
                    error = 'Content cannot be blank'
                
                if error != '':
                    return render(request, 'encyclopedia/edit.html', {
                        'form': form,
                        'error': error
                    })
                else:
                    util.save_entry(title, form.cleaned_data['content'])
                    return redirect('entry', title=title)
            
            else:
                return render(request, 'encyclopedia/edit.html', {
                    'form': form,
                    'error': 'Bad Data'
                })
        else:
            form = EntryForm(initial={'title': match, 'content': util.get_entry(match)})
            form.fields['title'].widget.attrs['readonly'] = True
            return render(request, 'encyclopedia/edit.html', {
                'form': form,
                'title': title
            })
