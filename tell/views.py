from django.shortcuts import render
from listen.models import Entry


def index(request):
    logs = []
    print "Hello:", Entry.objects.distinct("logger")
    for entry in Entry.objects.distinct("logger"):
        logs.append({'name': entry.logger,
               'entries': Entry.objects.all().order_by('-id')[:10]})
    ctx = {"logs": logs}
    print ctx
    return render(request, "index.html", ctx)