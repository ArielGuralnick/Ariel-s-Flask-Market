from sqlalchemy.orm import backref
from market import db # we can do like that because we generated db in __init__ file 
from market import bcrypt # we can do like that because we generated bqrypt in __init__ file 
from market import login_manager # we can do like that because we generated bqrypt in __init__ file 
from flask_login import UserMixin # pressing F12 will open ehat there is inside this class

# each refresh from any page flask aplication need to understand if we loged in or not, 
# (we will need to provide a user_loader callback)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin): # we must UserMixin because there is important functions there
    # !! must to put id when we use modules with flask !!
    id = db.Column(db.Integer(), primary_key = True)
    # Max characters is 30, unpossible null fields, unpossible 2 names or more same names
    user_name = db.Column(db.String(length = 30), nullable = False, unique = True)
    # Max characters is 50, unpossible null fields, unpossible 2 names or more same names
    email = db.Column(db.String(length = 50), nullable = False, unique = True)
    # Max characters is 60, unpossible null fields
    user_password_hash = db.Column(db.String(length = 60), nullable = False)
    # onlt charcaters,  unpossible null fields, every one starts with 10,000$
    budget = db.Column(db.Integer(), nullable = False, default = 10000)
    # backref allow us to specifiy items to users, in other words if we want to check who has Iphone, we can now check that
    # lazy - if we dont set up lazy=true --> SQLAlchemy will not grab all the objects of items in one shot
    items = db.relationship('Item', backref='owned_user', lazy = True)

    @property
    # In this function we add ',' if the budget more then 1000
    def prettier_budget(self):
        if len(str(self.budget)) >= 4:
            return f'{str(self.budget)[:-3]},{str(self.budget)[-3:]}$'
        else:
            return f'{self.budget}$'

    # to crypt our passwords
    @property
    def password(self):
        return self.password

    @password.setter
    def password(self,plain_text_password):
        self.user_password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    # In this function we check if password user wrote equal to passwords which we have
    def check_password_correction(self, attempted_password):
        if bcrypt.check_password_hash(self.user_password_hash, attempted_password):
            return True
    
    # in this function we check if users budget is bigger then price of item which user wants to buy
    def can_purchase(self, Item_obj):
        return self.budget >= Item_obj.price

    # in this function we check if user owen the item that he wants to sell
    def can_sell(self, Item_obj):
        return Item_obj in self.items
            
#This is module which going to be in our database
class Item(db.Model):
    # !! must to put id when we use modules with flask !!
    id = db.Column(db.Integer(), primary_key = True)
    # Max characters is 30, unpossible null fields, unpossible 2 names or more same names
    name = db.Column(db.String(length=30), nullable = False, unique = True)
    # only digits, unpossible null fields 
    price = db.Column(db.Integer(), nullable = False)
    # Max characters is 12, unpossible null fields, unpossible 2 names or more same names
    barcode = db.Column(db.String(length=12), nullable = False, unique = True) 
    # Max characters is 1024, unpossible null fields, unpossible 2 names or more same names
    description = db.Column(db.String(length=1024), nullable = False, unique = True)
    # ForeignKey search for the primary key of our model from the model that is realted to. 
    # because of 'user.id' the row related to each uniqe row that is going to be stored in that id.
    # !! it is very importand to write 'user.id' in lower case    
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def buy(self,current_user): #self is p_item_object
        # we need to put .id becauser in owner which we created in Item (in models) we put id
        self.owner = current_user.id 
        # after user buy something we need to decrease his budget
        current_user.budget = current_user.budget - self.price
        db.session.commit()

    def sell(self,current_user): #self is s_item_object
        # None - opposite action of adding owenrship, ae assign ownership to nobody
        self.owner = None 
        # after user sell something we need to increase his budget
        current_user.budget = current_user.budget + self.price
        db.session.commit()
    
    # function which prints the name of Item
    def __repr__(self):
        return f'Item {self.name}'