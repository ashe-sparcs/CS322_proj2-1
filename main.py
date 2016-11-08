import sys


class ENfa:
    state = []
    symbol = []
    func_dict = {}
    # func_string_list = []
    initial = []
    final = []
    todo_queue = []
    state_converting = []
    func_dict_converting = {} # state_converting and func_dict_converting should have same length, same order.

    def __init__(self, state, symbol, func_string_list, initial, final):
        self.state = state
        self.symbol = symbol
        # self.func_string_list = func_string_list
        for q in state:
            self.func_dict[q] = {}
            self.func_dict[q]['E'] = {}
        for func_string in func_string_list:
            func_string_split = func_string.split(',')
            self.func_dict[func_string_split[0]][func_string_split[1]] = func_string_split[2]
        self.initial = list(initial)
        self.final = final
        self.todo_queue.append(self.e_closure(self.initial))
        self.state_converting = list(self.todo_queue)

    def transition(self, from_state, input_symbol):
        if input_symbol in self.func_dict[from_state]:
            return self.func_dict[from_state][input_symbol]
        return False

    def e_closure(self, substate):
        result = list(substate)
        for ss in substate:
            result.append(self.transition(ss, 'E'))
        return sorted(result)

    def convert_to_dfa(self):
        while self.todo_queue:
            from_substate = self.todo_queue[0]
            for sym in self.symbol:
                to_substate = []
                for fs in from_substate:
                    if self.transition(fs, sym):
                        to_substate.append(self.transition(fs, sym))
                if to_substate:
                    to_substate = self.e_closure(to_substate)
                if to_substate and (to_substate not in self.state_converting):
                    self.state_converting.append(list(to_substate))
                    if to_substate not in self.todo_queue:
                        self.todo_queue.append(list(to_substate))
                if self.func_dict_converting.get(tuple(from_substate)) is None:
                    self.func_dict_converting[tuple(from_substate)] = {}
                self.func_dict_converting[tuple(from_substate)][sym] = list(to_substate)
            self.todo_queue.pop(0)
        print(self.state_converting)
        print(self.func_dict_converting)
        self.state = []
        for i in range(len(self.state_converting)):
            self.state.append('q'+str(i))
        self.func_dict = {}
        for from_substate in self.func_dict_converting.keys():
            from_substate = list(from_substate)
            # self.func_dict

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
        print(','.join(self.initial))
        print('Final state')
        print(','.join(self.final))


class Dfa(ENfa):
    def __init__(self, state, symbol, func_string_list, initial, final):
        ENfa.__init__(self, state, symbol, func_string_list, initial, final)
        for key in list(self.func_dict.keys()):
            del self.func_dict[key]['E']

    def rename(self):
        pass

    def minimize(self):
        pass


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
    q0 = dfa_file.readline().strip().split(',')
    dfa_file.readline()  # Final State
    f = dfa_file.readline().strip().split(',')

    # dfa = Dfa(q, sigma, func_string_list, q0, f)
    # dfa.print_self()

    e_nfa = ENfa(q, sigma, func_string_list, q0, f)
    e_nfa.convert_to_dfa()


main()

