import enum

class TokenType(enum.Enum):
    NONETYPE = 0
    GRAMMATICAL = 1
    PUNCTUATION = 2
    CONSONANT = 3
    VOWEL = 4

class Token:
    def __init__(self, contents, token_type):
        self.contents = contents
        self.token_type = token_type

    def __str__(self):
        return '{0} of type {1}'.format(self.contents, self.token_type)
        # return str(self.contents)

    def __eq__(self, other):
        return self.contents == other.contents and self.token_type == other.token_type