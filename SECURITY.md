# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| main    | :white_check_mark: |

This is a personal portfolio project. The `main` branch receives security updates.

## Reporting a Vulnerability

**Please DO NOT open a public issue to report a vulnerability.**

If you believe you have found a security flaw, please email **br4yangil006@gmail.com** with the following details:
1. Description of the issue.
2. Exact steps to reproduce it (payloads, URLs, etc.).
3. Potential impact (e.g., XSS, auth bypass, DoS).

**Response Commitment:**
- Acknowledgment of receipt within 72 hours.
- Initial severity assessment within 7 days.
- Fix or mitigation based on severity (CRITICAL/HIGH highest priority).

## Scope

Applies to all code contained in this repository:
- Python backend (`/security`, `/data`, `/handlers`).
- JavaScript frontend (`/frontend/js`).
- Database schemas (`/data/migrations`).

**Out of scope:**
- Vulnerabilities in third-party services (Google Analytics, Google/Microsoft OAuth).
- Social engineering attacks (phishing).
- Automated scanner reports without a working Proof of Concept (PoC).

## Implemented Security Measures

- **Content Security Policy (CSP):** Blocks inline scripts and styles (`unsafe-inline`).
- **CSRF:** Double-submit cookie pattern signed with HMAC-SHA256.
- **Passwords:** `scrypt` hashing with constant-time comparison (`hmac.compare_digest`).
- **SQL Injection:** Strict use of parameterized queries (never concatenated).
- **XSS:** HTML entity escaping on the backend and `textContent` in the frontend DOM.
- **Sessions:** `HttpOnly`, `SameSite=Strict`, and `Secure` (in production) cookies.
- **Rate Limiting:** Sliding window to prevent brute-force and API abuse.

Thank you for helping keep this project secure.
