from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5, Bootstrap
from flask_sqlalchemy import SQLAlchemy

# Here we define our bakery, which is the web application itself. We use app = Flask(__name__) to create an
# instance of the Flask class and give it a name (__name__ is a special variable). It's like setting up the
# oven and workspace for baking.
app = Flask(__name__)

# This line sets the location 🗺️ of the database (a file named the_film_collection.db) and the type of database 🛢️ (in this
# case SQLite).
# It's like setting where the ingredients will be stored for easy access.
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///the_film_collection.db"

# Then we configure the bakery using a secret key 🗝️,
# via app.config['SECRET_KEY'] = "super_secret_key"🗝️.
# This secret key is important for ensuring the security of our application, like having
# a secret recipe that nobody else knows.
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

# CREATE DB
# Finally, we initialize SQLAlchemy tool 🔨 through our bakery, using db.init_app(app).
db = SQLAlchemy()
# This allows them to work smoothly together, like having a skilled baker who knows how to handle the oven.
db.init_app(app)


# CREATE TABLE
# Here we define the blueprint of how movie templates 🎞️ look like in our system using class BooksDb(db.Model):
# Each of these properties (id, title, author, rating) is created using db.Column(...), specifying the data type and
# any special rules (e.g., being unique).
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    ranking = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)


# This line of code is used to create tables 🪧 in the database 🛢️, but only if they don't exist yet.
# This part ensures the appropriate environment 🍀 for db.create_all().
# It tells the application to temporarily use the "app" context, which is necessary for communicating with the database 🛢️.
with app.app_context():
    # This line of code checks whether the tables 🪧🪧🪧 in the database 🛢️ are already created.
    # If they are not, the code creates them.
    # If they are, the code does nothing.
    db.create_all()
    # Note:
    # This code runs only once‼️, e.g., during the first installation of the application.
    # There's no need to run it again because the tables 🪧🪧🪧 in the database 🛢️ are already created.

    # # ADD NEW ENTRY TO DATABASE
    # # Add a new movie, only if it doesn't exist in the database
    if not Movie.query.filter_by(title="Phone Booth").first():
        new_movie = Movie(
            title="Phone Booth",
            year=2002,
            description="Publicist Stuart Shepard finds himself trapped in a phone booth...",
            rating=7.3,
            ranking=10,
            review="My favourite character was the caller.",
            img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
        )

        second_movie = Movie(
            title="Avatar The Way of Water",
            year=2022,
            description="Set more than a decade after the events of the first film, learn the story of the Sully family (Jake, Neytiri, and their kids), the trouble that follows them, the lengths they go to keep each other safe, the battles they fight to stay alive, and the tragedies they endure.",
            rating=7.3,
            ranking=9,
            review="I liked the water.",
            img_url="https://image.tmdb.org/t/p/w500/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg"
        )
        # Add the new movie to the session and commit changes
        # 2) Add the movie 🎞️ to the shelf in the library 🗄️:
        db.session.add(new_movie)
        db.session.add(second_movie)

        # 3) Commit the place of the new movie 🎞️:
        db.session.commit()


@app.route("/")
def home():
    # Constructs 🔨 a query to select data from the database 🛢️. Building queries is the main feature of SQLAlchemy
    result = db.session.execute(db.select(Movie))

    # You’ll usually use the Result.scalars() method to get a list of results, or the Result.scalar() method to get a
    # single result
    all_movies = result.scalars().all()
    return render_template("index.html", film_list=all_movies)


if __name__ == '__main__':
    app.run(debug=True)
