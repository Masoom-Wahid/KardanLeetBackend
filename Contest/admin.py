from django.contrib import admin
from .models import (
    Contests,
    Contest_Groups,
    Contest_submissiosn,
)

admin.site.register(Contests)
admin.site.register(Contest_Groups)


@admin.register(Contest_submissiosn)
class Contest_submissiosnAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            ("Question Details"),
            {"fields":              
            ("id",
            "question",
            "lang",
            "solved",
            "status",
            "submit_time"
            ),
             }
        ),
        (
            ("Submission Code"),
            {"fields":("code",)}
        )
    )
    list_display = (
        "id",
        "question",
        "lang",
        "solved",
        "status",
        "submit_time",
    )
    ordering = ("-submit_time",)
    readonly_fields = ("submit_time","id",)
    search_fields = ("id","lang")