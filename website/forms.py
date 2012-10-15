from django import forms

from website.models import IPBan
from website.helpers import iptoint, inttoip


class IPBanAdminForm(forms.ModelForm):

    ip = forms.CharField(required=True, max_length=20)

    class Meta:
        model = IPBan

    def __init__(self, *args, **kwargs):
        super(IPBanAdminForm, self).__init__(*args, **kwargs)
        if self.initial.get('ip'):
            self.initial['ip'] = inttoip(self.initial['ip'])

    def clean_ip(self):
        ip = self.cleaned_data.get('ip')
        return iptoint(ip)
