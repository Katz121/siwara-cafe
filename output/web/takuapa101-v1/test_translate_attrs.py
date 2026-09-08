import unittest

from build_en import translate_attrs


class TranslateAttrsTests(unittest.TestCase):
    def test_translates_thai_value_without_extra_quote(self):
        tag = '<input placeholder="พิมพ์ชื่อร้านที่ต้องการ">'
        mem = {'พิมพ์ชื่อร้านที่ต้องการ': 'Type the shop name you want'}
        self.assertEqual(
            translate_attrs(tag, mem),
            '<input placeholder="Type the shop name you want">',
        )

    def test_leaves_value_and_records_missing_translation(self):
        missing = {}
        tag = '<img alt="ชื่อร้านใหม่">'
        self.assertEqual(translate_attrs(tag, {}, missing), tag)
        self.assertEqual(missing, {'ชื่อร้านใหม่': 1})

    def test_leaves_non_thai_value_unchanged(self):
        tag = '<input title="Already English">'
        self.assertEqual(
            translate_attrs(tag, {'Already English': 'Should not change'}),
            tag,
        )


if __name__ == '__main__':
    unittest.main()
