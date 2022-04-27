from flask import Flask, request
import os

from rubik.dispatch import dispatch


app = Flask(__name__)


@app.route("/rubik")
def server():
    try:
        result = dispatch({param: str(request.args.get(param, "")) for param in request.args})
        print(f"Response --> {result}")
        return str(result)
    except Exception as e:
        return str(e)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")))
