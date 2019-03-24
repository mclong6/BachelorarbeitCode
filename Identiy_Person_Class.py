import articleDateExtractor


class IdentifyPerson:
    def compare_year:
        d = articleDateExtractor.extractArticlePublishedDate("http://edition.cnn.com/2015/11/28/opinions/\
        sutter-cop21-paris-preview-two-degrees/index.html")
        print(d)