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
