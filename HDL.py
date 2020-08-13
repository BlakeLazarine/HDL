import parser
import re


class Module:

    def __init__(self, inputs, intermediaries, outputs, regs=[]):
        self.inputs = inputs
        self.outputs = outputs
        self.intermediaries = intermediaries
        self.regs = regs
        self.reg_vals = [0 for i in range(len(regs))]
        self.reg_eqns = [None for i in range(len(regs))]
        self.out_eqns = [None for i in range(len(outputs))]
        self.int_eqns = [None for i in range(len(intermediaries))]

    # def def_reg(self, r, e):
    #     if r in self.regs:
    #         for idx in range(len(self.intermediaries)):
    #             intermed = self.intermediaries[idx]
    #             e = re.sub(r'(?<![a-zA-Z0-9])' + intermed + r'(?![a-zA-Z0-9])', "int_vals[" + str(idx) + ']', e)
    #
    #         for idx in range(len(self.inputs)):
    #             inp = self.inputs[idx]
    #             if inp in e:
    #                 e = re.sub(r'(?<![a-zA-Z0-9])' + inp + r'(?![a-zA-Z0-9])', "in_vals[" + str(idx) + ']', e)
    #
    #         for idx in range(len(self.regs)):
    #             reg = self.regs[idx]
    #             if reg in e:
    #                 e = re.sub(r'(?<![a-zA-Z0-9])' + reg + r'(?![a-zA-Z0-9])', "self.reg_vals[" + str(idx) + ']', e)
    #
    #         #print(e)
    #         self.reg_eqns[self.regs.index(r)] = e
    #     else:
    #         print(r, "is not a register")
    #
    # def def_intermed(self, i, e):
    #     if i in self.intermediaries:
    #         for idx in range(len(self.intermediaries)):
    #             intermed = self.intermediaries[idx]
    #             e = re.sub(r'(?<![a-zA-Z0-9])' + intermed + r'(?![a-zA-Z0-9])', "int_vals[" + str(idx) + ']', e)
    #
    #         for idx in range(len(self.inputs)):
    #             inp = self.inputs[idx]
    #             if inp in e:
    #                 e = re.sub(r'(?<![a-zA-Z0-9])' + inp + r'(?![a-zA-Z0-9])', "in_vals[" + str(idx) + ']', e)
    #
    #         for idx in range(len(self.regs)):
    #             reg = self.regs[idx]
    #             if reg in e:
    #                 e = re.sub(r'(?<![a-zA-Z0-9])' + reg + r'(?![a-zA-Z0-9])', "self.reg_vals[" + str(idx) + ']', e)
    #
    #         #print(e)
    #         self.int_eqns[self.intermediaries.index(i)] = e
    #     else:
    #         print(i, "is not an intermediary")
    #
    # def def_out(self, o, e):
    #     if o in self.outputs:
    #         for idx in range(len(self.intermediaries)):
    #             intermed = self.intermediaries[idx]
    #             e = re.sub(r'(?<![a-zA-Z0-9])' + intermed + r'(?![a-zA-Z0-9])', "int_vals[" + str(idx) + ']', e)
    #                 #e = e.replace(intermed, "int_vals[" + str(idx) + ']')
    #
    #         for idx in range(len(self.inputs)):
    #             inp = self.inputs[idx]
    #             #print(inp, e, inp in e)
    #
    #             e = re.sub(r'(?<![a-zA-Z0-9])' + inp + r'(?![a-zA-Z0-9])', "in_vals[" + str(idx) + ']', e)
    #                 #e = e.replace(inp, "in_vals[" + str(idx) + ']')
    #
    #         for idx in range(len(self.regs)):
    #             reg = self.regs[idx]
    #             if reg in e:
    #                 e = re.sub(r'(?<![a-zA-Z0-9])' + reg + r'(?![a-zA-Z0-9])', "self.reg_vals[" + str(idx) + ']', e)
    #
    #         #print(e)
    #         self.out_eqns[self.outputs.index(o)] = e
    #     else:
    #         print(o, "is not an output")

    def assign(self, i, e):
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

    def evaluate(self, in_vals):
        int_vals = [None for i in range(len(self.intermediaries))]
        while None in int_vals:
            for i in range(len(self.intermediaries)):
                if not int_vals[i] is None:
                    continue
                int_match = re.findall(r'int_vals\[(\d+)\]', self.int_eqns[i])
                for m in int_match:
                    if int_vals[m] is None:
                        break
                else:
                    int_vals[i] = eval(parser.expr(self.int_eqns[i]).compile())

        out_vals = [None for i in range(len(self.outputs))]
        # print(in_vals)
        # print(int_vals)
        for i in range(len(self.outputs)):
            #print(self.out_eqns[i])
            out_vals[i] = eval(parser.expr(self.out_eqns[i]).compile())
            #print('out', eval(parser.expr(self.out_eqns[i]).compile()))

        for i in range(len(self.regs)):
            #print(self.out_eqns[i])
            self.reg_vals[i] = eval(parser.expr(self.reg_eqns[i]).compile())

        return out_vals


test = Module(['a', 'b', 'c'], ['d'], ['e', 'f'])
test.assign('d', 'a + b')
test.assign('e', 'd + c')
test.assign('f', 'd + a&b')
print(test.evaluate([1,2,3]))

new_test = Module(['a'], [], ['b'], regs=['r'])
new_test.assign('b', 'r')
new_test.assign('r', 'r + a')
print(new_test.evaluate([1]))
print(new_test.evaluate([1]))
print(new_test.evaluate([1]))
print(new_test.evaluate([1]))
