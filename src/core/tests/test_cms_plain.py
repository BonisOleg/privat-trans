from django.test import SimpleTestCase
from django.utils.safestring import SafeString

from src.core.site_blocks import html_to_plain, normalize_cms_plain, plain_with_breaks


class HtmlToPlainTests(SimpleTestCase):
    def test_tinymce_paragraphs_become_newlines(self):
        self.assertEqual(html_to_plain("<p>рядок 1</p><p>рядок 2</p>"), "рядок 1\nрядок 2")

    def test_tinymce_paragraphs_with_source_newline_stay_single_break(self):
        self.assertEqual(html_to_plain("<p>рядок 1</p>\n<p>рядок 2</p>"), "рядок 1\nрядок 2")

    def test_double_enter_empty_paragraph_is_blank_line(self):
        self.assertEqual(html_to_plain("<p>a</p><p>&nbsp;</p><p>b</p>"), "a\n\nb")

    def test_br_becomes_newline(self):
        self.assertEqual(html_to_plain("a<br>b<br />c"), "a\nb\nc")

    def test_textarea_newlines_kept(self):
        self.assertEqual(html_to_plain("a\nb"), "a\nb")

    def test_tags_stripped_without_xss(self):
        self.assertEqual(html_to_plain('<p>ok<script>x</script></p>'), "okx")

    def test_plain_with_breaks_escapes_and_br(self):
        html_out = plain_with_breaks("<p>A & B</p>\n<p>C</p>")
        self.assertIsInstance(html_out, SafeString)
        self.assertEqual(html_out, "A &amp; B<br>C")

    def test_normalize_cms_plain_keeps_breaks(self):
        self.assertEqual(normalize_cms_plain("<p>one</p><p>two</p>"), "one\ntwo")
