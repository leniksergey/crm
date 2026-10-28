from django.test import TestCase

from .models import Lead


class LeadStatusTests(TestCase):
    def test_new_lead_cannot_be_converted_to_customer(self):
        lead = Lead(status=Lead.Status.NEW)

        self.assertFalse(lead.can_convert_to_customer)

    def test_successful_lead_can_be_converted_to_customer(self):
        lead = Lead(status=Lead.Status.WON)

        self.assertTrue(lead.can_convert_to_customer)
