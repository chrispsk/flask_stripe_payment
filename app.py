from flask import Flask, render_template, request, redirect, url_for
import stripe

app = Flask(__name__)
public_key = "pk_test_TYooMQauvdEDq54NiTphI7jx"
stripe.api_key = "sk_test_4eC39HqLyjWDarjtT1zdp7dc"
@app.route('/')
def index():
    return render_template('index.html', public_key=public_key)


@app.route('/payment', methods=['POST'])
def payment():
    suma = 1999
    customer = stripe.Customer.create(email=request.form['stripeEmail'], source = request.form['stripeToken'])
    charge = stripe.Charge.create(
    customer=customer.id,
    amount=suma,
    currency='usd'
    )

    return render_template("thankyou.html", suma=suma/100)

if __name__ == '__main__':
    app.run()
