/**
 * Payment handling script for Kidz Runz.
 * Handles Stripe payment confirmation for booking payments.
 */
(function () {
    'use strict';

    // Ensure Stripe is loaded
    if (typeof Stripe === 'undefined') {
        console.error('Stripe library failed to load');
        return;
    }

    // Initialize Stripe with publishable key from global variable
    // The key is injected via a script tag in payment.html
    const stripePublishableKey = window.STRIPE_PUBLISHABLE_KEY;
    if (!stripePublishableKey) {
        console.error('Stripe Publishable Key is missing');
        return;
    }
    const stripe = Stripe(stripePublishableKey);
    const elements = stripe.elements();
    const card = elements.create('card', {
        style: {
            base: {
                fontSize: '16px',
                color: '#333', // High-contrast color for readability
                '::placeholder': { color: '#aab7c4' },
            },
            invalid: { color: '#dc3545' },
        },
        hidePostalCode: true, // Per UK requirement, no postal code
    });

    // Mount card element
    const cardElement = document.getElementById('card-element');
    if (!cardElement) {
        console.error('Card element not found in DOM');
        return;
    }
    card.mount('#card-element');

    // DOM elements
    const form = document.getElementById('payment-form');
    const submitButton = document.getElementById('submitButton');
    const loader = submitButton.querySelector('.loader');
    const errorElement = document.getElementById('card-errors');

    if (!form || !submitButton || !loader || !errorElement) {
        console.error('Required DOM elements missing');
        return;
    }

    // Payment submission handler
    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        submitButton.disabled = true;
        loader.classList.remove('d-none');

        const clientSecret = document.querySelector('input[name="client_secret"]')?.value;
        if (!clientSecret) {
            errorElement.textContent = 'Client secret is missing. Please reload the page.';
            submitButton.disabled = false;
            loader.classList.add('d-none');
            return;
        }

        try {
            const { error, paymentIntent } = await stripe.confirmCardPayment(clientSecret, {
                payment_method: {
                    card: card,
                    billing_details: {
                        name: form.dataset.name || '',
                        email: form.dataset.email || '',
                        phone: form.dataset.phone || '',
                        address: {
                            city: 'London',
                            country: 'GB',
                        },
                    },
                },
            });

            if (error) {
                errorElement.textContent = error.message;
                console.error('Payment confirmation failed:', error);
            } else if (paymentIntent.status === 'succeeded') {
                form.submit(); // Proceed to server-side confirmation
            } else {
                errorElement.textContent = `Payment status: ${paymentIntent.status}. Please try again.`;
                console.warn('Payment not succeeded:', paymentIntent.status);
            }
        } catch (error) {
            errorElement.textContent = 'An unexpected error occurred. Please try again or contact support.';
            console.error('Unexpected payment error:', error);
        } finally {
            submitButton.disabled = false;
            loader.classList.add('d-none');
        }
    });
})();