from django.forms import ModelForm
from .models import EmailList

class EmailListForm(ModelForm):
    class Meta:
        model = EmailList
        fields = ["email"]
