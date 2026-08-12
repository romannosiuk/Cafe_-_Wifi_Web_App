import os
import random
from datetime import datetime
from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY environment variable is not set. Please set it before running the app.")

app = Flask(__name__)


# CREATE DB
class Base(DeclarativeBase):
    pass


# Connect to Database
database_url = os.getenv("DATABASE_URL", "sqlite:///cafes.db")
if database_url.startswith("postgresql://"):
    database_url = database_url.replace("postgresql://", "postgresql+psycopg://")
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
print(f"🗄️  Database: {database_url[:60]}...")
db = SQLAlchemy(model_class=Base)
db.init_app(app)


def is_cafe_open(open_hours):
    try:
        now = datetime.now().time()
        times = open_hours.split(" - ")
        opening_time = datetime.strptime(times[0].strip(), "%I:%M %p").time()
        closing_time = datetime.strptime(times[1].strip(), "%I:%M %p").time()
        return opening_time <= now <= closing_time
    except:
        return False


# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    pets_allowed: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)
    has_food: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_alcohol: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_ac: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_parking: Mapped[bool] = mapped_column(Boolean, nullable=False)
    open_hours: Mapped[str] = mapped_column(String(250), nullable=False)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


with app.app_context():
    # db.drop_all()
    db.create_all()


@app.route("/")
def home():
    db.session.expire_all()
    result = db.session.execute(db.select(Cafe))
    cafes = result.scalars().all()
    return render_template("index.html", cafes=cafes)


@app.route("/random")
def get_random_cafe():
    db.session.expire_all()

    result = db.session.execute(db.select(Cafe))
    all_cafes = result.scalars().all()
    if not all_cafes:
        return jsonify(error={"Not Found": "No cafes in database"}), 404
    random_cafe = random.choice(all_cafes)
    return jsonify(cafe=random_cafe.to_dict())


# HTTP GET - Read Record

@app.route("/all")
def get_all_cafes():
    db.session.expire_all()

    result = db.session.execute(db.select(Cafe))
    all_cafes = result.scalars().all()
    return jsonify(cafes=[cafe.to_dict() for cafe in all_cafes])


@app.route("/search")
def get_search_cafes():
    db.session.expire_all()
    name = request.args.get("name")
    location = request.args.get("loc")

    query = db.select(Cafe)
    if name:
        query = query.where(Cafe.name.ilike(f"%{name}%"))
    if location:
        query = query.where(Cafe.location == location)

    result = db.session.execute(query)
    all_cafes = result.scalars().all()

    if all_cafes:
        return jsonify(cafes=[cafe.to_dict() for cafe in all_cafes])
    else:
        return jsonify(error={"Not Found": "Sorry, no cafes found."}), 404


# HTTP GET/POST - Add Cafe

@app.route("/add", methods=["GET", "POST"])
def add_cafe():
    if request.method == "POST":
        new_cafe = Cafe(
            name=request.form.get("name"),
            map_url=request.form.get("map_url"),
            img_url=request.form.get("img_url"),
            location=request.form.get("loc"),
            has_sockets=bool(request.form.get("sockets")),
            has_toilet=bool(request.form.get("toilet")),
            has_wifi=bool(request.form.get("wifi")),
            can_take_calls=bool(request.form.get("calls")),
            pets_allowed=bool(request.form.get("pets")),
            has_food=bool(request.form.get("food")),
            has_alcohol=bool(request.form.get("alcohol")),
            has_ac=bool(request.form.get("a/c")),
            has_parking=bool(request.form.get("parking")),
            seats=request.form.get("seats"),
            coffee_price=request.form.get("coffee_price"),
            open_hours=request.form.get("open_hours"),
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add_cafe.html")


@app.route("/update/<int:cafe_id>", methods=["GET", "POST"])
def update_cafe(cafe_id):
    cafe = db.session.get(entity=Cafe, ident=cafe_id)
    if not cafe:
        return jsonify(error={"Not Found": "Cafe not found"}), 404

    if request.method == "POST":
        api_key = request.form.get("api_key")
        if api_key != API_KEY:
            return render_template("add_cafe.html", cafe=cafe, error="Invalid API Key")

        cafe.name = request.form.get("name")
        cafe.map_url = request.form.get("map_url")
        cafe.img_url = request.form.get("img_url")
        cafe.location = request.form.get("loc")
        cafe.has_sockets = bool(request.form.get("sockets"))
        cafe.has_toilet = bool(request.form.get("toilet"))
        cafe.has_wifi = bool(request.form.get("wifi"))
        cafe.can_take_calls = bool(request.form.get("calls"))
        cafe.pets_allowed = bool(request.form.get("pets"))
        cafe.has_food = bool(request.form.get("food"))
        cafe.has_alcohol = bool(request.form.get("alcohol"))
        cafe.has_ac = bool(request.form.get("a/c"))
        cafe.has_parking = bool(request.form.get("parking"))
        cafe.seats = request.form.get("seats")
        cafe.coffee_price = request.form.get("coffee_price")
        cafe.open_hours = request.form.get("open_hours")
        db.session.commit()
        return redirect(url_for("home"))

    return render_template("add_cafe.html", cafe=cafe)


# HTTP DELETE - Delete Record

@app.route("/report-closed/<int:cafe_id>", methods=["DELETE"])
def delete_cafe(cafe_id):
    api_key = request.args.get("api-key")
    if api_key == API_KEY:
        cafe = db.session.get(Cafe, cafe_id)
        if cafe:
            db.session.delete(cafe)
            db.session.commit()
            return jsonify(response={"success": "Successfully deleted the cafe from the database."}), 200
        else:
            return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."}), 404
    else:
        return jsonify(error={"Forbidden": "Sorry, that's not allowed. Make sure you have the correct Api_Key."}), 403


@app.route("/random-page", methods=["GET"])
def random_page():
    db.session.expire_all()

    result = db.session.execute(db.select(Cafe))
    all_cafes = result.scalars().all()
    if not all_cafes:
        return render_template("index.html", cafes=[])
    random_cafe = random.choice(all_cafes)
    return render_template("index.html", cafes=[random_cafe])


@app.route("/filtered-page")
def filtered_page():
    db.session.expire_all()

    cafe_name = request.args.get("cafe_name")
    has_wifi = request.args.get("has_wifi")
    has_sockets = request.args.get("has_sockets")
    has_toilet = request.args.get("has_toilet")
    has_alcohol = request.args.get("has_alcohol")
    pets_allowed = request.args.get("pets_allowed")
    has_food = request.args.get("has_food")
    has_ac = request.args.get("has_ac")
    has_parking = request.args.get("has_parking")
    open_now = request.args.get("open_now")

    query = db.select(Cafe)
    if cafe_name:
        query = query.where(Cafe.name.ilike(f"%{cafe_name}%"))
    if has_wifi:
        query = query.where(Cafe.has_wifi == True)
    if has_sockets:
        query = query.where(Cafe.has_sockets == True)
    if has_toilet:
        query = query.where(Cafe.has_toilet == True)
    if pets_allowed:
        query = query.where(Cafe.pets_allowed == True)
    if has_food:
        query = query.where(Cafe.has_food == True)
    if has_alcohol:
        query = query.where(Cafe.has_alcohol == True)
    if has_ac:
        query = query.where(Cafe.has_ac == True)
    if has_parking:
        query = query.where(Cafe.has_parking == True)

    result = db.session.execute(query)
    filtered_cafes = result.scalars().all()
    if open_now:
        filtered_cafes = [cafe for cafe in filtered_cafes
                          if is_cafe_open(cafe.open_hours)]
    return render_template("index.html", cafes=filtered_cafes,
                           cafe_name=cafe_name,
                           has_wifi=has_wifi,
                           has_sockets=has_sockets,
                           has_toilet=has_toilet,
                           has_alcohol=has_alcohol,
                           pets_allowed=pets_allowed,
                           has_food=has_food,
                           has_ac=has_ac,
                           has_parking=has_parking,
                           open_now=open_now)


if __name__ == '__main__':
    app.run(debug=True)
