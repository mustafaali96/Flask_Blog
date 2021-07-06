from flask import render_template, url_for, flash, redirect,request
from werkzeug.security import generate_password_hash, check_password_hash
from flaskblog import app, db, bcrypt
from flaskblog.forms import *
from flaskblog.models import Collection, User, Order, Size, CustomSize
from flask_login import login_user, current_user, logout_user, LoginManager 
from datetime import datetime
import os


@app.route("/register/", methods=['GET','POST'])
def register():
    form = UserRegistrationForm()
    if request.method == 'POST':
        user = User(firstname=form.firstname.data, lastname=form.lastname.data, username=form.username.data, shop_name=form.shop_name.data, number=form.number.data, address=form.address.data, password=form.password.data, user_type=form.user_type.data, is_embroidery=form.embroidery.data, is_partywear=form.partywear.data,is_dailywear=form.dailywear.data, is_modestwear=form.modestwear.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to login', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='SignUp', form=form)

login_manager = LoginManager()
# login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)
    
    
@app.route("/")
def home():
    if current_user.is_authenticated:
        if current_user.user_type == 0 or current_user.user_type == 2:
            return redirect(url_for('customer_dashboard'))
        elif current_user.user_type == 1:
            return redirect(url_for('dashboard'))
    else:
        all_collections = Collection.query.all()
    return render_template('home.html', title='home', all_collections=all_collections)

@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('home'))

#login
@app.route("/login/", methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.username.data).first()
        if user:              # is user exist
            if user.password==form.password.data and user.username==form.username.data:
                user.is_authenticated = True                   #for login session
                login_user(user)
                if user.user_type == 0 or user.user_type == 2:
                    flash('Login Successful!!', 'success')
                    return redirect(url_for('customer_dashboard'))    #customer dashboad

                elif user.user_type == 1:
                    flash('Login Successful!!', 'success')
                    return redirect(url_for('dashboard'))

                else:
                    flash('Login Unsuccessful, Please check your username and password', 'danger')
            else:
                flash('Login Unsuccessful, Password did not matched', 'danger')
                
        else:
            flash('User not exist, Please check your username and password', 'danger')
    return render_template('login.html', title='Login', form=form)



# tailorsdashboard
@app.route("/dashboard/")
def dashboard():
    if request.method == 'GET':
        if current_user.is_authenticated:
            if current_user.user_type == 1:
                collections = Collection.query.filter(Collection.user_id==current_user.id).all()
                collectionIDs = []
                for collection in collections:
                    collectionIDs.append(collection.id)
                orders_count = Order.query.filter(Order.collection_id.in_(collectionIDs), Order.Is_Order_confirmed==False, Order.Is_Order_rejected==False).all()
                all_orders_count = Order.query.filter(Order.collection_id.in_(collectionIDs)).all()
            else:
                flash('Login Unsuccessful, Please login with Tailor account', 'danger')
                return redirect(url_for('login'))

    return render_template('dashboard.html', title='dashboard', orders_count=len(orders_count), all_orders_count=len(all_orders_count))

# Customer Dashboard
@app.route("/customer/")
def customer_dashboard():
    return render_template('customerdashboard.html', title='Customer') 

app.config['UPLOAD_PATH'] = '/home/omama/Desktop/Flask_Blog/flaskblog/static/profile_pics'
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif', '.PNG',  '.JPG']

@app.route('/update/profile/', methods=['GET','POST'])
def update_profile():
    user_form = lambda user_type : UpdateTailorAccountForm() if (user_type==1) else UpdateCustomerAccountForm()
    form= user_form(current_user.user_type)
    if request.method == 'POST':
        uploaded_file = request.files['image']
        filename = uploaded_file.filename
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                abort(400) 
            uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        if current_user.user_type==1:
            current_user.imagefile = filename
            current_user.firstname = form.firstname.data
            current_user.lastname = form.lastname.data
            current_user.username = form.username.data
            current_user.number = form.number.data
            current_user.shop_name = form.shop_name.data
            current_user.address = form.address.data
            # current_user.password = form.password.data
            current_user.is_embroidery = form.embroidery.data
            current_user.is_partywear = form.partywear.data
            current_user.is_dailywear = form.dailywear.data
            current_user.is_modestwear = form.modestwear.data
        else:
            current_user.imagefile = filename
            current_user.firstname = form.firstname.data
            current_user.lastname = form.lastname.data
            current_user.username = form.username.data
            current_user.number = form.number.data
            current_user.address = form.address.data
            # current_user.password = form.password.data

        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('update_profile'))
    elif request.method == 'GET':
        if current_user.user_type==1:
            form.firstname.data = current_user.firstname
            form.lastname.data = current_user.lastname
            form.username.data = current_user.username
            form.number.data = current_user.number
            form.shop_name.data = current_user.shop_name
            form.address.data = current_user.address
            # form.password.data = current_user.password
            form.embroidery.data = current_user.is_embroidery
            form.partywear.data = current_user.is_partywear
            form.dailywear.data = current_user.is_dailywear
            form.modestwear.data = current_user.is_modestwear
        else:
            form.firstname.data = current_user.firstname
            form.lastname.data = current_user.lastname
            form.username.data = current_user.username
            form.number.data = current_user.number    
            # form.password.data = current_user.password            
            form.address.data = current_user.address

    imagefile = url_for('static', filename='profile_pics/' + current_user.imagefile)
    return render_template('updateProfile.html', title='updateProfile', 
                                    imagefile=imagefile, form=form)


#add tailor product
@app.route('/dashboard/collections/add/', methods=['GET','POST'])
def add_collection():
    app.config['UPLOAD_PATH'] = '/home/omama/Desktop/Flask_Blog/flaskblog/static/abayacollection'
    app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif', '.PNG',  '.JPG']
    form = AddCollectionForm()
    if request.method == 'POST':
        uploaded_file = request.files['product_image']
        filename = uploaded_file.filename
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                abort(400) 
            uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))

        collection=Collection(user_id=current_user.id, created_at=datetime.now(), updated_at=datetime.now(), title=form.title.data, price=form.price.data, is_embroidery=form.embroidery.data, is_partywear=form.partywear.data,is_dailywear=form.dailywear.data, is_modestwear=form.modestwear.data, fabric=form.fabric.data, product_image=filename, description=form.description.data, category=form.category.data)
        print(collection)
        db.session.add(collection)
        db.session.commit()
        flash('Your product has been updated!', 'success')
        return redirect(url_for('collections'))
        # product_image = url_for('static', filename='collections/')
    return render_template('addcollection.html', title='Add Collection', form=form)


#tailor collections
@app.route('/dashboard/collections/', methods=['GET','POST'])
def collections():
    app.config['UPLOAD_PATH'] = '/home/omama/Desktop/Flask_Blog/flaskblog/static/abayacollection'
    app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif', '.PNG',  '.JPG']

    if request.method == 'GET':
        if current_user.is_authenticated:
            if current_user.user_type == 1:
                collections = Collection.query.filter(Collection.user_id==current_user.id).all()
            else:
                collections = Collection.query.all()
        else:
            collections = Collection.query.all()
        # imagefile = url_for('static', filename='abayacollection/' + current_user.imagefile)
    return render_template('collection.html', title='Tailor Collections', collections=collections)


# tailor order
@app.route('/dashboard/orders/', methods=['GET','POST'])
def order():
    if request.method == 'GET':
        if current_user.is_authenticated:
            if current_user.user_type == 1:
                collections = Collection.query.filter(Collection.user_id==current_user.id).all()
                collectionIDs = []
                for collection in collections:
                    collectionIDs.append(collection.id)
                orders = Order.query.filter(Order.collection_id.in_(collectionIDs), Order.Is_Order_confirmed==False, Order.Is_Order_rejected==False).all()
            elif current_user.user_type == 0 or current_user.user_type == 2:
                orders = Order.query.filter(Order.customer_id==current_user.id).all()
            else:
                return redirect(url_for('login'))
        else:
            return redirect(url_for('login'))

    if request.method == 'POST':
        if current_user.is_authenticated:
            if current_user.user_type == 1:
                try:
                    order_id = request.form.get('confirm_order')
                    Order.query.filter_by(id=int(order_id)).update(dict(Is_Order_confirmed = True))
                except:
                    order_id = request.form.get('reject_order')
                    Order.query.filter_by(id=int(order_id)).update(dict(Is_Order_rejected = True))
                db.session.commit()
                return redirect(url_for('order'))
            elif current_user.user_type == 0 or current_user.user_type == 2:
                order_id = request.form.get('delete_order')
                Order.query.filter(Order.id == int(order_id)).delete()
                db.session.commit()
                return redirect(url_for('order'))
            else:
                return redirect(url_for('login'))
        else:
            return redirect(url_for('login'))
    return render_template('order.html', title='Tailor Orders', orders=orders)

# tailor order
@app.route('/dashboard/allOrders/', methods=['GET','POST'])
def all_order():
    if request.method == 'GET':
        if current_user.is_authenticated:
            if current_user.user_type == 1:
                collections = Collection.query.filter(Collection.user_id==current_user.id).all()
                collectionIDs = []
                for collection in collections:
                    collectionIDs.append(collection.id)
                orders = Order.query.filter(Order.collection_id.in_(collectionIDs)).all()
            else:
                return redirect(url_for('login'))
        else:
            return redirect(url_for('login'))  
    return render_template('allOrder.html', title='Tailor Orders', orders=orders)


@app.route('/collections/<collection_id>/', methods=['GET','POST'])
def collection_detail(collection_id):
    form = OrderForm()
    if request.method == 'GET':
        collection = Collection.query.filter(Collection.id==collection_id)[0]
        sizes = Size.query.filter(Size.category==collection.category).all()
        my_customsize = CustomSize.query.filter(CustomSize.customer_id==current_user.id, CustomSize.category==collection.category).all()

    if request.method == 'POST':
        collection = Collection.query.filter(Collection.id==collection_id)[0]
        sizes = Size.query.filter(Size.category==collection.category).all()
        my_customsize = CustomSize.query.filter(CustomSize.customer_id==current_user.id, CustomSize.category==collection.category).all()
        if current_user.is_authenticated:
            if current_user.user_type == 0 or current_user.user_type == 1:
                Length = request.form["length"]
                width = request.form["width"]
                Shoulder = request.form["shoulder"]
                Armhole = request.form["armhole"]
                Sleeves = request.form["sleeves"]
                Chest = request.form["chest"]
                quantity = request.form["quantity"]
                order=Order(customer_id=current_user.id, order_created_at=datetime.now(), collection_id=collection_id, Length=Length, width=width, Shoulder=Shoulder, Armhole=Armhole, Sleeves=Sleeves, Chest=Chest, quantity=quantity)
                db.session.add(order)
                db.session.commit()
                flash('Your order has been placed!', 'success')
                return redirect(url_for('collections'))
            
            else:
                customsizes = CustomSize.query.filter(CustomSize.customer_id==current_user.id, CustomSize.category==collection.category).all()
                if len(customsizes) >= 1:
                    for customsize in customsizes:
                        order=Order(customer_id=current_user.id, order_created_at=datetime.now(), collection_id=collection_id, Length=customsize.Length, width=customsize.width, Shoulder=customsize.Shoulder, Armhole=customsize.Armhole, Sleeves=customsize.Sleeves, Chest=customsize.Chest)
                        db.session.add(order)
                        db.session.commit()
                    flash('Your bulk order has been placed!', 'success')
                    return redirect(url_for('collections'))
                else:
                    if collection.category == 0:
                        flash('No Abaya size found for bulk order!', 'danger')
                    else:
                        flash('No Hijab size found for bulk order!', 'danger')
                    return redirect(url_for('collections'))
        else:
            flash('Please login yourself first!', 'danger')
            return redirect(url_for('login'))

    return render_template('collectioninfo.html', title='Details', collection=collection, form=form, sizes=sizes, my_customsize=my_customsize)


@app.route('/<collection_id>/', methods=['GET','POST'])
def guest_collection_detail(collection_id):
    form = OrderForm()
    collection = Collection.query.filter(Collection.id==collection_id)[0]
    sizes = Size.query.filter(Size.category==collection.category).all()
    if request.method == 'GET':
        # print(current_user.id)
        collection = Collection.query.filter(Collection.id==collection_id)[0]
    if request.method == 'POST':
        return redirect(url_for('login')) 

    return render_template('collectioninfo.html', title='Details', collection=collection, form=form, sizes=sizes)
 

@app.route("/size/", methods=['GET','POST'])
def CustomerCustomSize():
    if request.method == 'GET':
        customsizes = CustomSize.query.filter(CustomSize.customer_id==current_user.id).all()
    if request.method == 'POST':
        if current_user.is_authenticated:
            customsize_id = request.form.get('customsize')
            CustomSize.query.filter_by(id=int(customsize_id)).delete()
            db.session.commit()
            return redirect(url_for('CustomerCustomSize'))
        else:
            flash('Please login yourself first!', 'danger')
            return redirect(url_for('login'))

    return render_template('size.html', title='Details', customsizes=customsizes)

@app.route("/size/add/", methods=['GET','POST'])
def AddCustomSize():
    form = CustomSizeForm()
    if request.method == 'GET':
        form = CustomSizeForm()
    if request.method == 'POST':
        if current_user.is_authenticated:
            name = request.form["name"]
            relation = request.form["relation"]
            category = request.form["category"]
            Length = request.form["Length"]
            width = request.form["width"]
            Shoulder = request.form["Shoulder"]
            Armhole = request.form["Armhole"]
            Sleeves = request.form["Sleeves"]
            Chest = request.form["Chest"]
            customSize = CustomSize(customer_id=current_user.id, name=name, relation=relation, category=category, Length=Length, width=width, Shoulder=Shoulder, Armhole=Armhole, Sleeves=Sleeves, Chest=Chest)
            db.session.add(customSize)
            db.session.commit()
            flash('Your size has been added!', 'success')
            return redirect(url_for('CustomerCustomSize'))
        else:
            flash('Please login yourself first!', 'danger')
            return redirect(url_for('login'))
    return render_template('addsize.html', title='My Size', form=form)

@app.route("/size/<customsize_id>/", methods=['GET','POST'])
def EditCustomSize(customsize_id):
    form = CustomSizeForm()
    customsize = CustomSize.query.filter(CustomSize.id==customsize_id)[0]
    if request.method == 'GET':
        form.name.data = customsize.name
        form.relation.data = customsize.relation
        form.category.data = customsize.category
        form.Length.data = customsize.Length
        form.width.data = customsize.width
        form.Shoulder.data = customsize.Shoulder
        form.Armhole.data = customsize.Armhole
        form.Sleeves.data = customsize.Sleeves
        form.Chest.data = customsize.Chest

    if request.method == 'POST':
        if current_user.is_authenticated:
            name = request.form["name"]
            relation = request.form["relation"]
            Length = request.form["Length"]
            width = request.form["width"]
            Shoulder = request.form["Shoulder"]
            Armhole = request.form["Armhole"]
            Sleeves = request.form["Sleeves"]
            Chest = request.form["Chest"]
            CustomSize.query.filter_by(id=int(customsize_id)).update(dict(name=name, relation=relation, Length=Length, width=width, Shoulder=Shoulder, Armhole=Armhole, Sleeves=Sleeves, Chest=Chest))
            db.session.commit()
            flash('Your size has been updated!', 'success')
            return redirect(url_for('CustomerCustomSize'))
        else:
            flash('Please login yourself first!', 'danger')
            return redirect(url_for('login'))

    return render_template('editsize.html', title='Edit Size', form=form, customsize=customsize)


@app.route('/filter/<filter_type>/', methods=['GET','POST'])
def filter_collection(filter_type):
    if request.method == 'GET':
        filters = { filter_type : True }
        filter_collection = Collection.query.filter_by(**filters)
    return render_template('filtercollection.html', title='Details', filter_collection=filter_collection)

#sortbylatest
@app.route('/filter/<order_by>/', methods=['GET','POST'])
def order_collection(order_by):
    if request.method == 'GET':
        filters = { order_by : True }
        # order_collection = Collection.query.order_by(desc(collection.title))
        order_collection = Collection.query.order_by(Collection.title).all()
    return render_template('filtercollection.html', title='Details', order_collection=order_collection)


@app.route('/filterTailor/<filter_user>/', methods=['GET','POST'])
def filter_tailor(filter_user):
    if request.method == 'GET':
        filter_collection = Collection.query.filter(Collection.user_id==filter_user).all()
    return render_template('filtercollection.html', title='Details', filter_collection=filter_collection)

@app.route('/about/')
def about():
    return render_template('about.html', title='About Us')

@app.route('/contact/')
def contact_us():
    return render_template('contactus.html', title='Contact Us')

#customerdashboard
# @app.route("/c/dashboard")
# def customerdashboard():
#     return render_template('customerdashboard.html', title='customerdashboard')

# app.config['UPLOAD_PATH'] = '/home/omama/Desktop/Flask_Blog/flaskblog/static/profile_pics'
# app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif', '.PNG',  '.JPG']

# # @app.route('/c/update/profile', methods=['GET','POST'])
# def cupdate_profile():
#     form = UpdateCustomerAccountForm()
#     if request.method == 'POST':

#         uploaded_file = request.files['image']
#         filename = uploaded_file.filename
#         if filename != '':
#             file_ext = os.path.splitext(filename)[1]
#             if file_ext not in app.config['UPLOAD_EXTENSIONS']:
#                 abort(400) 
#             uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
#         current_user.imagefile = filename
#         current_user.firstname = form.firstname.data
#         current_user.lastname = form.lastname.data
#         current_user.username = form.username.data
#         current_user.number = form.number.data
#         # current_user.shop_name = form.shop_name.data
#         current_user.address = form.address.data
#         # current_user.is_embroidery = form.embroidery.data
#         # current_user.is_partywear = form.partywear.data
#         # current_user.is_dailywear = form.dailywear.data
#         # current_user.is_shrugs = form.shrugs.data

#         # print(is_partywear)
#         # print(is_shrugs)
#         # if current_user.embroidery:
#         #   is_embroidery = form.embroidery.data

#         # elif current_user.partywear:
#         #   is_partywear = form.partywear.data

#         # elif current_user.shrugs:
#         #   is_shrugs = form.shrugs.data
#         # here add skills:
#         db.session.commit()
#         flash('Your account has been updated!', 'success')
#         return redirect(url_for('cupdate_profile'))
#     elif request.method == 'GET':
#         form.firstname.data = current_user.firstname
#         form.lastname.data = current_user.lastname
#         form.username.data = current_user.username
#         form.number.data = current_user.number
#         # form.shop_name.data = current_user.shop_name
#         form.address.data = current_user.address
#         # form.embroidery.data = current_user.is_embroidery
#         # form.partywear.data = current_user.is_partywear
#         # form.dailywear.data = current_user.is_dailywear
#         # form.shrugs.data = current_user.is_shrugs

#         # print(is_partywear)
#         # print(is_shrugs)
#         # elif form.partywear.data:
#         #   is_partywear = current_user.partywear

#         # elif form.shrugs.data:
#         #   is_shrugs = current_user.shrugs
#         # here add skills:
#     imagefile = url_for('static', filename='profile_pics/' + current_user.imagefile)
#     return render_template('customerupdateprofile.html', title='customerupdateProfile', 
#                                     imagefile=imagefile, form=form)

            
        # price = request.form["price"]
        # title = request.form["title"]
        # tname = request.form["tname"]
        # fabric = request.form["fabric"]
        # date_posted = request.form["date_posted"]
        # product_image = request.form["product_image"]
        # description = request.form["description"]
        # if  form.price.data:
        #   price = form.price.data
        # if form.title.data:
        #   title = form.title.data
        # if form.tname.data:
        #   tname = form.tname.data
        # if form.fabric.data:
        #   fabric = form.fabric.data
        # if form.date_posted.data:
        #   date_posted = form.date_posted.data
        # if form.product_image.data:
        #   product_image = form.product_image.data
        # if form.description.data:
        #   description = form.description.data
                


        
    # elif request.method == 'GET':
    #   form.tname.data = current_user.tname
    

# @app.route("/add/product")
# def AddProduct():
#   form = AddProductForm()
#   return render_template('tcollections.html', title='Add Product', form=form)
# @app.route('/addproduct')
# def AddProduct():
#   # form = AddProductForm()
#   return render_template('addproduct.html')


        



#customerside


# @app.route("/c/register", methods=['GET','POST'])
# def addcustomer():
    # form = RegistrationForm()
    # if current_user.is_authenticated:
    #   return redirect(url_for('home'))
    # form = RegistrationForm()
    # if request.method == 'POST': 
    #   user_type = 0
    #   if form.user_type.data == "True":
    #       user_type = form.user_type.data 

    #   if form.firstname.data:
    #       cfirstname = form.firstname.data
    #   # elif form.username.data:
    #   #   cusername = form.username.data
    #   # elif form.lastname.data:
    #   #   clastname = form.lastname.data
    #   # elif form.number.data:
    #   #   cnumber = form.number.data
    #   # elif form.address.data:
    #   #   caddress = form.address.data
    #   # elif form.password.data:
    #   #   cpassword = form.password.data
        

    #   customer = Customer(cfirstname=form.firstname.data, clastname=form.lastname.data, cusername=form.username.data, cnumber=form.number.data, caddress=form.address.data, cpassword=form.password.data, user_type=form.user_type.data)
    #   print(customer)
    #   db.session.add(customer)
    #   db.session.commit()
    #   flash('Your account has been created! You are now able to login', 'success')
    #   return redirect(url_for('login'))
    # return render_template('register.html', title='SignUp', form=form)





# Tailor Side

# registertailor
# @app.route("/register", methods=['GET','POST'])
# def register():
#   form = RegistrationForm()
#   if current_user.is_authenticated:
#       return redirect(url_for('home'))
    
#   if request.method == 'POST': 
#       try:
#           form = RegistrationForm()
#       # user_type = 1
#       # if form.user_type.data == "True":
#       #   user_type = form.user_type.data

#           if form.embroidery.data:
#               is_embroidery = form.embroidery.data

#           elif form.partywear.data:
#               is_partywear = form.partywear.data


#           elif form.dailywear.data:
#               is_dailywear = form.dailywear.data
                    

#           elif form.shrugs.data:
#               is_shrugs = form.shrugs.data
                    

#           tailor = Tailor(firstname=form.firstname.data, lastname=form.lastname.data, username=form.username.data, shop_name=form.shop_name.data, number=form.number.data, address=form.address.data, password=form.password.data, is_embroidery=form.embroidery.data, is_partywear=form.partywear.data,is_dailywear=form.dailywear.data, is_shrugs=form.shrugs.data)
#           print(tailor)
#           db.session.add(tailor)
#           db.session.commit()
#           flash('Your account has been created! You are now able to login', 'success')
#           return redirect(url_for('login'))


    

#       except: 
#           form = CustomerRegistrationForm()
            
#           if form.firstname.data:
#               cfirstname = form.firstname.data
            
            

#           customer = Customer(cfirstname=form.firstname.data, clastname=form.lastname.data, cusername=form.username.data, cnumber=form.number.data, caddress=form.address.data, cpassword=form.password.data)
#           print(customer)
#           db.session.add(customer)
#           db.session.commit()
#           flash('Your account has been created! You are now able to login', 'success')
#           return redirect(url_for('login'))
#   return render_template('register.html', title='SignUp', form=form)









