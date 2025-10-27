from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///features.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Feature(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)

with app.app_context():
    db.create_all()
    if Feature.query.count() == 0:
        db.session.bulk_save_objects([
            Feature(name="Responsive Design", description="Mobile-friendly layouts with Bootstrap."),
            Feature(name="Dynamic Content", description="Features loaded from database."),
            Feature(name="Custom Styling", description="SCSS compiled to CSS."),
        ])
        db.session.commit()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")

        if not name or not description:
            flash("Both fields are required.", "danger")
        else:
            db.session.add(Feature(name=name, description=description))
            db.session.commit()
            flash("Feature added successfully!", "success")

        return redirect(url_for("index"))

    features = Feature.query.all()
    return render_template("index.html", features=features)

if __name__ == "__main__":
    app.run(debug=True)
