import re


class Register:
    # a struct would be better for this

    def __init__(self, name, default, trigger, eqn=''):
        self.name = name
        self.value = default
        self.trigger = trigger #string
        self.trig_prev = False
        self.eqn = eqn

    def assign(self, eqn):
        self.eqn = eqn


class Module:

    def __init__(self):
        self.inputs = []
        self.in_vals = []
        self.outputs = []
        self.wires = []
        self.regs = []
        self.out_eqns = []
        self.wire_eqns = []

    def assign(self, name, eqn):
        for idx in range(len(self.intermediaries)):
            intermed = self.intermediaries[idx]
            e = re.sub(r'(?<![a-zA-Z0-9])' + intermed + r'(?![a-zA-Z0-9])', "int_vals[" + str(idx) + ']', e)
            # e = e.replace(intermed, "int_vals[" + str(idx) + ']')

        for idx in range(len(self.inputs)):
            inp = self.inputs[idx]
            # print(inp, e, inp in e)

            e = re.sub(r'(?<![a-zA-Z0-9])' + inp + r'(?![a-zA-Z0-9])', "in_vals[" + str(idx) + ']', e)
            # e = e.replace(inp, "in_vals[" + str(idx) + ']')

        for idx in range(len(self.regs)):
            reg = self.regs[idx]
            if reg in e:
                e = re.sub(r'(?<![a-zA-Z0-9])' + reg + r'(?![a-zA-Z0-9])', "self.reg_vals[" + str(idx) + ']', e)

        # print(e)
        if i in self.outputs:
            self.out_eqns[self.outputs.index(i)] = e
        elif i in self.intermediaries:
            self.int_eqns[self.intermediaries.index(i)] = e
        elif i in self.regs:
            self.reg_eqns[self.regs.index(i)] = e
        else:
            print(i, "not a defined value")

    def add_input(self, name, size):
        self.inputs.append(name)
        self.in_vals.append(0)

    def add_output(self, name, size):
        self.outputs.append(name)
        self.out_eqns.append('')

    def add_wire(self, name, size, eqn):
        self.wires.append(name)
        self.wire_eqns.append('')
        self.assign(name, eqn)

    def add_register(self, name, size, default, trig_sign, trigger, eqn=''):
        trigstr = '!' if trig_sign == 'negedge' else ''
        #append the array value name for trigger

        self.regs.append(Register(name, default, trigstr, eqn))

    def update(self):
        pass

    def set_in(self, name, val):
        if name in self.inputs:
            self.in_vals[self.inputs.index(name)] = val

    def print_info(self):
        print('--Inputs--')
        for i in range(len(self.inputs)):
            print(self.inputs[i], '=', self.in_vals[i])

        print('--Outputs--')
        for i in range(len(self.outputs)):
            print(self.outputs[i], '=', self.out_eqns[i])

        print('--Wires--')
        for i in range(len(self.wires)):
            print(self.wires[i], '=', self.wire_eqns[i])

        print('--Regs--')
        for r in self.regs:
            print(r.name, r.value, r.trigger, r.eqn)

