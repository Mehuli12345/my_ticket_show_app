from flask import render_template, request, redirect, url_for, session, flash
from backend.models import db, UserInfo, Show, Theatre, Booking 
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

def register_routes(app):
    @app.route("/", endpoint='home')
    def home():
        return render_template("index.html")

    @app.route("/login", methods=["GET", "POST"], endpoint='login')
    def login():
        if request.method == "POST":
            email = request.form["email"]
            password = request.form["password"]
            user = UserInfo.query.filter_by(email=email).first()
            if user and check_password_hash(user.password, password):
                session["user_id"] = user.id
                session["user_type"] = user.user_type
                if user.user_type == "admin":
                    return redirect(url_for("admin_dashboard"))
                else:
                    return redirect(url_for("user_dashboard"))
            flash("Invalid credentials", "danger")
        return render_template("login.html")

    @app.route("/register", methods=["GET", "POST"], endpoint='register')
    def register():
        if request.method == "POST":
            new_user = UserInfo(
                email=request.form["email"],
                password=generate_password_hash(request.form["password"]),
                full_name=request.form["full_name"],
                address=request.form["address"],
                pin_code=request.form["pin_code"],
                user_type=request.form["user_type"]
            )
            db.session.add(new_user)
            db.session.commit()
            flash("Registration successful", "success")
            return redirect(url_for("login"))
        return render_template("signup.html")

    @app.route("/signup", methods=["GET"], endpoint='signup_alias')
    def signup_alias():
        return redirect(url_for("register"))

    @app.route("/admin/dashboard", endpoint='admin_dashboard')
    def admin_dashboard():
        if session.get("user_type") != "admin":
            flash("Unauthorized access", "danger")
            return redirect(url_for("login"))
        user = UserInfo.query.get(session["user_id"])
        theatres = Theatre.query.all()
        return render_template("admin_dashboard.html", name=user.full_name, theatres=theatres)

    @app.route("/user/dashboard", endpoint='user_dashboard')
    def user_dashboard():
        if session.get("user_type") != "user":
            flash("Unauthorized access", "danger")
            return redirect(url_for("login"))
        user = UserInfo.query.get(session["user_id"])
        shows = Show.query.all() 
        return render_template("user_dashboard.html", name=user.full_name, shows=shows)

    @app.route("/logout")
    def logout():
        session.clear()
        flash("Logged out successfully", "success")
        return redirect(url_for("login"))

    @app.route("/add_venue", methods=["GET", "POST"])
    def add_venue():
        if session.get("user_type") != "admin":
            return redirect(url_for("login"))
        if request.method == "POST":
            new_theatre = Theatre(
                name=request.form["name"],
                location=request.form["location"],
                pin_code=request.form["pin_code"],
                capacity=request.form["capacity"]
            )
            db.session.add(new_theatre)
            db.session.commit()
            flash("Theatre added successfully", "success")
            return redirect(url_for("admin_dashboard"))
        return render_template("add_venue.html")

    @app.route("/edit_venue/<int:venue_id>", methods=["GET", "POST"])
    def edit_venue(venue_id):
        if session.get("user_type") != "admin":
            return redirect(url_for("login"))
        venue = Theatre.query.get_or_404(venue_id)
        if request.method == "POST":
            venue.name = request.form["name"]
            venue.location = request.form["location"]
            venue.pin_code = request.form["pin_code"]
            venue.capacity = request.form["capacity"]
            db.session.commit()
            flash("Theatre updated successfully", "success")
            return redirect(url_for("admin_dashboard"))
        return render_template("edit_venue.html", venue=venue)

    @app.route("/delete_venue/<int:venue_id>")
    def delete_venue(venue_id):
        if session.get("user_type") != "admin":
            return redirect(url_for("login"))
        venue = Theatre.query.get_or_404(venue_id)
        db.session.delete(venue)
        db.session.commit()
        flash("Theatre deleted successfully", "success")
        return redirect(url_for("admin_dashboard"))
    
    @app.route('/book_ticket/<int:show_id>', methods=['GET', 'POST'])
    def book_ticket(show_id):
        show = Show.query.get_or_404(show_id)

        if request.method == 'POST':
        # Check if user is logged in (assuming you store user_id in session)
            user_id = session.get('user_id')
            if not user_id:
                flash("Please login to book tickets.", "warning")
                return redirect(url_for('login'))

        # Create a new booking record
            new_booking = Booking(user_id=user_id, show_id=show.id)
            db.session.add(new_booking)
            db.session.commit()

            flash(f'You have successfully booked tickets for "{show.name}"!', 'success')
            return redirect(url_for('user_dashboard'))

        return render_template('book_ticket.html', show=show)



    @app.route("/add_show", methods=["GET", "POST"])
    def add_show():
        if session.get("user_type") != "admin":
            return redirect(url_for("login"))
        theatres = Theatre.query.all()
        if request.method == "POST":
            new_show = Show(
                theatre_id=request.form["theatre_id"],
                name=request.form["name"],
                tags=request.form["tags"],
                rating=request.form["rating"],
                tkt_price=request.form["tkt_price"],
                date_time=datetime.strptime(request.form["date_time"], "%Y-%m-%dT%H:%M")
            )
            db.session.add(new_show)
            db.session.commit()
            flash("Show added successfully", "success")
            return redirect(url_for("admin_dashboard"))
        return render_template("add_show.html", theatres=theatres)

    @app.route("/delete_show/<int:show_id>")
    def delete_show(show_id):
        if session.get("user_type") != "admin":
            return redirect(url_for("login"))
        show = Show.query.get_or_404(show_id)
        db.session.delete(show)
        db.session.commit()
        flash("Show deleted successfully", "success")
        return redirect(url_for("admin_dashboard"))
