from __future__ import absolute_import

from django.core.management.base import BaseCommand
import listen.net

class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        background_server = listen.net.BackgroundServer()
        background_server.run()