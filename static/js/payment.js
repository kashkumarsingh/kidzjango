document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('payment-form');
    if (!form) return;

    const stripePublishableKey = window.STRIPE_PUBLISHABLE_KEY;
     if (!stripePublishableKey) {
        console.error("Stripe key not set.");
        return;
    }
    const name = form.dataset.name;
    const email = form.dataset.email;
    const phone = form.dataset.phone;

    const stripe = Stripe(stripePublishableKey);
    const elements = stripe.elements();

    const card = elements.create('card', {
        style: {
            base: {
                fontSize: '16px',
                color: '#333',
                '::placeholder': { color: '#aab7c4' },
            },
            invalid: { color: '#dc3545' },
        },
        hidePostalCode: true,
    });
    card.mount('#card-element');

    const submitButton = document.getElementById('submitButton');
    const loader = submitButton.querySelector('.loader');
    const errorElement = document.getElementById('card-errors');

    form.addEventListener('submit', async function (e) {
        e.preventDefault();
        submitButton.disabled = true;
        loader.classList.remove('d-none');

        const clientSecret = document.querySelector('input[name="client_secret"]').value;

        const { error, paymentIntent } = await stripe.confirmCardPayment(clientSecret, {
            payment_method: {
                card: card,
                billing_details: {
                    name: name,
                    email: email,
                    phone: phone,
                    address: {
                        city: 'London',
                        country: 'GB'
                    }
                }
            }
        });

        if (error) {
            errorElement.textContent = error.message;
            console.error(error);
            submitButton.disabled = false;
            loader.classList.add('d-none');
        } else if (paymentIntent && paymentIntent.status === 'succeeded') {
            form.submit();
        } else {
            errorElement.textContent = `Payment status: ${paymentIntent?.status || 'unknown'}`;
            submitButton.disabled = false;
            loader.classList.add('d-none');
        }
    });
});
