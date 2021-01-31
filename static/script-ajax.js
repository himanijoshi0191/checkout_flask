const button = document.querySelector('#buy_now_btn');

button.addEventListener('click', event => {
    fetch('/pay_card')
    .then((result) => { return result.json(); })
    .then((data) => {
        var stripe = Stripe(data.checkout_public_key);
        stripe.redirectToCheckout({
            sessionId: data.checkout_session_id
        }).then(function (result) {
            
        });
    })
});