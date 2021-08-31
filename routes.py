from market import app
from flask import render_template,redirect,url_for, flash, request
from market.models import Item,User
from market.forms import RegisterForm,LoginForm,purchseItemForm,sellItemForm
# we can import from market because db created in __init__.py file
from market import db
from flask_login import login_user,logout_user, login_required, current_user

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/market', methods=['GET','POST'])
@login_required # that line takes automaticaly to the login page. in __init__.py there is line login_manager.login_view = "name of function of the route"
def marketpage():
    purchase_form = purchseItemForm() 
    selling_form = sellItemForm()
    if request.method == 'POST': # if we click on Purchase (in modal)

        ### Purchase Item Logic
        purchased_item = request.form.get('purchased_item')  # grabing the Item that was attempted for purchasing. The name 'purchased_item' came from input name in items_modals.html. 
        p_item_object = Item.query.filter_by(name=purchased_item).first() # we filter the Item object based on the VALUE of purchased_item 
        if p_item_object:  # if p_item_object is not none
            if current_user.can_purchase(p_item_object): # if user budget bigger than the price of item, with help of current_user which we imported.
                p_item_object.buy(current_user) # buy function located in models.py
                flash(f"Congratulation!! You Purchased {p_item_object.name} for {p_item_object.price}$", category='success')
            else:
                flash(f"Sorry, You Dont Have Enough Money To Purchase {p_item_object.name}", category='danger')

        ### Sell Item Logic
        sold_item = request.form.get('sold_item')  # grabing the Item that was attempted for selling. The name 'sold_item' came from input name in items_modals.html.
        s_item_object = Item.query.filter_by(name=sold_item).first() # we filter the Item object based on the VALUE of sold_item
        if s_item_object:  # if s_item_object is not none
            if current_user.can_sell(s_item_object): # if user owen the Item that he wants to sell, with help of current_user which we imported.
                s_item_object.sell(current_user) # sell function located in models.py
                flash(f"Congratulation!! You Sold {s_item_object.name} for {s_item_object.price}$ back to market ", category='success')
            else:
                flash(f"Sorry, something went wrong with selling {s_item_object.name}", category='danger')
        return redirect(url_for('marketpage'))

    if request.method == 'GET': #if we just wnat to see items without purchasing (in my opinion)
        owned_items = Item.query.filter_by(owner=current_user.id)
        items = Item.query.filter_by(owner = None) # After someone purchase item, that item need to disappear
    
    return render_template('market.html',  items=items, purchase_form = purchase_form, owned_items=owned_items, selling_form = selling_form)

@app.route('/register', methods=['GET','POST'])
def registerpage():
    form = RegisterForm()
    # checking if the user click sumbit button
    if form.validate_on_submit():
        user_to_create = User(user_name=form.user_name.data,
        email=form.email_address.data,
        password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account Created Successfuly! Yoa Are Now Logged In As {user_to_create.user_name}" ,category="success")
        return redirect(url_for('marketpage'))
    # if there are no errors from the vlidations
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f"there was an error with createing user: {err_msg}", category = 'danger') #flash is function of flask which prints errors to user
    return render_template('register.html', form = form)

@app.route('/login', methods=['GET','POST'])
def loginpage():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(user_name = form.user_name.data).first()
        # if attempted_user filled and with the help of method we wrote in models.py the passwords are equals
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.user_name}', category='success')
            return redirect(url_for('marketpage'))
        else:
            flash(f'User Name and Password are not match! Please try again!', category='danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logoutpage():
    # we can use this function because we import logout_user and this enough to grab the user and log out
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home"))