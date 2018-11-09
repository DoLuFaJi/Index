class InvertedFileEntry:
    def __init__(self, term):
        self.term = term
        self.pl_size = 0

    def __hash__(self):
        return hash(self.term)

    def __eq__(self, other):
        return self.term == other

    def __str__(self):
        return self.term

    def __repr__(self):
        return self.term
