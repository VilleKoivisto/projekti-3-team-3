import flask

def medium(request):

    request_args = request.args

    if request_args and "name" in request_args:
        name = request_args["name"]
    else:
        name = "juukeli"
    return "Haista sinä {} vittu!".format(flask.escape(name))