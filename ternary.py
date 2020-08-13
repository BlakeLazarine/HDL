import re


def convert_ternary(s):
    removed_name = 'reahjkfhdjakhsal'
    removed = []
    while s.count('(') > 0:
        m = re.search(r'(\([^\(\)]+\))', s).group(1)
        s = s.replace(m, removed_name + str(len(removed)))
        removed.append(m)

    while len(removed) > 0:
        st = re.sub(r'([^\(\)]+)\?([^\(\)]+):([^\(\)]+)', r'\2 if \1 else \3', s)
        if st != s:
            s = '(' + st + ')'
        s = s.replace(removed_name + str(len(removed)-1), removed.pop(-1))
    st = re.sub(r'([^\(\)]+)\?([^\(\)]+):([^\(\)]+)', r'\2 if \1 else \3', s)
    if st != s:
        s = '(' + st + ')'
    s = re.sub(r' +', ' ', s)

    return s

print(convert_ternary('(d ? e : f)'))
print(convert_ternary('a + b ? c : (d ? e : f)'))
print(convert_ternary('a + b ? c : ((d+g)*h ? e : f)'))


print(convert_ternary('a + b ? (d ? e : f) : c'))
