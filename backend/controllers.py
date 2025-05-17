from flask import render_template, request, redirect, url_for
from backend.models import db, UserInfo

def register_routes(app):
    @app.route("/")
    def home():
        return render_template("index.html")
    @app.route("/admin_dashboard")
    def admin_dashboard():
        return render_template("admin_dashboard.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            email = request.form.get("email")
            password = request.form.get("password")

        # Check database for matching user
            user = UserInfo.query.filter_by(email=email, password=password).first()

            if user:
                return redirect(url_for('admin_dashboard'))  # ← go to dashboard if valid
            else:
                return redirect(url_for('login'))  # ← stay on login if wrong

        return render_template("login.html", msg="Invalid user credential")


    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            email = request.form.get("email")
            password = request.form.get("password")
            password=my_encrypt(password)
            full_name = request.form.get("full_name")
            address = request.form.get("address")
            pin_code = request.form.get("pin_code")

            new_user = UserInfo(
                email=email,
                password=password,
                full_name=full_name,
                address=address,
                pin_code=pin_code
            )

            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('login', msg= "Registration successfull, try login in now"))

        return render_template("signup.html")

    @app.route("/signup", methods=["GET"])
    def signup_alias():
        return redirect("/register")
    
    def my_encrypt():
        #code here

