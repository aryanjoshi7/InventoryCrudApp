# from flask import Flask, request, jsonify
# import sqlite3
from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/product.db'
app.config['SQLALCHEMY_BINDS'] = {'del' : 'sqlite:////tmp/del.db'}
db = SQLAlchemy(app)

class Productt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    quantity = db.Column(db.Integer)
    category = db.Column(db.String(30))

class Deleted(db.Model):
  __bind_key__ = 'del'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80), unique=False, nullable=False)
  quantity = db.Column(db.Integer)
  category = db.Column(db.String(30))
  comments = db.Column(db.String(200))
  
db.create_all()
  
@app.route('/create' , methods = ['GET','POST'])
def create():
    if request.method == 'GET':
        return render_template('create.html')
    
    if request.method == 'POST':
        id = request.form['product_id']
        name = request.form['name']
        quantity = request.form['quantity']
        category = request.form['category']
        product = Productt(id=id, name=name,quantity= quantity, category = category)
        db.session.add(product)
        db.session.commit()
        return redirect('/')

      
@app.route('/data')
def RetrieveDataList():
    items = Productt.query.all()
    return render_template('multiple.html',items = items)


@app.route('/data/deleted')
def RetrieveDeletedDataList():
    item = Deleted.query.all()
    return render_template('deleteditems.html',item = item)
  
@app.route('/data/<int:id>')
def RetrieveSingleItem(id):
    item = Productt.query.filter_by(id=id).first()
    if item:
        return render_template('single.html', item = item)
    return f"Item with id ={id} doenst exist"

  
@app.route('/data/<int:id>/update',methods = ['GET','POST'])
def update(id):
    item = Productt.query.filter_by(id=id).first()
    if request.method == 'POST':
        if item:
            db.session.delete(item)
            db.session.commit()
 
            name = request.form['name']
            quantity = request.form['quantity']
            category = request.form['category']
            newitem = Productt(id=id, name=name, quantity=quantity, category = category)
 
            db.session.add(newitem)
            db.session.commit()
            return redirect(f'/data/{id}')
        return f"Item with id = {id} doesnt exist"
 
    return render_template('update.html', item = newitem)


@app.route('/data/<int:id>/delete', methods=['GET','POST'])
def delete(id):
    
    item = Productt.query.filter_by(id=id).first()
    if request.method == 'POST':
        if item:
            delemp = Deleted(id = id, name = item.name, quantity = item.quantity, category = item.category, item = request.form['comments'])
            db.session.delete(item)
            db.session.commit()
            db.session.add(delemp)
            db.session.commit()
            return redirect('/data/deleted')
 
    return render_template('delete.html')


@app.route('/data/<int:id>/undelete', methods=['GET','POST'])
def undelete(id):
    
    item = Deleted.query.filter_by(id=id).first()
    if request.method == 'POST':
        if item:
            delemp = Productt(id = id, name = item.name, quantity = item.quantity, category = item.category)
            db.session.delete(item)
            db.session.commit()
            db.session.add(delemp)
            db.session.commit()
            return redirect('/data')
 
    return render_template('undelete.html')

  
@app.route("/")
def index():
    return render_template("home.html")
  
app.run(host='0.0.0.0', port=81)
