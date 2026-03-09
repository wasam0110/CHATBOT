# API_CHATNOT

This repository contains a Django-based chatbot API and web interface. It is designed for easy deployment and customization, with a clean, production-ready codebase.

## Features

- Django 4.2 backend
- MySQL database support (via PyMySQL)
- Environment variable management with dotenv
- User authentication (login, registration, password reset)
- Modern chat UI with Markdown, code highlighting, and KaTeX math rendering
- Responsive, professional theme (custom CSS)

## Setup

1. **Clone the repository:**
   ```sh
   git clone <your-repo-url>
   cd API_CHATNOT
   ```
2. **Create a virtual environment:**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
4. **Configure environment variables:**
   - Copy `.env.example` to `.env` and update values as needed.
5. **Apply migrations:**
   ```sh
   python manage.py migrate
   ```
6. **Run the server:**
   ```sh
   python manage.py runserver
   ```

## Deployment

- Configure your production database and environment variables.
- Use a WSGI server (e.g., Gunicorn, uWSGI) and a web server (e.g., Nginx) for deployment.
- Collect static files with `python manage.py collectstatic`.

## File Structure

- `MyChatbot/` — Django project and app code
- `templates/` — HTML templates (chat, auth, etc.)
- `static/` — CSS, JS, and assets
- `.env.example` — Example environment config
- `requirements.txt` — Python dependencies

## Notes

- Do **not** commit your virtual environment or database files.
- For customization, edit the CSS in `static/css/` and templates in `templates/`.

## License

This project is licensed under the MIT License.
