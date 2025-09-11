INSTALLED_APPS = [
    # default apps...
    "accounts",  # 👈 add this line
]

AUTH_USER_MODEL = "bookshelf.CustomUser"


# SECURITY SETTINGS (production-ready defaults — adjust hosts & origins)
DEBUG = False

ALLOWED_HOSTS = [
    "yourdomain.com",  # <- replace with your production domain
    "localhost",       # keep while testing locally
    "127.0.0.1",
]

# Prevent clickjacking
X_FRAME_OPTIONS = "DENY"

# Browser-based XSS filter
SECURE_BROWSER_XSS_FILTER = True

# Content Type sniffing protection
SECURE_CONTENT_TYPE_NOSNIFF = True

# Cookies: only sent over HTTPS
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

# Redirect all HTTP to HTTPS (enable in production when you have HTTPS)
SECURE_SSL_REDIRECT = True

# HSTS (ensure you understand HSTS before enabling on production domains)
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Trusted origins for CSRF (for example if using https://yourdomain.com)
CSRF_TRUSTED_ORIGINS = [
    "https://yourdomain.com",
    # "https://subdomain.yourdomain.com",
]

# --- Content Security Policy (Option: using django-csp) ---
# 1) pip install django-csp
# 2) add 'csp' to INSTALLED_APPS
# 3) add 'csp.middleware.CSPMiddleware' to MIDDLEWARE (see below)
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'",)       # adjust if using CDNs
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'")  # 'unsafe-inline' only if necessary
CSP_IMG_SRC = ("'self'", "data:")
CSP_FONT_SRC = ("'self'", "data:")
CSP_CONNECT_SRC = ("'self'",)

# --- Middleware: make sure CSPMiddleware is present (if using django-csp) ---
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # ... other middleware ...
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    # CSP (if using django-csp)
    "csp.middleware.CSPMiddleware",
    # ... other middleware (keep ordering sensible) ...
]


# ---- HTTPS / Security settings (production) ----
# NOTE: These are production settings. For local HTTP testing, you may temporarily set DEBUG=True and
# set CSRF_COOKIE_SECURE = SESSION_COOKIE_SECURE = False. Always ensure these are True in production.

DEBUG = False  # MUST be False in production.

# List your production domains here (no protocol)
ALLOWED_HOSTS = ["yourdomain.com", "www.yourdomain.com"]

# --- Force HTTPS ---
# Redirect all HTTP requests to HTTPS
SECURE_SSL_REDIRECT = True

# If Django is behind a trusted proxy (e.g., nginx, Heroku), set this so Django knows the original protocol.
# Example: ('HTTP_X_FORWARDED_PROTO', 'https') if nginx sets X-Forwarded-Proto.
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# --- HSTS (HTTP Strict Transport Security) ---
# Instruct browsers to use HTTPS for future requests. Enable after verifying HTTPS is properly configured.
SECURE_HSTS_SECONDS = 31536000  # 1 year, change to smaller during initial rollout (e.g., 3600)
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# --- Secure cookies ---
# Ensure cookies are only sent over HTTPS
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# HTTPOnly cookies help mitigate XSS stealing cookies (Django sets this by default for session cookie)
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = False  # typically False so client-side JS frameworks can read CSRF token if needed

# --- Browser security headers ---
# Protect against MIME type sniffing (prevents some XSS attack vectors)
SECURE_CONTENT_TYPE_NOSNIFF = True

# Enable the browser's XSS filter
SECURE_BROWSER_XSS_FILTER = True

# Prevent the site being framed to mitigate clickjacking
X_FRAME_OPTIONS = "DENY"

# --- Content Security Policy (optional, recommended) ---
# Optionally configure CSP via django-csp or middleware (see docs). Example defaults:
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'",)
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'")  # avoid 'unsafe-inline' if possible
CSP_IMG_SRC = ("'self'", "data:")
CSP_FONT_SRC = ("'self'", "data:")
CSP_CONNECT_SRC = ("'self'",)

# --- Other security-related settings ---
# Prevent referrer leakage (optional)
SECURE_REFERRER_POLICY = "no-referrer-when-downgrade"

# Trust the X-Forwarded-Proto header set by the proxy
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Security settings for HTTPS
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Secure Headers
X_FRAME_OPTIONS = "DENY"
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True

# Trust proxy header for HTTPS
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

