import os
import flask
import flask_login
from string import ascii_uppercase
from hashlib import sha256
import json
       
app = flask.Flask(__name__)
app.secret_key = os.urandom(4096)
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

class User(flask_login.UserMixin):
  pass

class objects:
    path:str = os.path.dirname(__file__)
    prev_path:str = os.path.dirname(path)
    json:dict = {}
    files:list = []
    folders:list = []

@login_manager.user_loader
def loader(user_id) -> User:
  user = User()
  user.id = user_id
  return user

def loadJSON():
    with open(
        os.path.join(
            os.path.dirname(__file__),
            "config/server.config.json"
        )
    ) as r:
        objects.json = json.load(r)


@app.route("/")
@app.route("/index/")
def index():
    if "login" in flask.session and flask.session["login"]:
        objects.files = []
        objects.folders = []
        for file in os.scandir(objects.path):
            if file.is_file():
                try:
                    with open(file) as r:pass
                except:
                    objects.files.append((file.name, False))
                else:
                    objects.files.append((file.name, True))
            elif file.is_dir():
                try:
                    os.scandir(file)
                except:
                    objects.folders.append((file.name, False))
                else:
                    objects.folders.append((file.name, True))

        return flask.render_template(
            "folders.html",
            directory=objects.path,
            folders=objects.folders,
            prev_path=objects.prev_path,
            version=objects.json["INFO"]["version"]
        )
    else:
        return flask.redirect("/login/")

@app.route("/index/folders/", methods=["GET"])
@flask_login.login_required
def folders():
    return flask.render_template(
        "folders.html",
        directory=objects.path,
        folders=objects.folders,
        prev_path=objects.prev_path,
        version=objects.json["INFO"]["version"]
    )

@app.route("/index/files/", methods=["GET"])
@flask_login.login_required
def files():
    return flask.render_template(
        "files.html",
        directory=objects.path,
        files=objects.files,
        prev_path=objects.prev_path,
        version=objects.json["INFO"]["version"]
    )

@app.route("/login/", methods=["GET", "POST"])
def login():
  if flask.request.method == "GET":
    return flask.render_template("login.html", version=objects.json["INFO"]["version"])
  elif flask.request.method == "POST":
    if flask.request.form["username"] == objects.json["USER"]["username"]:
        m = sha256()
        m.update(bytes(flask.request.form["password"], "utf8"))
        if m.hexdigest() == objects.json["USER"]["pass"]:
          user = User()
          user.id = flask.request.form["username"]
          flask_login.login_user(user)
          flask.session.update({"login":True})

          return flask.redirect(flask.url_for("index"))

        else:
            return flask.render_template("login.html", error="Error", version=objects.json["INFO"]["version"])

    else:
      return flask.render_template("login.html", error="Error", version=objects.json["INFO"]["version"])
      
  else:
    flask.abort(403)


@app.route("/download/<item>/", methods=["GET"])
@flask_login.login_required
def download(item):
    return flask.send_from_directory(directory=objects.path, path=item, as_attachment=True)

@app.route("/previous/")
@flask_login.login_required
def prevdir():
    objects.path = objects.prev_path
    objects.prev_path = os.path.dirname(objects.path)
    return flask.redirect("/index/")

@app.route("/upload/", methods=["POST"])
@flask_login.login_required
def upload():
    file = flask.request.files['file']
    file.save(os.path.join(objects.path, file.filename))
    return flask.redirect("/index/")

@app.route("/next/<folder>/")
@flask_login.login_required
def next(folder):
    if os.path.exists(f"{objects.path}/{folder}"):
        objects.prev_path = objects.path
        objects.path = f"{objects.path}/{folder}"

    return flask.redirect("/index/")

@app.route("/reset/")
def reset():
    objects.path = os.path.dirname(__file__)
    objects.prev_path = os.path.dirname(objects.path)
    return flask.redirect("/index/")

@app.errorhandler(403)
def e403(error):
    return flask.render_template("500.html", error=error, status=403)

@app.errorhandler(404)
def e404(error):
    return flask.render_template("500.html", error=error, status=404)

@app.errorhandler(Exception)
def e500(error):
    return flask.render_template("500.html", error=error, status=500)

if __name__ == "__main__":
    loadJSON()
    app.run(
        debug=True,
        host=objects.json["NETWORK"]["host"],
        port=objects.json["NETWORK"]["port"]
    )