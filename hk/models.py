from django.db import models


class PhoneNumberField(models.CharField):
    description = 'Phone number'

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 9  # e.g. XXXX-XXXX
        super(PhoneNumberField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        from common.forms import HKPhoneNumberField
        defaults = {'form_class': HKPhoneNumberField}
        defaults.update(kwargs)
        return super(PhoneNumberField, self).formfield(**defaults)
