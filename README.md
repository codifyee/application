# Task Management System

A comprehensive task management web application with a WordPress frontend and Django backend. Users can view tasks, pick tasks, update task status, and track progress. The system provides an interactive dashboard for team productivity tracking.

## Features

- User authentication (login/signup)
- Interactive dashboard showing task statistics
- Task listing and filtering
- Task assignment functionality
- Task status updates (To Do, In Progress, Done, Blocked)
- Task history tracking
- Comments on tasks
- Admin panel for task management
- Responsive design for all devices
- WordPress integration for content pages (Home, About, Services, etc.)

## Architecture

The application uses a hybrid architecture:

- **Frontend**: WordPress for the main website pages (Home, About, Contact, etc.)
- **Backend**: Django for the task management functionality
- API integration between WordPress and Django for seamless user experience

## Setup Instructions

### Prerequisites

- Python 3.8+
- Django 5.0+
- MySQL/PostgreSQL database (optional, can use SQLite for development)

### Django Backend Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/task-management-system.git
   cd task-management-system
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the dependencies:
   ```
   pip install django
   ```

4. Apply migrations:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

6. Run the Django development server:
   ```
   python manage.py runserver
   ```

7. Access the Django admin at `http://127.0.0.1:8000/admin/`

### WordPress Setup

1. Install WordPress on your server

2. Copy the WordPress theme files from the `wordpress` directory to your WordPress themes directory:
   ```
   cp -r wordpress /path/to/your/wordpress/wp-content/themes/taskmanager
   ```

3. Activate the "Task Manager" theme in the WordPress admin panel

4. Configure the connection to Django backend in WordPress:
   - Go to WordPress admin > Settings > Task Manager API
   - Set the API URL to your Django backend (e.g., `http://127.0.0.1:8000/api/`)

## Usage

### Admin Tasks

1. Log in to the Django admin panel at `http://127.0.0.1:8000/admin/`
2. Create and manage tasks, users, and other settings

### User Tasks

1. Visit the website homepage
2. Log in using your credentials
3. View your dashboard to see available tasks and statistics
4. Pick tasks that are unassigned
5. Update task status as you progress
6. Add comments to tasks for team collaboration

## Development

### Django Structure

- `tasks/models.py`: Database models
- `tasks/views.py`: View functions for the application
- `tasks/forms.py`: Form definitions
- `tasks/api.py`: API endpoints for WordPress integration
- `templates/`: HTML templates for the application

### WordPress Structure

- `wordpress/functions.php`: Main theme functions
- `wordpress/header.php` & `wordpress/footer.php`: Template parts
- `wordpress/front-page.php`: Homepage template
- `wordpress/assets/`: CSS, JS, and images
- `wordpress/includes/`: Additional PHP files for the theme

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin feature/my-new-feature`
5. Submit a pull request 
