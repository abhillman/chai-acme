import lxml.etree

from .attributes import Attributes


class Parser:
    def __init__(self):
        pass

    @staticmethod
    def parse_results(html_str):
        parser = lxml.etree.HTMLParser()
        etree = lxml.etree.fromstring(html_str, parser=parser)

        # If querying breaks, consider referencing the documentation,
        # especially the part about generating xpath expressions; which
        # could form the basis of a means of fetching things with dynamic
        # selectors. https://lxml.de/xpathxslt.html#generating-xpath-expressions

        # List of artifacts (scholarly references like PDFs, books, etc.) on the current page
        artifacts = []

        # Fetch all elements with the class `gs_ri` (presumably "Google Scholar Row Item")
        for item in etree.xpath('//*[@id="gs_res_ccl_mid"]/div[*]/*[@class="gs_ri"]'):
            # > The .find*() methods are usually faster than the full-blown XPath support
            # - https://lxml.de/xpathxslt.html#xpath

            current_artifact = {}

            # `current_artifact[property_name]` is repeated as `match` has isolated scope
            for property_name in Attributes.__members__.values():
                match property_name:
                    case Attributes.KIND:
                        xpath_result = item.find('.//span[@class="gs_ct1"]')
                        if text := getattr(xpath_result, "text", None):
                            current_artifact[property_name] = text[1:-1].lower()
                        else:
                            current_artifact[property_name] = None
                    case Attributes.LINK:
                        current_artifact[property_name] = item.find(".//a").attrib[
                            "href"
                        ]

            artifacts.append(current_artifact)

        return artifacts
