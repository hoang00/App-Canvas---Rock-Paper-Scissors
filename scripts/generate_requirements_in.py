import re
out=[]
with open('requirements.txt') as f:
    for l in f:
        l=l.strip()
        if not l or l.startswith('#'):
            continue
        pkg = re.split(r'==|>=|<=|~=|===|!=|<|>', l)[0].strip()
        if pkg:
            out.append(pkg)
with open('requirements.in','w') as f:
    f.write('\n'.join(out))
print('wrote requirements.in with %d packages' % len(out))