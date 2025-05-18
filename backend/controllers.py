from flask import render_template, request, redirect, url_for, session, flash
from backend.models import db, UserInfo, Show, Theatre
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

def register_routes(app):

    @app.route("/")
    def home():
        return render_template("index.html")

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']

            user = UserInfo.query.filter_by(email=email).first()
            if user and check_password_hash(user.password, password):
                session['user_id'] = user.id
                session['user_type'] = user.user_type

                return redirect(url_for('admin_dashboard' if user.user_type == 'admin' else 'user_dashboard'))
            flash('Invalid credentials', 'danger')
            return redirect(url_for('login'))
        return render_template('login.html')

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            new_user = UserInfo(
                email=request.form.get("email"),
                password=generate_password_hash(request.form.get("password")),
                full_name=request.form.get("full_name"),
                address=request.form.get("address"),
                pin_code=request.form.get("pin_code"),
                user_type=request.form.get("user_type")
            )
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login', msg="Registration successful"))
        return render_template("signup.html")

    @app.route("/signup", methods=["GET"])
    def signup_alias():
        return redirect("/register")

    @app.route('/admin/dashboard')
    def admin_dashboard():
        if session.get('user_type') != 'admin':
            flash("Unauthorized access", "danger")
            return redirect(url_for('login'))
        user = UserInfo.query.get(session.get('user_id'))
        theatres = Theatre.query.all()
        return render_template('admin_dashboard.html', theatres=theatres, name=user.full_name)

    @app.route('/user/dashboard')
    def user_dashboard():
        if session.get('user_type') != 'user':
            flash("Unauthorized access", "danger")
            return redirect(url_for('login'))
        user = UserInfo.query.get(session.get('user_id'))
        shows = Show.query.filter(Show.date_time >= datetime.now()).all()
        return render_template('user_dashboard.html', shows=shows, name=user.full_name)

    @app.route("/user/<name>")
    def user_named_page(name):
        return render_template("user_dashboard.html", name=name)

    @app.route("/admin/<name>")
    def admin_named_page(name):
        return render_template("admin_dashboard.html", name=name)

    @app.route('/add_venue', methods=['GET', 'POST'])
    def add_venue():
        msg = ''
        if request.method == 'POST':
            name = request.form['name']
            location = request.form['location']
            pin_code = request.form['pin_code']
            capacity = request.form['capacity']

            if not all([name, location, pin_code, capacity]):
                msg = "Please fill all fields."
                return render_template('add_venue.html', msg=msg)

            try:
                new_venue = Theatre(name=name, location=location,
                                    pin_code=int(pin_code), capacity=int(capacity))
                db.session.add(new_venue)
                db.session.commit()
                msg = "Venue added successfully"
            except Exception as e:
                db.session.rollback()
                msg = f"Error adding venue: {str(e)}"
        return render_template('add_venue.html', msg=msg)

    @app.route('/show/<int:id>/<name>', methods=['GET', 'POST'])
    def show(id, name):
        if session.get('user_type') != 'admin':
            flash("Unauthorized access", "danger")
            return redirect(url_for('login'))

        msg = ''
        if request.method == 'POST':
            venue_id = request.form.get('venue_id')
            movie_name = request.form.get('movie_name')
            tags = request.form.get('tags')
            rating = request.form.get('rating')
            tkt_price = request.form.get('tkt_price')
            dt_time = request.form.get('dt_time')

            if not all([venue_id, movie_name, tags, rating, tkt_price, dt_time]):
                msg = "Please fill all fields."
                return render_template('add_show.html', msg=msg, id=id, name=name)

            try:
                new_show = Show(
                    theatre_id=int(venue_id),
                    name=movie_name,
                    tags=tags,
                    rating=int(rating),
                    tkt_price=float(tkt_price),
                    date_time=datetime.strptime(dt_time, '%Y-%m-%dT%H:%M')
                )
                db.session.add(new_show)
                db.session.commit()
                msg = "Show added successfully."
            except Exception as e:
                db.session.rollback()
                msg = f"Error adding show: {str(e)}"

        return render_template('add_show.html', msg=msg, id=id, name=name)