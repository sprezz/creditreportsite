from django.test import TestCase

from website.templatetags.static_file_prefix import fileurl_prefix


class TestTemplateTag(TestCase):
    def test_ok(self):
        self.assertEqual(fileurl_prefix('US', 'lp2'), '/lps/us/lp2')

