from flask_principal import Permission, RoleNeed

# Define role needs
admin_role = RoleNeed('admin')
guest_role = RoleNeed('guest')

# Define permissions
admin_permission = Permission(admin_role)
guest_permission = Permission(guest_role)
