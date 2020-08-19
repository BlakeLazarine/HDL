import re
import ternary
import parser


class Register:
    # a struct would be better for this

    def __init__(self, name, default, trigger, eqn=''):
        self.name = name
        self.value = int(default)
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

        eqn = ternary.convert_ternary(eqn)

        for idx in range(len(self.wires)):
            wire = self.wires[idx]
            eqn = re.sub(r'(?<![a-zA-Z0-9])' + wire + r'(?![a-zA-Z0-9])', "wire_vals[" + str(idx) + ']', eqn)
            # e = e.replace(intermed, "int_vals[" + str(idx) + ']')

        for idx in range(len(self.inputs)):
            inp = self.inputs[idx]
            # print(inp, e, inp in e)

            eqn = re.sub(r'(?<![a-zA-Z0-9])' + inp + r'(?![a-zA-Z0-9])', "self.in_vals[" + str(idx) + ']', eqn)
            # e = e.replace(inp, "in_vals[" + str(idx) + ']')

        for idx in range(len(self.regs)):
            reg = self.regs[idx]
            if reg.name in eqn:
                eqn = re.sub(r'(?<![a-zA-Z0-9])' + reg.name + r'(?![a-zA-Z0-9])', "self.regs[" + str(idx) + '].value', eqn)

        # print(e)
        if name in self.outputs:
            self.out_eqns[self.outputs.index(name)] = eqn
        elif name in self.wires:
            self.wire_eqns[self.wires.index(name)] = eqn
        else:
            for i in self.regs:
                if i.name == name:
                    i.eqn = eqn
                    return
            print(name, 'is not a defined value')

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

    def add_reg(self, name, size, default, trig_sign, trigger, eqn=''):
        trigstr = 'not ' if trig_sign == 'negedge' else ''
        #append the array value name for trigger
        if trigger in self.inputs:
            trigstr += 'self.in_vals[' + str(self.inputs.index(trigger)) + ']'
        if trigger in self.wires:
            trigstr += 'self.wire_vals[' + str(self.wires.index(trigger)) + ']'

        self.regs.append(Register(name, default, trigstr))
        self.assign(name, eqn)

    def update(self):
        wire_vals = [None for i in range(len(self.wires))]
        while None in wire_vals:
            for i in range(len(self.wires)):
                if not wire_vals[i] is None:
                    continue
                wire_match = re.findall(r'int_vals\[(\d+)\]', self.wire_eqns[i])
                for m in wire_match:
                    if wire_vals[m] is None:
                        break
                else:
                    wire_vals[i] = eval(parser.expr(self.wire_eqns[i]).compile())

        out_vals = [None for i in range(len(self.outputs))]
        # print(in_vals)
        # print(int_vals)
        for i in range(len(self.outputs)):
            # print(self.out_eqns[i])
            out_vals[i] = eval(parser.expr(self.out_eqns[i]).compile())
            # print('out', eval(parser.expr(self.out_eqns[i]).compile()))

        for r in self.regs:
            # print('hello', r.trigger)
            if eval(parser.expr(r.trigger).compile()) and not r.trig_prev:
                r.value = eval(parser.expr(r.eqn).compile())
            r.trig_prev = eval(parser.expr(r.trigger).compile())

        return out_vals

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

