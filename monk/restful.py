from monk.router import Router
from monk.monk import Monk
import abc


class ResourcesBase:
    def __init__(self, app: Monk):
        self.router = app.router
        self.url = '/'+str(self.__class__.__name__).lower()
        self.router.add(url=self.url, handle=self.dispatch, methods=['GET', 'PUT', 'POST', 'DELETE'])

    async def dispatch(self, request):
        if request.method == 'GET':
            resp = await self.get(request)
        elif request.method == 'PUT':
            resp = await self.put(request)
        elif request.method == 'POST':
            resp = await self.post(request)
        elif request.method == 'DELETE':
            resp = await self.delete(request)
        else:
            resp = Monk.abort_404("Undefined method")
        return resp

    async def get(self, request):
        return Monk.abort_404('Undefined method')

    async def put(self, request):
        return Monk.abort_404('Undefined method')

    async def post(self, request):
        return Monk.abort_404('Undefined method')

    async def delete(self, request):
        return Monk.abort_404('Undefined method')


