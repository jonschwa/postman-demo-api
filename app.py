from flask import Flask, request, make_response

app = Flask(__name__)


def get_headers(request):
    return {key: val for key, val in request.headers.items()}


def get_args(request):
    return {key: val for key, val in request.args.items()}


def get_cookies(request):
    return {key: val for key, val in request.cookies.items()}


@app.route("/echo", methods=["POST", "PUT", "PATCH"])
def echo_with_json_body():
    return {
        "method": request.method,
        "args": get_args(request),
        "body": request.json,
        "cookies": get_cookies(request),
        "headers": get_headers(request),
    }


@app.route("/echo", methods=["GET"])
def echo_get():
    return {
        "method": request.method,
        "args": get_args(request),
        "headers": get_headers(request),
        "cookies": get_cookies(request),
    }


@app.route("/delete", methods=["DELETE"])
def echo_delete():
    return "", 204


@app.route("/set_env_var", methods=["GET"])
def return_env_vars():
    return {"token": "abc123"}


@app.route("/protected", methods=["GET"])
def protected_endpoint():
    headers = get_headers(request)
    if auth_header := headers.get("Authorization", {}):
        # make sure this very secure token is valid
        token = auth_header.split()[1]
        if token == "abc123":
            return "Welcome!"
    return "Not Authorized", 401


@app.route("/cookies", methods=["GET"])
def set_cookies():
    resp = make_response("Cookies Set")
    resp.set_cookie("ll-postman-demo-cookie", "this-is-cookie-data!")
    return resp


@app.route("/mock", methods=["GET"])
def mock_endpoint():
    return {"property_1": "something"}
