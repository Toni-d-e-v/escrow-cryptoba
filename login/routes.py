from flask import flash, render_template, request, redirect, url_for
from flask_login import (
    LoginManager,
    login_required,
    login_user,
    logout_user,
    current_user,
)
from login import app, db
from login.models import User, remove_escrow, change_bep20_address, change_email, change_password, change_telegram_username, change_tron_address,verify_escrow, Escrow, get_users,getUser,  add_escrow, get_escrow, get_escrows, get_escrows_by_user_id, get_escrows_by_created_by_user_id, get_escrows_by_status, close_escrow


login_manager = LoginManager(app)
login_manager.login_view = "login_page"


class HttpMethod:
    GET: str = "GET"
    POST: str = "POST"

    @classmethod
    def new_request(cls) -> tuple:
        return cls.GET, cls.POST


def add_user(username: str, password: str, tron_address: str, bep20_address: str, telegram_username: str, email: str) -> None:
    # is this first user make admin
    if len(User.query.all()) == 0:
        admin = True
        db.session.add(User(username=username, password=password, tron_address=tron_address, bep20_address=bep20_address, telegram_username=telegram_username, admin=admin, email=email))
        db.session.commit()
        flash("User is created")


    else:
        admin = False
        db.session.add(User(username=username, password=password, tron_address=tron_address, bep20_address=bep20_address, telegram_username=telegram_username, admin=admin, email=email))
        db.session.commit()
        flash("User is created")


@app.route("/")
@app.route("/index.html")
def index() -> str:
    return render_template("index.html", user=current_user)

@app.route("/dashboard", methods=HttpMethod.new_request())
@login_required
def dashboard() -> str:
    return render_template("dashboard.html", session=current_user)
@app.route("/postavke", methods=HttpMethod.new_request())
@login_required
def postavke() -> str:
    return render_template("postavke.html", session=current_user)
@app.route("/create_escrow", methods=HttpMethod.new_request())
@login_required
def create_escrow() -> str:
    if request.method == HttpMethod.POST and "amount"   in request.form:
        amount = request.form.get("amount")
        description = request.form.get("description")
        add_escrow(
            created_by_user=current_user.username,
            created_by_user_id=current_user.id,
            buyer_user_id=0,
            status="created",
            amount=amount,
            description="",
        )
        flash("Escrow is created")
        print("Escrow is created")
        return redirect(url_for("dashboard"))
    else:

        print("Escrow is not created")
        return render_template("create_escrow.html")
@app.route("/escrow/<int:id>", methods=HttpMethod.new_request())
@login_required
def escrow(id: int) -> str:
    escrow = get_escrow(id)
    user_created = getUser(escrow.created_by_user_id)
    user_buyer = getUser(escrow.buyer_user_id)
    print(escrow.created_by_user_id)
    print(user_created)
    print(user_buyer)
    return render_template("escrow.html", escrow=escrow, session=current_user, user_created=user_created, user_buyer=user_buyer)

@app.route("/escrows", methods=HttpMethod.new_request())
@login_required
def escrows() -> str:
    escrows = get_escrows()
    print(escrows)
    return render_template("escrows.html", escrows=escrows)
@app.route("/escrow_cancel/<int:id>", methods=HttpMethod.new_request())
@login_required
def escrow_cancel(id: int) -> str:
    escrow = get_escrow(id)
    if escrow.created_by_user_id == current_user.id:
        close_escrow(id)
        flash("Escrow is canceled")
    else:
        flash("You can't cancel this escrow")
    return redirect(url_for("escrow", id=id))
@app.route("/escrow_accept/<int:id>", methods=HttpMethod.new_request())
@login_required
def escrow_accept(id: int) -> str:
    escrow = get_escrow(id)
    if escrow.created_by_user_id == current_user.id:
        flash("You can't accept this escrow")
        return redirect(url_for("escrow", id=id))
    if escrow.buyer_user_id == 0:
        escrow.buyer_user_id = current_user.id
        escrow.status = "accepted"
        db.session.commit()
        flash("Escrow is accepted")
    else:
        flash("You can't accept this escrow")
    return redirect(url_for("escrow", id=id))
@app.route("/escrow_reject/<int:id>", methods=HttpMethod.new_request())
@login_required
def escrow_reject(id: int) -> str:
    escrow = get_escrow(id)
    if escrow.created_by_user_id == current_user.id:
        escrow.status = "rejected"
        db.session.commit()
        flash("Escrow is rejected")

    else:
        flash("You can't reject this escrow")
    return redirect(url_for("escrow", id=id))
# accept
@app.route("/escrow_approve/<int:id>", methods=HttpMethod.new_request())
@login_required
def escrow_aprove(id: int) -> str:
    escrow = get_escrow(id)
    if escrow.created_by_user_id == current_user.id:
        escrow.status = "approved"
        db.session.commit()
        flash("Escrow is approved")
    else:
        flash("You can't aprove this escrow")
    return redirect(url_for("escrow", id=id))

@app.route("/admin", methods=HttpMethod.new_request())
@login_required
def admin() -> str:
    if current_user.admin:
        return render_template("admin.html", session=current_user, escrows=get_escrows(), users=get_users())

# /user/id
@app.route("/user/<int:id>", methods=HttpMethod.new_request())
@login_required
def user(id: int) -> str:
    if current_user.admin:
        print(getUser(id))
        return render_template("user.html", session=current_user, user=getUser(id), escrows=get_escrows_by_user_id(id))
# escrow_verify
@app.route("/escrow_verify/<int:id>", methods=HttpMethod.new_request())
@login_required
def escrow_verify(id: int) -> str:
    if current_user.admin:
        verify_escrow(id)
        flash("Escrow is verified")
        return redirect(url_for("escrow", id=id))
# escrow_remove
@app.route("/escrow_remove/<int:id>", methods=HttpMethod.new_request())
@login_required
def escrow_remove(id: int) -> str:
    if current_user.admin:
        remove_escrow(id)
        flash("Escrow is removed")
        return redirect(url_for("admin"))

@app.route("/login", methods=HttpMethod.new_request())
def login_page() -> str:
    if request.method == HttpMethod.POST and "username" in request.form:
        user = User.query.filter_by(
            username=request.form.get("username")
        ).first()
        if user:
            if user.password == request.form.get("password"):
                login_user(user)
                return redirect(url_for("dashboard"))
        return "Invalid username or password"
    return render_template("login.html")


@app.route("/logout")
@login_required
def logout_page() -> str:
    logout_user()
    return redirect(url_for("index"))


@app.route("/create_user", methods=HttpMethod.new_request())
def create_user() -> str:
    if request.method == HttpMethod.POST and "username" in request.form:
        username = request.form.get("username")
        password = request.form.get("password")
        tron_address = request.form.get("tron_address")
        bep20_address = request.form.get("bep20_address")
        telegram_username = request.form.get("telegram")
        email = request.form.get("email")
        add_user(username, password, tron_address, bep20_address, telegram_username, email)
        return redirect(url_for("login_page"))
    return render_template("create_user.html")
# new_pass
@app.route("/new_pass", methods=HttpMethod.new_request())
@login_required
def new_pass() -> str:
    if request.method == HttpMethod.POST and "password" in request.form:
        print(request.form.get("password"))
        change_password(current_user.id, request.form.get("password"))
        flash("Password is changed")
        
    return redirect(url_for("dashboard"))
# new email
@app.route("/new_email", methods=HttpMethod.new_request())
@login_required
def new_email() -> str:
    if request.method == HttpMethod.POST and "email" in request.form:
        change_email(current_user.id, request.form.get("email"))
        flash("Email is changed")
        
    return redirect(url_for("dashboard"))
# new_telegram
@app.route("/new_telegram", methods=HttpMethod.new_request())
@login_required
def new_telegram() -> str:
    if request.method == HttpMethod.POST and "telegram" in request.form:
        change_telegram_username(current_user.id, request.form.get("telegram"))
        flash("Telegram is changed")
        
    return redirect(url_for("dashboard"))

# new_tron
@app.route("/new_tron", methods=HttpMethod.new_request())
@login_required
def new_tron() -> str:
    if request.method == HttpMethod.POST and "tron" in request.form:
        change_tron_address(current_user.id, request.form.get("tron"))
        flash("Tron address is changed")
        
    return redirect(url_for("dashboard"))


# new_bep20
@app.route("/new_bep20", methods=HttpMethod.new_request())
@login_required
def new_bep20() -> str:
    if request.method == HttpMethod.POST and "bep20" in request.form:
        change_bep20_address(current_user.id, request.form.get("bep20"))
        flash("Bep20 address is changed")
        
    return redirect(url_for("dashboard"))

# new_pass_a
@app.route("/new_pass_a/<int:id>", methods=HttpMethod.new_request())
@login_required
def new_pass_a(id: int) -> str:
    if current_user.admin:
        if request.method == HttpMethod.POST and "password" in request.form:
            print(request.form.get("password"))
            change_password(id, request.form.get("password"))
            flash("Password is changed")
            
        return redirect(url_for("user", id=id))

# new_email_a
@app.route("/new_email_a/<int:id>", methods=HttpMethod.new_request())
@login_required
def new_email_a(id: int) -> str:
    if current_user.admin:
        if request.method == HttpMethod.POST and "email" in request.form:
            change_email(id, request.form.get("email"))
            flash("Email is changed")
            
        return redirect(url_for("user", id=id))










@login_manager.user_loader
def load_user(user_id: str):
    return User.query.get(int(user_id))

app.run(host="127.0.0.1", port=80, debug=True)
