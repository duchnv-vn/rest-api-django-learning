"""
Django admin customization
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from core.models import (
    User,
    Recipe,
    Tag,
    Ingredient,
)


class UserAdmin(BaseUserAdmin):
    """ Define the admin pages for users """
    # Set fields displayed in table of list page
    ordering = ['id']
    list_display = ['email', 'name']

    # Set fields displayed in edit page
    fieldsets = (
        (
            None,
            {
                'fields': (
                    'email',
                    'password'
                )
            }
        ),
        (
            _('Detail information'),
            {
                'fields': (
                    'name',
                )
            }
        ),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser'
                )
            }
        ),
        (
            _('Important dates'),
            {
                'fields':
                (
                    'last_login',
                )
            }
        ),
    )

    readonly_fields = ['last_login']

    # Set fields displayed in create page
    add_fieldsets = (
        (
            None,
            {
                'classes': (
                    'wide',
                ),
                'fields': (
                    'email',
                    'password1',
                    'password2',
                    'name',
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
    )


admin.site.register(User, UserAdmin)
admin.site.register(Recipe)
admin.site.register(Tag)
admin.site.register(Ingredient)
