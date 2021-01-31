import os
import stripe

from flask import Flask,  render_template, url_for, request, abort

app = Flask(__name__)
app.config['STRIPE_PUBLIC_KEY'] = 'STRIPE_PUBLIC_KEY'
app.config['STRIPE_SECRET_KEY'] = 'STRIPE_SECRET_KEY'

# Set your secret key. Remember to switch to your live secret key in production!
# See your keys here: https://dashboard.stripe.com/account/apikeys

stripe.api_key = app.config['STRIPE_SECRET_KEY'] 

@app.route('/')
def checkout():
    return render_template(
        'checkout.html', 
    )

@app.route('/pay_card')
def pay_card():
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': 'prod_IrT7mfcMsEGPzf',
            'quantity': 1,
        }],
        mode='payment',
        success_url=url_for('success', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=url_for('checkout', _external=True),
    )
    return {
        'checkout_session_id': session['id'], 
        'checkout_public_key': app.config['STRIPE_PUBLIC_KEY']
    }

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/card_pay_webhook', methods=['POST'])
def card_pay_webhook():
    print('Web hook call')

    if request.content_length > 1024 * 1024:
        abort(400)
    payload = request.get_data()
    sig_header = request.environ.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = 'YOUR_ENDPOINT_SECRET'
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        print('Invalid payload')
        return {}, 400
    except stripe.error.SignatureVerificationError as e:
        print('Invalid Signature')
        return {}, 400

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        print(session)
        line_items = stripe.checkout.Session.list_line_items(session['id'], limit=1)
        print(line_items['data'][0]['description'])

    return {}

if __name__== '__main__':
    app.run(debug=True)