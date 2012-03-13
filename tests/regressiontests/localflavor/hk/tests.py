from django.contrib.localflavor.hk.forms import HKPhoneNumberField
from django.contrib.localflavor.hk.forms import hk_special_numbers, \
                                                hk_phone_prefixes
from django.test import SimpleTestCase


class HKLocalFlavorTests(SimpleTestCase):
    def test_HKPhoneNumberField(self):
        error_format = (
            u'Phone numbers should not start with ' \
             'one of the followings: %s.' % \
             ', '.join(hk_special_numbers),
            u'Phone numbers must be in XXXX-XXXX format.',
            u'Phone numbers should start with ' \
             'one of the followings: %s.' % \
             ', '.join(hk_phone_prefixes),
        )
        valid = {
            '3102-3883': '3102-3883',
            '3102 3883': '3102-3883',
            '31023883': '3102-3883',
            '(852) 3102-3883': '3102-3883',
            '(+852) 3102-3883': '3102-3883',
            '852-3102-3883': '3102-3883',
            '85231023883': '3102-3883',
        }
        invalid = {
            '1083': error_format,
            '18503': error_format,
            '999': error_format,
            '992': error_format,
            '112': error_format,
            '99987654': error_format,
            '99287654': error_format,
            '11287654': error_format,
            '00000000': error_format,
            '44444444': error_format,
            '77777777': error_format,
            '3102--3883': error_format,
        }
        self.assertFieldOutput(HKPhoneNumberField, valid, invalid)
