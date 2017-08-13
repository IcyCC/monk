# -- Monk
 A async web framework with RESTful imitate Sanic

## environment

Only for *nix because of httptools and uvloop. And python 3.5++.

## Simple Use

Like flask you should define a *app*, then use *app.route* decorate a function with a parameter
*request* and return a *Response*. *request* provide like *args,form,json*.And you can make a response
use like *app.jsonfy app.html app.abort_404*

```
from monk import monk

app = monk.Monk()

@app.route("/")
async def index(request):
    """
    json 返回测试
    request.args 测试
    :param request: 
    :return: 
    """
    c = request.args.get("c")
    return app.jsonfy(a=1, b=2, c=c)

app.run()
```
## Static
Request url like /index.html, will access ./static/index.html .
All your static file should be put into static folder.

## RESTfull 

Define a class inherit monk.restful.ResourcesBase and *async def* like *put,get,post,delete*
Registered it with app. You will get /<class_name_lower_case> url

```angular2html
from monk.restful import ResourcesBase

class Pig(ResourcesBase):
    """
    RESTful test 
    http://127.0.0.1:5000/pig method='GET' 
    """
    def __init__(self, app):
        ResourcesBase.__init__(self, app=app)
        self.app = app

    async def get(self, request):
        return app.html("<h1>PIG TEST</h1>")

pig = Pig(app)

```