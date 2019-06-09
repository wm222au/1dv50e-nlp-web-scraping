class HarvestEngine:
    def __init__(self, options):
        self.options = options
        self.parsers = []
        self.data = []

    def add_parser(self, parser):
        self.parsers.append(parser)

    def add_data(self, data):
        self.data.append(data)

    def run(self):
        print("Running parsers through scraper")

        for parser in self.parsers:
            parser.run(self.data)