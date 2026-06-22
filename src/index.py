from workers import WorkerEntrypoint
from django_cf import DjangoCF
from restaurants.wsgi import application

class Default(DjangoCF, WorkerEntrypoint):
    async def get_app(self):
        return application
