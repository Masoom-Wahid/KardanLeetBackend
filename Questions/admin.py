from django.contrib import admin
from Contest.models import Contest_Question
from .models import (
    sample_test_cases,
    sample_test_cases_file,
    Constraints
)
admin.site.register(Constraints)
admin.site.register(Contest_Question)
admin.site.register(sample_test_cases)
admin.site.register(sample_test_cases_file)
