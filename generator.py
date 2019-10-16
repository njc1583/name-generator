class Generator:
    TERMINAL = "TERMINAL"
    INITIAL = "INITIAL"

    def __init__(self, culture, city_data, grammar={}):
        self.culture = culture
        self.city_data = city_data
        self.grammar = grammar

    def generate_grammar(self):
        self.grammar = {}

        self.grammar[self.INITIAL] = {}

        for city in self.city_data['cities']:
            initial_char = city[0].lower()

            if initial_char not in self.grammar[self.INITIAL]:
                self.grammar[self.INITIAL][initial_char] = 0

            self.grammar[self.INITIAL][initial_char] += 1

            for i in range(len(city)-1):
                prefix = city[i].lower()
                suffix = city[i+1].lower()

                if prefix not in self.grammar:
                    self.grammar[prefix] = {}

                if suffix not in self.grammar[prefix]:
                    self.grammar[prefix][suffix] = 0
                
                self.grammar[prefix][suffix] += 1

            end_char = city[len(city)-1].lower()

            if end_char not in self.grammar:
                self.grammar[end_char] = {}

            if self.TERMINAL not in self.grammar[end_char]:
                self.grammar[end_char][self.TERMINAL] = 0

            self.grammar[end_char][self.TERMINAL] += 1

        print(self.grammar)

    def generate_graph(self):
        with open(self.culture + '_grammar.DOT', 'w', encoding='utf-8') as dotfile:
            dotfile.write('digraph {\n')

            for node in self.grammar:
                # node_str = node

                node_str = '\"{}\"'.format(node)

                # if node_str == ' ':
                #     node_str = '\" \"'

                dotfile.write('\t{0} [shape=circle]\n'.format(node_str))

                for destination in self.grammar[node]:
                    dest_str = '\"{}\"'.format(destination)

                    # if dest_str == ' ':
                    #     dest_str = '\" \"'

                    dotfile.write('\t{0} -> {1} [label={2}]\n'.format(node_str, dest_str, self.grammar[node][destination]))

            dotfile.write('}\n')