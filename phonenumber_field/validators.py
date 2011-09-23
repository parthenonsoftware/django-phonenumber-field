#-*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from phonenumbers import parse
from phonenumbers.phonenumberutil import NumberParseException
from phonenumber_field.phonenumber import PhoneNumber

def validate_international_phonenumber(value):
    phone_number = PhoneNumber.from_field_value(value)
    if phone_number and not phone_number.is_valid():
        raise ValidationError(_(u'Enter a valid phone number ("e.g +411234567").'))

