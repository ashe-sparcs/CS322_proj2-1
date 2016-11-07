import sys


class ENfa:
    state = []
    symbol = []
    func_dict = {}
    func_string_list = []
    initial = ''
    final = []

    def __init__(self, state, symbol, func_string_list, initial, final):
        self.state = state
        self.symbol = symbol
        self.func_string_list = func_string_list
        for q in state:
            self.func_dict[q] = {}
            self.func_dict[q]['E'] = {}
        for func_string in func_string_list:
            func_string_split = func_string.split(',')
            self.func_dict[func_string_split[0]][func_string_split[1]] = func_string_split[2]
        self.initial = initial
        self.final = final

    def transition(self, from_state, input_symbol):
        return self.func_dict[from_state][input_symbol]

    def print_self(self):
        print('State')
        print(','.join(self.state))
        print('Input symbol')
        print(','.join(self.symbol))
        print('State transition function')
        '''
        for func_string in self.func_string_list:
            print(func_string)
        '''
        for q in sorted(list(self.func_dict.keys())):
            for sym in sorted(list(self.func_dict[q])):
                print(q + ',' + sym + ',' + self.transition(q, sym))
        print('Initial state')
        print(self.initial)
        print('Final state')
        print(','.join(self.final))


class Dfa(ENfa):
    def __init__(self, state, symbol, func_string_list, initial, final):
        ENfa.__init__(self, state, symbol, func_string_list, initial, final)
        for key in list(self.func_dict.keys()):
            del self.func_dict[key]['E']
        self.initial = initial
        self.final = final


def main():
    dfa_filename = sys.argv[1]
    # output = sys.argv[2]
    dfa_file = open(dfa_filename, 'r')
    # output_file = open(output, 'w')

    dfa_file.readline()  # State
    q = dfa_file.readline().strip().split(',')  # state
    dfa_file.readline()  # Input symbol
    sigma = dfa_file.readline().strip().split(',')  # symbol
    dfa_file.readline()  # State transition function
    func_string_list = []
    while True:
        line_temp = dfa_file.readline().strip()
        if line_temp == 'Initial state':
            break
        func_string_list.append(line_temp)
    # Initial State
    q0 = dfa_file.readline().strip()
    dfa_file.readline()  # Final State
    f = dfa_file.readline().strip().split(',')

    dfa = Dfa(q, sigma, func_string_list, q0, f)
    dfa.print_self()


main()


