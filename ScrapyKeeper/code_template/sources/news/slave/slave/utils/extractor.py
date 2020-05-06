from gne import GeneralNewsExtractor


class Extractor(object):
    extractor = GeneralNewsExtractor()

    def extract(self, html_text):
        return self.extractor.extract(html_text)

    def is_detail_page(self, response, threshold: float):
        all_tags = len(response.xpath('//body//*'))
        a_tags = len(response.xpath('//body//a'))
        if round(a_tags / float(all_tags), 2) < threshold or \
                (response.url.endswith(".html") or response.url.endswith(".shtml") or response.url.endswith(".htm")):
            return True
        else:
            return False

