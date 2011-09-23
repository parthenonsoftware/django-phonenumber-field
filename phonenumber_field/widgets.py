#-*- coding: utf-8 -*-
import re
import phonenumbers

from django.forms.widgets import MultiWidget, Select, TextInput

from country_codes import COUNTRY_CODES
from phonenumber import PhoneNumber

class InternationalPhoneNumberWidget(MultiWidget):
    phone_clean = re.compile("[^0-9]");

    def __init__(self, attrs = None):
        widgets = (
                    Select(choices = self.get_choices()),
                    TextInput(),
                )
        super(InternationalPhoneNumberWidget, self).__init__(widgets, attrs)

    @classmethod
    def get_choices(cls):
        """
        Transforms country code information from its current format like:
            ('Afghanistan', '93', )
        to something more visibly descriptive:
            ('Afghanistan (+93)', '93', )
        """
        choices = map(
                    lambda n: (
                            cls.phone_clean.sub('', n[1]), 
                            n[0] + " (+" + n[1] + ")",
                        ),
                    COUNTRY_CODES,
                )
        choices.insert(0, (None, None, ))
        return choices
    
    def decompress(self, value):
        if isinstance(value, PhoneNumber):
            return (str(value.country_code), str(value.national_number), )
        elif value:
            parsed = phonenumbers.parse(value, None)
            return (str(parsed.country_code), str(parsed.national_number), )
        return ''
