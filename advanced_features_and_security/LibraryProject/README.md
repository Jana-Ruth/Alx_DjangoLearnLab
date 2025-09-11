# Permissions & Groups Setup

## Custom Permissions
Defined in `bookshelf/models.py`:
- `can_view` → Allows viewing books.
- `can_create` → Allows creating books.
- `can_edit` → Allows editing books.
- `can_delete` → Allows deleting books.

## Groups
Configured in Django Admin:
- **Viewers** → can_view
- **Editors** → can_view, can_create, can_edit
- **Admins** → can_view, can_create, can_edit, can_delete

## Enforcing in Views
Permissions are enforced with `@permission_required` decorators in `bookshelf/views.py`.

## Testing
- Create test users
- Assign them to groups
- Verify that users can only access actions allowed by their group permissions.



# Security Notes

## Important settings (production)
- DEBUG = False
- ALLOWED_HOSTS must include your domain(s)
- CSRF_COOKIE_SECURE = True
- SESSION_COOKIE_SECURE = True
- SECURE_SSL_REDIRECT = True
- SECURE_HSTS_SECONDS = 31536000 (use only on production after testing)

## CSRF Protection
- All POST forms include `{% csrf_token %}` in templates.

## Prevent SQL Injection
- Use Django ORM (filter, exclude, get) and ModelForms.
- If using raw SQL, use parameterized queries (cursor.execute(sql, [params])).

## Content Security Policy (CSP)
- Use django-csp or set header. Adjust CSP_* settings in `settings.py`.

## Permissions & Groups
- Custom permissions defined in `bookshelf.models.Book.Meta.permissions`.
- Use `@permission_required('bookshelf.can_edit', raise_exception=True)` in views.

## Testing
- Create test users in admin and assign them to groups (Viewers/Editors/Admins).
- Verify actions permitted/forbidden for each group.
