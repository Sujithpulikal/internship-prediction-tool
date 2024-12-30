from flask import Flask,  request,render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/lead")
def lead():
    return render_template("lead.html")
@app.route("/attrition")
def attrition():
    return render_template("attrition.html")
@app.route("/placement")
def placement():
    return render_template("placement.html")
@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)