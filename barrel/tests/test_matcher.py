from unittest import TestCase

from barrel.extractor import HtmlMatcher, HtmlExtractor


class TestHtmlMatcher(TestCase):
    def test_extraction(self):
        """Test if matcher works properly"""
        # just xpath match
        extractor = HtmlMatcher(regex=r"ana", xpath='//span/text()',
                                collect=False)
        input_text = '<span>maria</span>'
        expected = False
        self.assertEqual(extractor.parse(input_text), expected)

        # just regex match
        extractor = HtmlMatcher(regex=r"ana", xpath='//span/text()',
                                collect=False)
        input_text = '<div>ana</div>'
        expected = False
        self.assertEqual(extractor.parse(input_text), expected)

        # both match
        extractor = HtmlMatcher(regex=r"ana", xpath='//div/text()',
                                collect=False)
        input_text = '<div>ana</div>'
        expected = True
        self.assertEqual(extractor.parse(input_text), expected)

        # css match
        extractor = HtmlMatcher(regex=r"ana", css='.class2',
                                collect=False)
        input_text = '<div class="class1">maria</div>'
        expected = False
        self.assertEqual(extractor.parse(input_text), expected)

        # regex match
        extractor = HtmlMatcher(regex=r"ana", css='.class2',
                                collect=False)
        input_text = '<div class="class1">ana</div>'
        expected = False
        self.assertEqual(extractor.parse(input_text), expected)

        # both match
        extractor = HtmlMatcher(regex=r"ana", css='.class1',
                                collect=False)
        input_text = '<div class="class1">ana</div>'
        expected = True
        self.assertEqual(extractor.parse(input_text), expected)

        # regex match
        extractor = HtmlMatcher(regex=r"ana", collect=False)
        input_text = '<div class="class1">ana</div>'
        expected = True
        self.assertEqual(extractor.parse(input_text), expected)


        # regex match
        extractor = HtmlMatcher(regex=r"(a|b)na", collect=False)
        input_text = '<div class="class1">ana</div>'
        expected = True
        self.assertEqual(extractor.parse(input_text), expected)

        # no match
        extractor = HtmlMatcher(regex=r"asadsadna", collect=False)
        input_text = '<div class="class1">ana</div>'
        expected = False
        self.assertEqual(extractor.parse(input_text), expected)

    def test_matching(self):
        """Test if collection works properly"""
        # just xpath match
        extractor = HtmlMatcher(regex=r"ana", xpath='//span/text()',
                                collect=True)
        input_text = '<span>maria</span>'
        expected = []
        self.assertListEqual(extractor.parse(input_text), expected)

        # just regex match
        extractor = HtmlMatcher(regex=r"ana", xpath='//span/text()',
                                collect=True)
        input_text = '<div>ana</div>'
        expected = []
        self.assertListEqual(extractor.parse(input_text), expected)

        # both match
        extractor = HtmlMatcher(regex=r"ana.", xpath='//div/text()',
                                collect=True)
        input_text = '<div>anaa maria anax ana</div>'
        expected = ['anaa', 'anax']
        self.assertListEqual(extractor.parse(input_text), expected)

        # css match
        extractor = HtmlMatcher(regex=r"ana", css='.class2',
                                collect=True)
        input_text = '<div class="class1">maria</div>'
        expected = []
        self.assertListEqual(extractor.parse(input_text), expected)

        # regex match
        extractor = HtmlMatcher(regex=r"ana", css='.class2',
                                collect=True)
        input_text = '<div class="class1">ana</div>'
        expected = []
        self.assertListEqual(extractor.parse(input_text), expected)

        # both match
        extractor = HtmlMatcher(regex=r"ana.", css='.class1',
                                collect=True)
        input_text = '<div class="class1">anax</div> anz'
        expected = ['anax']
        self.assertListEqual(extractor.parse(input_text), expected)

        # regex match
        extractor = HtmlMatcher(regex=r"ana...", collect=True)
        input_text = '<div class="class1">anatar</div> anapur'
        expected = ['anatar', 'anapur']
        self.assertListEqual(extractor.parse(input_text), expected)

        # no match
        extractor = HtmlMatcher(regex=r"asadsadna", collect=True)
        input_text = '<div class="class1">ana</div>'
        expected = []
        self.assertListEqual(extractor.parse(input_text), expected)

        # xpath match
        extractor = HtmlMatcher(xpath="//div/text()", collect=True)
        input_text = '<p><div class="class1">ana</div> <div>aaa</div></p>'
        expected = ['ana', 'aaa']
        self.assertListEqual(extractor.parse(input_text), expected)
        self.assertListEqual(extractor.parse(input_text), expected)

        # css match
        extractor = HtmlMatcher(css="div::text", collect=True)
        input_text = '<p><div class="class1">ana</div> <div>aaa</div></p>'
        expected = ['ana', 'aaa']
        self.assertListEqual(extractor.parse(input_text), expected)


class TestHtmlExractor(TestCase):
    def test_extraction(self):
        extractor = HtmlExtractor(collect={"ana": r"(A|B)na",
                                           "divs": {"xpath": '//div/text()'},
                                           "cls": {"css": ".cls::text"}},
                                  keywords={"e": r"exists",
                                            "css": {"css": ".cls"},
                                            "xpath": {"xpath": "//p"},
                                            "xpath2": {"xpath": "//a"}})
        input_text = '<p><div class="class1">Anax</div> Bna ' \
                     '<span class="cls">continut</span>' \
                     'exists</p>'
        results = extractor.extract(input_text)

        self.assertListEqual(results['ana'], ['Ana', 'Bna'])
        self.assertListEqual(results['divs'], ['Anax'])
        self.assertListEqual(results['cls'], ['continut'])

        self.assertEqual(results['e'], True)
        self.assertEqual(results['css'], True)
        self.assertEqual(results['xpath'], True)
        self.assertEqual(results['xpath2'], False)






