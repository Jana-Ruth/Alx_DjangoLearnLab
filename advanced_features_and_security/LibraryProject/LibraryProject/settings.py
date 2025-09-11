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
