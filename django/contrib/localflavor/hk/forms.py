import re

from django.core.validators import EMPTY_VALUES
from django.forms import CharField
from django.forms import ValidationError
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext_lazy as _


hk_phone_digits_re = re.compile(r'^(?:852-?)?(\d{4})[-\.]?(\d{4})$')
hk_special_numbers = ('999', '992', '112')
hk_phone_prefixes = ('2', '3', '5', '6', '8', '9')


class HKPhoneNumberField(CharField):
    """
    Validate Hong Kong phone number.
    The input format can be either one of the followings:
    'XXXX-XXXX', '852-XXXX-XXXX', '(+852) XXXX-XXXX',
    'XXXX XXXX', or 'XXXXXXXX'.
    The output format is 'XXXX-XXXX'.

    Note: The phone number shall not start with 999, 992, or 112.
          And, it should start with either 2, 3, 5, 6, 8, or 9.

    Ref - http://en.wikipedia.org/wiki/Telephone_numbers_in_Hong_Kong
    """
    default_error_messages = {
        'disguise': _('Phone numbers should not start with ' \
                      'one of the followings: %s.') % \
                      ', '.join(hk_special_numbers),
        'invalid': _('Phone numbers must be in XXXX-XXXX format.'),
        'prefix': _('Phone numbers should start with ' \
                    'one of the followings: %s.') % \
                    ', '.join(hk_phone_prefixes),
    }

    def __init__(self, *args, **kwargs):
        super(HKPhoneNumberField, self).__init__(*args, **kwargs)

    def clean(self, value):
        super(HKPhoneNumberField, self).clean(value)

        if value in EMPTY_VALUES:
            return u''

        value = re.sub('(\(|\)|\s+|\+)', '', smart_unicode(value))
        m = hk_phone_digits_re.search(value)
        if not m:
            raise ValidationError(self.error_messages['invalid'])

        value = u'%s-%s' % (m.group(1), m.group(2))
        for special in hk_special_numbers:
            if value.startswith(special):
                raise ValidationError(self.error_messages['disguise'])

        prefix_found = map(lambda prefix: value.startswith(prefix),
                           hk_phone_prefixes)
        if not any(prefix_found):
            raise ValidationError(self.error_messages['prefix'])

        return value
