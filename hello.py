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


@app.route("/ht")
async def html_test(request):
    """
    html 返回测试
    :param request: 
    :return: 
    """
    return app.html("<h1>hello</h1>")


@app.route('/404')
async def test_404(request):
    """
    404 测试
    :param request: 
    :return: 
    """
    return app.abort_404("NOT FOUND")

# 静态路由测试 直接访问 /index.html 得到 static/index.html
# Static routing test direct access to /index.html get static / index.html

app.run()
