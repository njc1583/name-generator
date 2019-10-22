import re
from token import Token
from token import TokenType

VOWEL_REGEX = re.compile('[aeiou]')

class Generator:
    TERMINAL = "TERMINAL"
    INITIAL = "INITIAL"

    def __init__(self, culture, city_data, grammar={}):
        self.culture = culture
        self.city_data = city_data
        self.grammar = grammar
        self.tokens = None

    # def generate_grammar(self):
    #     self.grammar = {}

    #     self.grammar[self.INITIAL] = {}

    #     for city in self.city_data['cities']:
    #         initial_char = city[0].lower()

    #         if initial_char not in self.grammar[self.INITIAL]:
    #             self.grammar[self.INITIAL][initial_char] = 0

    #         self.grammar[self.INITIAL][initial_char] += 1

    #         for i in range(len(city)-1):
    #             prefix = city[i].lower()
    #             suffix = city[i+1].lower()

    #             if prefix not in self.grammar:
    #                 self.grammar[prefix] = {}

    #             if suffix not in self.grammar[prefix]:
    #                 self.grammar[prefix][suffix] = 0
                
    #             self.grammar[prefix][suffix] += 1

    #         end_char = city[len(city)-1].lower()

    #         if end_char not in self.grammar:
    #             self.grammar[end_char] = {}

    #         if self.TERMINAL not in self.grammar[end_char]:
    #             self.grammar[end_char][self.TERMINAL] = 0

    #         self.grammar[end_char][self.TERMINAL] += 1

    #     print(self.grammar)
    
    def generate_tokens(self):
        token_frequency = {}

        tokens = []

        count = 0
        average_freq = 0

        for city in self.city_data['cities']:
            city_split = city.lower().split(' ')

            count += len(city_split)

            for word in city_split:
                if word not in token_frequency:
                    token_frequency[word] = 0

                token_frequency[word] += 1

        for token in token_frequency:
            token_frequency[token] /= count
            average_freq += token_frequency[token]

        average_freq /= count

        for token in token_frequency:
            if token_frequency[token] > average_freq: 
                potential_token = Token(contents=token, token_type=TokenType.GRAMMATICAL)

                if potential_token not in tokens:
                    tokens.append(potential_token)
            else:
                for char in token:
                    potential_token = Token(contents=char, token_type=TokenType.NONETYPE)

                    if re.search(VOWEL_REGEX, char):
                        potential_token.token_type=TokenType.VOWEL
                    else:
                        potential_token.token_type=TokenType.CONSONANT

                    if potential_token not in tokens:
                        tokens.append(potential_token)
    
        return tokens

    def generate_grammar(self):
        self.tokens = self.generate_tokens()

        self.grammar = {}

    def generate_graph(self, tolerance=0.10):
        with open(self.culture + '_grammar.DOT', 'w', encoding='utf-8') as dotfile:
            dotfile.write('digraph {\n')

            for node in self.grammar:
                node_str = '\"{}\"'.format(node)

                dotfile.write('\t{0} [shape=circle]\n'.format(node_str))

                for destination in self.grammar[node]:
                    dest_str = '\"{}\"'.format(destination)

                    dotfile.write('\t{0} -> {1} [label={2}]\n'.format(node_str, dest_str, self.grammar[node][destination]))

            dotfile.write('}\n')