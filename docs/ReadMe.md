kidzjango/
├── config/
│   ├── __pycache__/
│   ├── __init__.py (artifact_id: config_init_j9t0u1v2-3w4x-5y6z-7a8b, version_id: v1)
│   ├── asgi.py (artifact_id: asgi_k0u1v2w3-4x5y-6z7a-8b9c, version_id: v1)
│   ├── settings.py (artifact_id: settings_l1v2w3x4-5y6z-7a8b-9c0d, version_id: v3)
│   ├── urls.py (artifact_id: urls_m2w3x4y5-6z7a-8b9c-0d1e, version_id: v2)
│   ├── wsgi.py (artifact_id: wsgi_n3x4y5z6-7a8b-9c0d-1e2f, version_id: v1)
├── core/
│   ├── __pycache__/
│   ├── migrations/
│   ├── management/
│       ├── commands/
            ├── sendtestmail.py (needed new artifacts_id)
│   ├── templates/
│       ├── core/
            ├── cancel_booking.html (needed new artifacts_id)
            ├── choose_package.html (artifact_id: 16e833c7-a447-43d5-af5e-6f8a2809ff4e)
            ├── email_admin_notification.html (needed new artifacts_id)
            ├── email_visitor_confirmation.html (needed new artifacts_id)
│   │   │   ├── thank_you.html (artifact_id: b9caeace-44ab-4e37-a6ec-f864df615e2d)
│   ├── __init__.py (artifact_id: core_init_1a2b3c4d-5e6f-7g8h-9i0j, version_id: v1)
│   ├── admin.py (artifact_id: core_admin_3c4d5e6f-7g8h-9i0j-1k2l, version_id: v1)
    ├── apps.py (artifact_id: core_apps_4d5e6f7g-8h9i-0j1k-2l3m, version_id: v1)
│   ├── context_processors.py (artifact_id: core_context_9i0j1k2l-3m4n-5o6p-7q8r, version_id: v1)
    ├── models.py (artifact_id: core_models_2b3c4d5e-6f7g-8h9i-0j1k, version_id: v1)
│   ├── tests.py (artifact_id: core_test_5e6f7g8h-9i0j-1k2l-3m4n, version_id: v1)
│   ├── urls.py (artifact_id: core_test_5e6f7g8h-9i0j-1k2l-3m4n, version_id: v1)
│   ├── views.py (artifact_id: core_test_5e6f7g8h-9i0j-1k2l-3m4n, version_id: v1)
├── frontend/
│   ├── __pycache__/
│   ├── __init__.py (artifact_id: init_1a2b3c4d-5e6f-7g8h-9i0j, version_id: v1)
│   ├── views.py (artifact_id: frontend_views_6f7g8h9i-0j1k-2l3m-4n5o, version_id: v1)
│   ├── urls.py (artifact_id: frontend_urls_7g8h9i0j-1k2l-3m4n-5o6p, version_id: v1)
│   ├── apps.py (artifact_id: frontend_apps_8h9i0j1k-2l3m-4n5o-6p7q, version_id: v1)
│   ├── test.py (artifact_id: frontend_test_9i0j1k2l-3m4n-5o6p-7q8r, version_id: v1)
│   ├── templates/
│   │   ├── frontend/
│   │   │   ├── about.html (artifact_id: e2f9a4b1-9d2c-4a3e-8e7b-2f1c8d9e0a4b, version_id: v2)
│   │   │   ├── activities.html (artifact_id: activities_4d5e6f7g-8h9i-0j1k-2l3m, version_id: v1)
│   │   │   ├── benefits.html (artifact_id: benefits_5e6f7g8h-9i0j-1k2l-3m4n, version_id: v1)
│   │   │   ├── bookings.html (artifact_id: e50ac4ad-1826-4eb1-96e5-b7c465b3479c, version_id: v2)
│   │   │   ├── cams.html (artifact_id: cams_6f7g8h9i-0j1k-2l3m-4n5o, version_id: v1)
│   │   │   ├── communication.html (artifact_id: comm_7g8h9i0j-1k2l-3m4n-5o6p, version_id: v1)
│   │   │   ├── contact.html (artifact_id: 7caa725d-1c9b-40f7-bd48-81984a743a85, version_id: 8b17741e-7d3b-4ab5-8bbe-3b2e418a6484)
│   │   │   ├── explore.html (artifact_id: explore_8h9i0j1k-2l3m-4n5o-6p7q, version_id: v1)
│   │   │   ├── faqs.html (artifact_id: faqs_a0j1k2l3-4m5n-6o7p-8q9r, version_id: v1)
│   │   │   ├── home.html (artifact_id: dade429d-1370-42c7-bd04-1d86ea563375, version_id: v3)
│   │   │   ├── mission.html (artifact_id: mission_9i0j1k2l-3m4n-5o6p-7q8r, version_id: v1)
│   │   │   ├── parent_tips.html (artifact_id: tips_a0j1k2l3-4m5n-6o7p-8q9r, version_id: v1)
│   │   │   ├── safeguarding.html (artifact_id: safeguard_b1l2m3n4-5o6p-7q8r-9s0t, version_id: v1)
│   │   │   ├── services.html (artifact_id: f2d21d61-c279-4dee-a595-3f39a8c52b17, version_id: 3ac04ec5-f937-4a3e-bcf6-8449b6e7bbb4)
│   │   │   ├── story.html (artifact_id: story_c2m3n4o5-6p7q-8r9s-0t1u, version_id: v1)
│   │   │   ├── welcome.html (artifact_id: welcome_d3n4o5p6-7q8r-9s0t-1u2v, version_id: v1)
│   │   │   ├── pricing_packages.html (needed an newly generated artifact_id)
├── accounts/  # To be created later
│   ├── __pycache__/
│   ├── migrations/
│   ├── __init__.py (artifact_id: accounts_init_e5o5p6q7-8r9s-0t1u-2v3w, version_id: v1)
│   ├── models.py (artifact_id: accounts_models_f6p6q7r8-9s0t-1u2v-3w4x, version_id: v1)
│   ├── forms.py (artifact_id: accounts_forms_g7q7r8s9-0t1u-2v3w-4x5y, version_id: v1)
│   ├── views.py (artifact_id: accounts_views_h8r8s9t0-1u2v-3w4x-5y6z, version_id: v1)
│   ├── urls.py (artifact_id: accounts_urls_i9s9t0u1-2v3w-4x5y-6z7a, version_id: v1)
│   ├── admin.py (artifact_id: accounts_admin_j0t0u1v2-3w4x-5y6z-7a8b, version_id: v1)
│   ├── apps.py (artifact_id: accounts_apps_k1u1v2w3-4x5y-6z7a-8b9c, version_id: v1)
│   ├── test.py (artifact_id: accounts_test_l2v2w3x4-5y6z-7a8b-9c0d, version_id: v1)
│   ├── templates/
│   │   ├── accounts/
│   │   │   ├── login.html (artifact_id: login_m3w3x4y5-6z7a-8b9c-0d1e, version_id: v1)
│   │   │   ├── signup.html (artifact_id: signup_n4x4y5z6-7a8b-9c0d-1e2f, version_id: v1)
│   │   │   ├── dashboard.html (artifact_id: dashboard_o5y5z6a7-8b9c-0d1e-2f3g, version_id: v1)
├── logs/
├── static/
│   ├── css/
│   │   └── custom.css (artifact_id: 2afedfa1-9503-48f1-a372-af1845b2ea33, version_id: ba6fccf1-6c4f-4a7a-9068-c04bbb7e9228)
│   ├── images/ (artifact_id: images_u0e1f2g3-4h5i-6j7k-8l9m, version_id: v1)
│   ├── js/ (artifact_id: js_v1f2g3h4-5i6j-7k8l-9m0n, version_id: v1)
├── templates/
│   ├── partials/
│   │   ├── _footer.html (artifact_id: footer_e4o5p6q7-8r9s-0t1u-2v3w, version_id: v1)
│   │   ├── _header.html (artifact_id: header_f5p6q7r8-9s0t-1u2v-3w4x, version_id: v1)
│   │   ├── _navigation.html (artifact_id: nav_g6q7r8s9-0t1u-2v3w-4x5y, version_id: v1)
│   │   ├── _hero.html (artifact_id: hero_h7r8s9t0-1u2v-3w4x-5y6z, version_id: v1)
│   └── base.html (artifact_id: base_i8s9t0u1-2v3w-4x5y-6z7a, version_id: v1)
├── tests/ (artifact_id: tests_o4y5z6a7-8b9c-0d1e-2f3g, version_id: v1)
├── staticfiles/ (generated via `python manage.py collectstatic`)
├── venv/ (generated via `python -m venv env`)
├── .env (artifact_id: env_p5z6a7b8-9c0d-1e2f-3g4h, version_id: v1)
├── .gitignore (artifact_id: gitignore_q6a7b8c9-0d1e-2f3g-4h5i, version_id: v1)
├── db.sqlite3 (artifact_id: db_r7b8c9d0-1e2f-3g4h-5i6j, version_id: v1)
├── manage.py (artifact_id: manage_s8c9d0e1-2f3g-4h5i-6j7k, version_id: v1)
├── requirements.txt (artifact_id: req_t9d0e1f2-3g4h-5i6j-7k8l, version_id: v1)

+-------------------+       +-------------------+       +-------------------+
|    Browser        |       |    Django App     |       |    Stripe API     |
|                   |       |                   |       |                   |
|  +-------------+  |       |  +-------------+  |       |  +-------------+  |
|  | Templates   |  |       |  | Views       |  |       |  | Payment     |  |
|  | - home.html |  |       |  | - choose    |  |       |  | Processing  |  |
|  | - choose... |  |<----->|  | - bookings  |  |<----->|  | Webhooks    |  |
|  | - bookings  |  | HTTP  |  | - payment   |  | HTTP  |  +-------------+  |
|  | - payment   |  |       |  | - thank_you |  |       |                   |
|  | - thank_you |  |       |  +-------------+  |       |                   |
|  +-------------+  |       |                   |       |                   |
|                   |       |  +-------------+  |       |                   |
|  +-------------+  |       |  | Models      |  |       |                   |
|  | Static      |  |       |  | - FAQ       |  |       |                   |
|  | - custom.css|  |       |  | - Pricing   |  |       |                   |
|  | - main.js   |  |       |  | - Booking   |  |       |                   |
|  | - payment.js|  |       |  +-------------+  |       |                   |
|  +-------------+  |       |                   |       |                   |
+-------------------+       +-------------------+       +-------------------+