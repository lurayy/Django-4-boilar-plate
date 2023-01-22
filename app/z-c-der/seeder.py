from django.contrib.auth import get_user_model

print("Seeding User App . . . ")
User = get_user_model()

admin = User.objects.create_superuser('admin', '', 'pass')
admin.save()
