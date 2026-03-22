# Smart Living Hub

## Overview

Smart Living Hub is a Flask-based web application designed to help users manage key aspects of everyday life in one place. It combines job searching, housing exploration, financial advice, and accessibility features into a simple and interactive platform.

This project was built during a hackathon as a full-stack application using Python, HTML, and Bootstrap.

---

## Features

### User Authentication

* Register and log in securely
* Password hashing using Werkzeug
* Session-based login system
* Logout functionality

---

### Job Search (Part-Time & Full-Time)

* Search jobs using API integration
* Filter by:

  * Job title
  * Location
  * Contract type
* Displays job details such as salary and location

---

### Rental Listings

* Fetch and display housing/property data
* Designed for filtering based on user input
* Integrates with external APIs

---

### Finance Section

* Dedicated page for financial advice
* Placeholder for budgeting and savings tools

---

### Subscriptions Page

* UI for managing subscriptions/services
* Can be expanded with backend functionality

---

### Accessibility Settings

* Custom user preferences:

  * Text size
  * Icon size
  * Dark mode
  * Colour filters
  * Language
* Stored in database and applied across pages

---

## Tech Stack

**Backend:**

* Flask (Python)
* MySQL
* dotenv (environment variables)

**Frontend:**

* HTML
* Bootstrap
* Jinja2 templating

**Security:**

* Werkzeug password hashing
* Flask sessions

---

## Project Structure

```
project/
│── app.py
│── templates/
│── static/
│── .env
│── test_app.py
```

---

## Environment Variables

Create a `.env` file in your project root:

```
SECRET_KEY=your_secret_key
DB_HOST=your_host
DB_USER=your_user
DB_PASS=your_password
DB_NAME=your_database

ADZUNA_APP_ID=your_app_id
ADZUNA_APP_KEY=your_app_key

LETTINGKEY=your_api_key
```

---

## How to Run

1. Install dependencies

```
pip install flask mysql-connector-python python-dotenv
```

2. Run the app

```
python app.py
```

3. Open in browser

```
http://127.0.0.1:8080
```

---

## Testing

Run unit tests:

```
python test_app.py
```

---

## What We Learned

* How to build full-stack apps with Flask
* API integration and data handling
* Authentication and session management
* Debugging and testing web applications

---

## Notes

* Some features (job filtering, rent API) are still being improved
* API keys are required for full functionality

---

## Future Improvements

* Better UI/UX design
* Advanced filters for jobs and rentals
* Save favourites
* Deploy online

---

## Team

Built during a hackathon as a collaborative project.

---

## License

For educational and hackathon use only.
