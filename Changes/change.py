class Change:
    """
    A data object that represents the data relevant to a wiki change. Also contains operators and methods
    to sort those pieces of data
    """

    def __init__(self, date_time, article_name, article_link):
        self.date_time = date_time
        self.article_name = article_name
        self.article_link = article_link

    def __str__(self):
        return f'{{"date_time": {self.date_time}, "article_name": {self.article_name}, "article_link": {self.article_link}}}'