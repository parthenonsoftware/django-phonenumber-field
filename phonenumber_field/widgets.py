#-*- coding: utf-8 -*-
import re
import phonenumbers

from django.forms.widgets import MultiWidget, Select, TextInput, MultipleHiddenInput
from django.forms.util import flatatt
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe

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


class HiddenInternationalPhoneNumberWidget(MultipleHiddenInput):
    def render(self, name, value, attrs=None, choices=()):
        if value is None: value = []
        final_attrs = self.build_attrs(attrs, type=self.input_type)
        id_ = final_attrs.get('id', None)
        inputs = []
        for i, v in enumerate(value):
            input_attrs = dict(value=force_unicode(v), **final_attrs)
            if id_:
                # An ID attribute was given. Add a numeric index as a suffix
                # so that the inputs don't all have the same ID attribute.
                input_attrs['id'] = '%s_%s' % (id_, i)
            # and we need to add this field!
            input_attrs['name'] = '%s_%s' % (name, i)
            inputs.append(u'<input%s />' % flatatt(input_attrs))
        return mark_safe(u'\n'.join(inputs))
