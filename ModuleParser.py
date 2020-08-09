import re
vtext = open("ha1_1.v").read()
operations = ['+', '-', '*', '/', '<', '>', '==', '!', '!=', '<<', '>>', '|', '&', '||', '&&', '^', '%', '<=', '>=']
special = '?:()'
input_names = []
output_names = []
for i in re.findall(r'input(.*)[;,]', vtext):
    input_names += [s.strip().split(' ')[-1] for s in i.split(',')]

for i in re.findall(r'output(.*)[;,]', vtext):
    output_names += [s.strip().split(' ')[-1] for s in i.split(',')]
print(input_names)
print(output_names)

for n in output_names:
    print(n + ' = ' + re.search(n + r'.*[^!>=]=[^=](.*);', vtext).group(1))
