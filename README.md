# 🎫 Event Management API

This project is a **backend system for event management** built with **Django REST Framework (DRF)**. It provides user registration, authentication, event creation, ticketing, and booking functionalities.

---

## ✨ Key Features

### User Management

* **Registration:** StartRegistration endpoint
* **Verification:** VerificationProcess endpoint with resend functionality
* **Login:** LoginUser endpoint
* **Update Profile:** FullUpdateUser endpoint
* **Change Password:** UpdatePassword endpoint

### Event Management

* **Create Event:** CreateEventAPIView endpoint
* **Manage Event:** MangeEventAPIView endpoint for updating or deleting events
* **List/Search Events:** AllEventsAPIView endpoint

### Ticket Management

* **Create Ticket:** CreateTicket endpoint
* **Delete Ticket:** DeleteTicket endpoint

### Booking Management

* **Book Ticket:** BookingAPIView endpoint
* **View My Bookings:** MyBookings endpoint
* **Get Specific Booking:** GetMybooking endpoint
* **Cancel Booking:** DeleteMyBooking endpoint

---

## 🔹 API Endpoints

| Endpoint                 | Method     | Description                       |
| ------------------------ | ---------- | --------------------------------- |
| `/registration/`         | POST       | Register new user                 |
| `/verification/`         | POST       | Verify user registration          |
| `/update_user/`          | PUT        | Update user profile               |
| `/login/`                | POST       | User login                        |
| `/update_password/`      | PUT        | Update user password              |
| `/resend_code/`          | POST       | Resend verification code          |
| `/create_event/`         | POST       | Create a new event                |
| `/event_management/<id>` | PUT/DELETE | Manage specific event             |
| `/api/events/`           | GET        | List or search events             |
| `/create_ticket/<id>`    | POST       | Create a ticket for event         |
| `/delete_ticket/<id>`    | DELETE     | Delete a ticket                   |
| `/booking_ticket/<id>/`  | POST       | Book a ticket for an event        |
| `/my_bookings/`          | GET        | List all my bookings              |
| `/my_booking/<id>`       | GET        | Get details of a specific booking |
| `/delete_booking/<id>`   | DELETE     | Cancel my booking                 |

---

## 🛠 Tech Stack

* **Python 3.10+**
* **Django 4.x**
* **Django REST Framework (DRF)**
* **SQLite / PostgreSQL**
* **JWT Authentication / Token based auth**
* **Git / GitHub**

---

## 🔹 Project Structure

```
EventManagementAPI/
├── event/                 # Main app for user and event management
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   └── admin.py
├── config/                # Django project settings and configuration
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── requirements.txt
└── README.md
```

---

## 👤 User Flow

1. User registers via `/registration/` and verifies account.
2. User logs in via `/login/`.
3. Users can view all events via `/api/events/`.
4. Admins can create, update, or delete events and tickets.
5. Users can book tickets, view bookings, and cancel bookings via booking endpoints.
6. JWT token ensures secure authenticated requests.

---

## 🔑 Environment Variables (.env)

```
DEBUG=True
SECRET_KEY=your_secret_key
DATABASE_URL=postgres://user:password@localhost:5432/db_name
```

---

## 📄 License

Private project, intended for learning and personal portfolio.

---

## 👨‍💻 Author

Developed by **Muhammadumar Umarov**
Telegram: @Muhammadumar_umarov
Python Developer
