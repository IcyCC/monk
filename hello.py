from monk import monk

app = monk.Monk()


@app.route("/")
async def index(request):
    return app.jsonfy(a=1,b=2)

app.run()
