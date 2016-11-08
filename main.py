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
    func_dict_converting = {}  # state_converting and func_dict_converting should have same length, same order.
    indistinguishable = []
    distinguishable = []
    belong_dict = {}

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
        print(self.func_dict)
        print(from_state)
        if input_symbol in self.func_dict[from_state]:
            return self.func_dict[from_state][input_symbol]
        return False

    def e_closure(self, substate):
        result = list(substate)
        for ss in substate:
            result.append(self.transition(ss, 'E'))
        return my_sorted(result)

    def rename(self):
        # renaming
        self.state = []
        for i in range(len(self.state_converting)):
            self.state.append('q'+str(i))
        self.func_dict = {}
        self.func_dict_converting = list(self.func_dict_converting.items())
        for j in range(len(self.func_dict_converting)):
            self.func_dict_converting[j] = list(self.func_dict_converting[j])
            self.func_dict_converting[j][0] = self.state[self.state_converting.index(list(self.func_dict_converting[j][0]))]
            self.func_dict_converting[j][1] = list(self.func_dict_converting[j][1].items())
            for k in range(len(self.func_dict_converting[j][1])):
                self.func_dict_converting[j][1][k] = list(self.func_dict_converting[j][1][k])
                self.func_dict_converting[j][1][k][1] = self.state[self.state_converting.index(self.func_dict_converting[j][1][k][1])]
        self.func_dict = list(self.func_dict_converting)
        for i in range(len(self.func_dict)):
            self.func_dict[i][1] = dict(self.func_dict[i][1])

        self.func_dict = dict(self.func_dict_converting)
        final_copy = list(self.final)
        self.final = []
        for s_list in self.state_converting:
            if self.initial[0] in s_list:
                self.initial = []
                self.initial.append(self.state[self.state_converting.index(s_list)])
            for s in s_list:
                if s in final_copy:
                    self.final.append(self.state[self.state_converting.index(s_list)])

    def convert_to_dfa(self):
        # converting
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

        self.rename()

        '''
        print(self.state)
        print(self.func_dict)
        print(self.initial)
        print(self.final)
        '''

    def minimize(self):
        end_flag = True
        if not self.indistinguishable:
            for s1 in self.state:
                for s2 in self.state:
                    if (s1 in self.final and s2 in self.final) or (s1 not in self.final and s2 not in self.final):
                        self.indistinguishable.append(my_sorted([s1, s2]))
                    else:
                        self.distinguishable.append(my_sorted([s1, s2]))
        else:
            for i in range(len(self.indistinguishable)):
                if self.is_distinguishable(self.indistinguishable[i]):
                    self.distinguishable.append(self.indistinguishable.pop(i))
                    end_flag = False
        if not end_flag:
            self.minimize()
        else:
            self.aggregate()

    def aggregate(self):
        s = self.indistinguishable[0][0]
        substate = [s]
        self.belong_dict[s] = substate
        for pair in self.indistinguishable:
            if s in pair:
                substate.append(pair[1])
                self.belong_dict[pair[1]] = substate
        self.state_converting.append(substate)
        indistinguishable_copy = list(self.indistinguishable)
        self.indistinguishable = []
        for pair in indistinguishable_copy:
            if (pair[0] not in substate) and (pair[1] not in substate):
                self.indistinguishable.append(pair)
        if self.indistinguishable:
            self.aggregate()
        else:
            self.func_dict_converting = {}
            print('state_converting '+str(self.state_converting))
            for substate in self.state_converting:
                self.func_dict_converting[tuple(substate)] = {}
                for sym in self.symbol:
                    self.func_dict_converting[tuple(substate)][sym] = self.belong_dict[self.transition(substate[0], sym)]
            self.rename()

    def is_distinguishable(self, pair):
        for sym in self.symbol:
            if my_sorted([self.transition(pair[0], sym), self.transition(pair[1], sym)]) in self.distinguishable:
                return True
        return False

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
        for q in my_sorted(list(self.func_dict.keys())):
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


def my_sorted(state_list):
    for i in range(len(state_list)):
        state_list[i] = int(state_list[i][1:])
    state_list = sorted(state_list)
    for i in range(len(state_list)):
        state_list[i] = 'q' + str(state_list[i])
    return state_list


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
    e_nfa.minimize()
    e_nfa.print_self()


main()

