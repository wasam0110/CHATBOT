This project is a Django-based chatbot platform that provides both a RESTful API and a modern web interface for interactive conversations. It is designed for easy deployment, secure configuration, and professional use in production environments.

Key Features:

Django 4.2 Backend: Robust, scalable, and secure Python web framework.
Chatbot API: RESTful endpoints for sending and receiving chat messages, enabling integration with other apps or frontend clients.
User Authentication: Supports user registration, login, logout, and password reset, ensuring secure access.
MySQL Database Support: Uses PyMySQL for reliable data storage and retrieval.
Environment Configuration: Uses dotenv for managing secrets and environment variables, keeping sensitive data out of source control.
Modern Web UI: Responsive chat interface with Markdown support, code syntax highlighting, and KaTeX for math rendering.
Customizable Theme: Professional, clean CSS for a polished user experience.
Production-Ready: Structured for deployment with WSGI servers (Gunicorn, uWSGI) and web servers (Nginx), and includes static file management.
Intended Use Cases:

Deploy as a standalone chatbot web app for customer support, education, or entertainment.
Integrate the API with other applications, bots, or messaging platforms.
Use as a template for building more advanced conversational AI or assistant systems.
Security & Best Practices:

No sensitive files (like .env or venv) are tracked in the repository.
All secrets and API keys are managed via environment variables.
The codebase is suitable for public, open-source sharing.
Setup & Deployment:

Clone the repo, create a virtual environment, install dependencies, and configure your environment variables.
Run Django migrations and start the development server.
For production, configure your database, collect static files, and deploy with a WSGI server behind a web server.
Customization:

Edit CSS in the static directory and HTML templates for branding or UI changes.
Extend the chatbot logic or API endpoints to add new features or integrations.
License:
MIT License — free for personal and commercial use.
