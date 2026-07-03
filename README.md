# Toriloshop

Toriloshop is a simple Django practice project for a small shop site. It demonstrates basic app setup, URL routing, and simple HTTP responses for a home page, product list page, and about page.

## Features Implemented

- `home()` at `/`
- `product_list()` at `/products/`
- `about()` at `/about/`
- `products` and `users` registered in `INSTALLED_APPS`

## Setup Instructions

1. Create and activate a virtual environment.
2. Install Django.
3. Run migrations if needed.
4. Start the server with `python manage.py runserver`.
5. Open the pages in a browser:
   - `http://127.0.0.1:8000/`
   - `http://127.0.0.1:8000/products/`
   - `http://127.0.0.1:8000/about/`

## Screenshots

![Home page](screenshots/01_home_page.png)

![Products page](screenshots/02_products_page.png)

![About page](screenshots/03_about_page.png)

![Project structure](screenshots/04_project_structure.png)

## Notes

The `users` app is included as required by the assignment and is ready for future user-related views or models.