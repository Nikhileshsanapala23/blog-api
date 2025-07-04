# Blog API with Authentication

A Django-based blogging API with user authentication, post creation, and commenting functionality.

## Features

- User registration and login
- Create, view blog posts
- Add comments to posts
- Session-based authentication
- RESTful API endpoints (without DRF)

## Setup Instructions

### Prerequisites

- Python 3.8+
- pip
- Virtualenv (recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/blogapi.git
   cd blogapi
Create and activate virtual environment

bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
Install dependencies

bash
pip install -r requirements.txt
Database setup

bash
python manage.py migrate
Create superuser (optional)

bash
python manage.py createsuperuser
Run the development server

bash
python manage.py runserver
The API will be available at http://localhost:8000/api/