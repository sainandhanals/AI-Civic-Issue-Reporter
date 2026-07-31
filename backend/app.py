from flask import Flask, render_template, request

app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static"
)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    image = request.files["image"]

    return f"""
    <h2>✅ Image Uploaded Successfully!</h2>
    <p>Filename: {image.filename}</p>
    <a href="/">Go Back</a>
    """


if __name__ == "__main__":
    app.run(debug=True)