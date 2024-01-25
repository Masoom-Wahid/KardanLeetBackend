from django.contrib import admin
from Contest.models import Contest_Question
from .models import (
    SampleTestCasesExample,
    SampleTestCases,
    Constraints
)
admin.site.register(SampleTestCasesExample)
admin.site.register(Constraints)
admin.site.register(Contest_Question)
admin.site.register(SampleTestCases)
