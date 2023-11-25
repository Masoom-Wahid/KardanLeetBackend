from django.contrib import admin
from .models import (
    Contests,
    Contest_Groups,
    Contestants,
    Contest_submissiosn,
    Contest_solutions
)

admin.site.register(Contests)
admin.site.register(Contest_Groups)
admin.site.register(Contestants)
admin.site.register(Contest_submissiosn)
admin.site.register(Contest_solutions)