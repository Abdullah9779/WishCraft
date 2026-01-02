# ✨WishCraft

<p align="center">
  <!-- Replace with your logo if you have one -->
  <a href="#">
    <img src="https://dotcoder.site/static/wishcraft/icon/wishcraft-logo.png" alt="WishCraft Logo" width="150"/>
  </a>
</p>

<p align="center">
  <strong>A Django-based platform for creating and sharing beautiful, personalized wish templates.</strong>
</p>

<p align="center">
    <a href="#"><img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54" alt="Python"></a>
    <a href="#"><img src="https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white" alt="Django"></a>
    <a href="#"><img src="https://img.shields.io/badge/mysql-%2300f.svg?style=for-the-badge&logo=mysql&logoColor=white" alt="MySQL"></a>
    <a href="#"><img src="https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white" alt="HTML5"></a>
    <a href="#"><img src="https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white" alt="CSS3"></a>
    <a href="#"><img src="https://img.shields.io/badge/tailwindcss-%2338B2AC.svg?style=for-the-badge&logo=tailwind-css&logoColor=white" alt="TailwindCSS"></a>
    <a href="#"><img src="https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E" alt="JavaScript"></a>
    <a href="#"><img src="https://img.shields.io/badge/pythonanywhere-%2300678B.svg?style=for-the-badge&logo=pythonanywhere&logoColor=white" alt="PythonAnywhere"></a>
</p>

Welcome to WishCraft, a web application designed for creating and sharing personalized templates. WishCraft provides a seamless user experience for generating beautiful and dynamic wish templates for any occasion.

🌐 **Website:** [https://wishcraft.pythonanywhere.com](https://wishcraft.pythonanywhere.com)

## ✨ Features

-   **✍️ Template Creation:** Easily create and customize wish templates with a user-friendly interface.
-   **🚀 API Support:** A built-in REST API (using Django REST Framework) to manage templates programmatically.
-   **🛡️ Enhanced Admin Security:** A custom middleware protects the admin panel, requiring session-based activation and IP whitelisting for enhanced security.
-   **📂 Dynamic Content:** Utilizes JSON data to manage templates, songs, and pictures, allowing for easy updates and scalability.
-   **📄 Static Pages:** Includes pre-built pages for About, Contact, and Privacy Policy.
-   **🔐 User Authentication:** (If applicable, add details about user registration/login)

## 🛠️ Tech Stack

-   **Backend:** Python, Django, Django REST Framework
-   **Frontend:** HTML, CSS, JavaScript
-   **Database:** MySQL
-   **Deployment:** PythonAnywhere
-   **Data:** JSON

## 🚀 Getting Started

Follow these instructions to get a local copy of WishCraft up and running for development and testing purposes.

### Prerequisites

-   Python 3.8+
-   Git

### Installation

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/Abdullah9779/WishCraft.git
    cd WishCraft
    ```

2.  **Create and activate a virtual environment:**
    -   On Windows:
        ```sh
        python -m venv WishCraft_venv
        .\WishCraft_venv\Scripts\activate
        ```
    -   On macOS/Linux:
        ```sh
        python3 -m venv WishCraft_venv
        source WishCraft_venv/bin/activate
        ```

3.  **Install the dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    Create a `.env` file in the root directory.
    ```env
    # --------------- Secret key ---------------
    SECRET_KEY = "your-secret-key"

    # --------------- Email Configurations ---------------
    EMAIL_HOST_USER = 'your-email-address@gmail.com'
    EMAIL_HOST_PASSWORD = 'your-email-password'
    DEFAULT_FROM_EMAIL = 'WishCraft <your-email-address@gmail.com>'
    MAIL_SEND_TO = 'your-second-email-address@gmail.com'

    # --------------- MySQL Configurations ---------------

    DATABASE_NAME = 'wishcraft-name'
    DATABASE_USER = 'wishcraft-user'
    DATABASE_PASSWORD = 'wishcraft-password'
    DATABASE_HOST = 'localhost'
    DATABASE_PORT = '3306'


    ```

5.  **Run the migrations:**
    ```sh
    python manage.py makemigrations
    python manage.py migrate
    ```

6.  **Create a superuser (optional):**
    To access the Django admin panel, create a superuser.
    ```sh
    python manage.py createsuperuser
    ```

7.  **Run the development server:**
    ```sh
    python manage.py runserver
    ```
    The application will be available at `http://127.0.0.1:8000/`.


## 📂 Project Structure

The project is organized into several Django apps, following a modular architecture:

```
WishCraft/
├── WishCraft/                      # Main Django project configuration
├── WishCraft_admin_panel_protection/ # Custom app for securing the admin panel
├── WishCraft_api/                  # App for the RESTful API
├── WishCraft_pages/                # App for handling static pages and views
├── static/                         # Static files (CSS, JS, images)
├── templates/                      # HTML templates
├── wishcraft-templates-data/       # JSON data for templates
├── .env                            # Environment variables (needs to be created)
├── manage.py                       # Django's command-line utility
└── requirements.txt                # Project dependencies
```

## 📄 License

Distributed under the Apache License 2.0.  
See the [LICENSE](https://github.com/Abdullah9779/WishCraft/blob/main/LICENSE) file for details.
