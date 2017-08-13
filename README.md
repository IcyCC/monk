# Monk a async web framework learn Sanic

## environment

only for *nix because of httptools and uvloop

## Simple Use

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

## RestFULL 

will add son