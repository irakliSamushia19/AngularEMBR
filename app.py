from flask import Flask, render_template
import sqlite3
from sqlalchemy import desc
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy, SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///embroidery.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Clothes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<Clothes {self.title}>'


# new_clothes = Clothes(
#     category='New',
#     name='Shirt',
#     price=29.99,
#     image='https://static.goldengoose.com/image/upload/w_auto,c_scale,f_auto,q_auto/v1666349874/Style/ECOMM/GMP01220.P000865-11443-9'
# )

# with app.app_context():
#     db.session.add(new_clothes)
#     db.session.commit()


@app.route('/')
def hello_world():
    category = 'New'
    clothes = Clothes.query.filter_by(category=category).order_by(desc(Clothes.id)).limit(6).all()
    return render_template('main.html', category=category, clothes=clothes
                           )


@app.route('/get_content/<category>')
def get_content(category='New'):
    if category == 'Men':
        category = 'Men'
    elif category == 'New':
        category = 'New'
    elif category == 'Women':
        category = 'Women'

    clothes = Clothes.query.filter_by(category=category).all()

    return render_template('main.html', category=category, clothes=clothes)


@app.route('/get_content/<category>/<int:product_id>')
def view_product(category, product_id):
    product = Clothes.query.get(product_id)

    if product:
        return render_template('product_details.html', category=category, product=product)
    else:
        return "Product not found"


if __name__ == '__main__':
    app.run(debug=True)
