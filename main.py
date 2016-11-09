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
    state_aggregating = []
    func_dict_converting = {}  # state_converting and func_dict_converting should have same length, same order.
    func_dict_aggregating = {}
    indistinguishable = []
    distinguishable = []
    belong_dict = {}

    def __init__(self, state, symbol, func_string_list, initial, final):
        self.state = state
        self.symbol = symbol
        # self.func_string_list = func_string_list
        for q in state:
            self.func_dict[q] = {}
            # self.func_dict[q]['E'] = {}
        for func_string in func_string_list:
            func_string_split = func_string.split(',')
            if func_string_split[1] not in self.func_dict[func_string_split[0]].keys():
                self.func_dict[func_string_split[0]][func_string_split[1]] = []
            self.func_dict[func_string_split[0]][func_string_split[1]].append(func_string_split[2])
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
            closure = self.transition(ss, 'E')
            if not closure:
                continue
            elif isinstance(closure, list):
                result = result + self.transition(ss, 'E')
            else:
                result.append(closure)
        return my_sorted(result)

    def rename_converting(self):
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

    def rename_aggregating(self):
        # renaming
        self.state = []
        for i in range(len(self.state_aggregating)):
            self.state.append('q'+str(i))
        self.func_dict = {}
        self.func_dict_aggregating = list(self.func_dict_aggregating.items())
        for j in range(len(self.func_dict_aggregating)):
            self.func_dict_aggregating[j] = list(self.func_dict_aggregating[j])
            self.func_dict_aggregating[j][0] = self.state[self.state_aggregating.index(list(self.func_dict_aggregating[j][0]))]
            self.func_dict_aggregating[j][1] = list(self.func_dict_aggregating[j][1].items())
            for k in range(len(self.func_dict_aggregating[j][1])):
                self.func_dict_aggregating[j][1][k] = list(self.func_dict_aggregating[j][1][k])
                self.func_dict_aggregating[j][1][k][1] = self.state[self.state_aggregating.index(self.func_dict_aggregating[j][1][k][1])]
        self.func_dict = list(self.func_dict_aggregating)
        for i in range(len(self.func_dict)):
            self.func_dict[i][1] = dict(self.func_dict[i][1])

        self.func_dict = dict(self.func_dict_aggregating)
        final_copy = list(self.final)
        self.final = []
        for s_list in self.state_aggregating:
            if self.initial[0] in s_list:
                self.initial = []
                self.initial.append(self.state[self.state_aggregating.index(s_list)])
            for s in s_list:
                if s in final_copy and self.state[self.state_aggregating.index(s_list)] not in self.final:
                    self.final.append(self.state[self.state_aggregating.index(s_list)])

    def convert_to_dfa(self):
        # converting
        while self.todo_queue:
            from_substate = self.todo_queue[0]
            for sym in self.symbol:
                to_substate = []
                for fs in from_substate:
                    transition = self.transition(fs, sym)
                    if not transition:
                        pass
                    elif isinstance(transition, list):
                        to_substate = to_substate + transition
                    else:
                        to_substate.append(transition)
                if to_substate:
                    to_substate = self.e_closure(to_substate)
                if to_substate and (to_substate not in self.state_converting):
                    self.state_converting.append(list(to_substate))
                    if to_substate not in self.todo_queue:
                        self.todo_queue.append(list(to_substate))
                if self.func_dict_converting.get(tuple(from_substate)) is None:
                    self.func_dict_converting[tuple(from_substate)] = {}
                if to_substate:
                    self.func_dict_converting[tuple(from_substate)][sym] = list(to_substate)
            self.todo_queue.pop(0)

        self.rename_converting()

    def minimize(self):
        end_flag = True
        if not self.distinguishable:
            print('self.state : ')
            print(self.state)
            for s1 in self.state:
                for s2 in self.state:
                    if (s1 not in self.final and s2 in self.final) or (s1 in self.final and s2 not in self.final):
                        if my_sorted([s1, s2]) not in self.distinguishable:
                            self.distinguishable.append(my_sorted([s1, s2]))
                            end_flag = False
        else:
            for s1 in self.state:
                for s2 in self.state:
                    if my_sorted([s1, s2]) not in self.distinguishable:
                        if self.is_distinguishable([s1, s2]):
                            self.distinguishable.append(my_sorted([s1, s2]))
                            end_flag = False
        if not end_flag:
            self.minimize()
        else:
            for s1 in self.state:
                for s2 in self.state:
                    if my_sorted([s1, s2]) not in self.distinguishable and my_sorted([s1, s2]) not in self.indistinguishable:
                        self.indistinguishable.append(my_sorted([s1, s2]))
            self.aggregate()

    def find_intersection(self, m_list):
        for i, v in enumerate(m_list):
            for j, k in enumerate(m_list[i+1:], i+1):
                if v & k:
                    self.state_aggregating[i] = v.union(m_list.pop(j))
                    return self.find_intersection(m_list)
        return m_list

    def aggregate(self):
        self.state_aggregating = [set(i) for i in self.indistinguishable if i]
        self.find_intersection(self.state_aggregating)
        self.state_aggregating = [list(i) for i in self.state_aggregating if i]
        print('self.state_aggregating : ')
        print(self.state_aggregating)
        for s in self.state:
            if s not in sum(self.indistinguishable, []):
                self.state_aggregating.append([s])
        for substate in self.state_aggregating:
            for s in substate:
                self.belong_dict[s] = substate
        for substate in self.state_aggregating:
            self.func_dict_aggregating[tuple(substate)] = {}
            for sym in self.symbol:
                if self.transition(substate[0], sym):
                    self.func_dict_aggregating[tuple(substate)][sym] = self.belong_dict[self.transition(substate[0], sym)]
        print('self.func_dict_aggregating: ')
        print(self.func_dict_aggregating)
        self.rename_aggregating()

    def is_distinguishable(self, pair):
        for sym in self.symbol:
            transition1 = self.transition(pair[0], sym)
            transition2 = self.transition(pair[1], sym)
            if my_sorted([transition1, transition2]) in self.distinguishable:
                return True
        return False

    def print_self(self):
        print('State')
        print(','.join(self.state))
        print('Input symbol')
        print(','.join(self.symbol))
        print('State transition function')
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
    if False in state_list:
        return state_list
    for i in range(len(state_list)):
        state_list[i] = int(state_list[i][1:])
    state_list = sorted(state_list)
    for i in range(len(state_list)):
        state_list[i] = 'q' + str(state_list[i])
    return state_list


def xor(b1, b2):
    return (b1 and not b2) or (not b1 and b2)


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
    e_nfa.print_self()
    print('@@@@@@@@@@@@@@@@@')
    e_nfa.minimize()
    e_nfa.print_self()


main()

