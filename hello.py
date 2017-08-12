from monk import monk

app = monk.Monk()


@app.route("/")
async def index(request):
    c = request.args.get("c")
    return app.jsonfy(a=1, b=2, c=c)


@app.route("/ht")
async def html_test(request):
    return app.html("<h1>hello</h1>")


@app.route('/404')
async def test_404(request):
    return app.abort_404()

app.run()
