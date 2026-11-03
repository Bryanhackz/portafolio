# 🛡️ Secure Portfolio - Bryanhackz

![Python Tests](https://github.com/Bryanhackz/portafolio-bryanhackz/actions/workflows/test.yml/badge.svg)
![Python Version](https://img.shields.io/badge/python-3.11%2B-blue)
![Dependencies](https://img.shields.io/badge/dependencies-0-success)
![License](https://img.shields.io/badge/license-MIT-green)

A professional web development portfolio built with a **Security-First** approach. Designed from scratch using exclusively the **Python Standard Library**—no frameworks, no external dependencies, and no build steps.

🌐 **[View Live Site](https://your-render-or-pythonanywhere-url.com)** *(Update this link when deployed)*

## ✨ Key Features

- **Zero Dependencies:** The entire backend runs on pure Python (WSGI, SQLite, `hashlib`, `hmac`).
- **Enterprise-Grade Security:**
  - Strict Content Security Policy (CSP) with no `unsafe-inline`.
  - CSRF protection with HMAC-SHA256 signed tokens.
  - Password hashing with `scrypt` (N=2^15).
  - In-memory rate limiting with a sliding window.
  - Strict input/output sanitization.
- **Vanilla Frontend:** Semantic HTML5, modern CSS3 (CSS Grid, Flexbox), and ES6+ JavaScript (native modules).
- **Internationalization (i18n):** Native support for 8 languages based on the `Accept-Language` header.
- **Admin Panel:** Project and message management protected by role-based access control.

## 🚀 Technologies Used

- **Backend:** Python 3.11+ (WSGI, SQLite, `socketserver`, `urllib`).
- **Frontend:** HTML5, CSS3 (Custom Properties), Vanilla JavaScript.
- **Infrastructure:** Designed to run on standard WSGI servers (Render, PythonAnywhere, Gunicorn).
- **CI/CD:** GitHub Actions (14 unit tests).

## ⚙️ Local Installation & Execution

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Bryanhackz/portafolio-bryanhackz.git
   cd portafolio-bryanhackz
