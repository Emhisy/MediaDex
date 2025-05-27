from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from ..constants.sources_constant import SOURCES

@login_required(login_url="/login/")
def explorer_home(request):
    context = { "sources": SOURCES.keys() }
    return render(request, 'explorer/index.html', context)

@login_required(login_url="/login/")
def explorer_source(request, source_name):
    source = SOURCES[source_name]()
    context = { "mangas": source.get_popular_manga() }
    return render(request, 'explorer/sources/index.html', context)