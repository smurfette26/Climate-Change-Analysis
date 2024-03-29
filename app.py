from flask import Flask

app = Flask(__name__)


@app.route("/")
def Hello():
  return "hello mayur"


print(__name__)
if __name__ == "__main__":
  app.run(host="0.0.0.0", port=8080)
