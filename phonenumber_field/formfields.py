#-*- coding: utf-8 -*-
import re

from django.utils.translation import ugettext_lazy as _
from django.forms.fields import CharField, MultiValueField, ChoiceField
from django.core.exceptions import ValidationError
from phonenumber_field.validators import validate_international_phonenumber
from phonenumber_field.phonenumber import PhoneNumber

from widgets import InternationalPhoneNumberWidget

class PhoneNumberField(CharField):
    default_error_messages = {
        'invalid': _(u'Enter a valid phone number ("e.g +411234567").'),
    }
    default_validators = [validate_international_phonenumber]

    def to_python(self, value):
        phone_number = PhoneNumber.from_field_value(value)
        if phone_number and not phone_number.is_valid():
            raise ValidationError(self.error_messages['invalid'])
        return phone_number

class InternationalPhoneNumberField(MultiValueField):
    widget = InternationalPhoneNumberWidget

    phone_clean = re.compile("[^0-9]");

    def __init__(self, *args, **kwargs):
        fields = (
                    ChoiceField(
                            choices = self.widget.get_choices()
                        ),
                    CharField(),
                )
        # it doesn't make sense that I have to do this :-\
        # I'll investigate later
        if "max_length" in kwargs.keys():
            del(kwargs['max_length'])
        super(InternationalPhoneNumberField, self).__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        if not data_list or len(data_list) < 2 or not data_list[0] or not data_list[1]:
            return None
        return '+%s %s' % (self.phone_clean.sub('', data_list[0]), self.phone_clean.sub('', data_list[1]))

    def to_python(self, value):
        phone_number = PhoneNumber.from_field_value(value)
        if phone_number and not phone_number.is_valid():
            raise ValidationError()
        return phone_number
