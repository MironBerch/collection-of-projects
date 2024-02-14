f = open('вопросы.md').readlines()
import os
to_remove = []
for p in f:
    if p[:5] != '- [ ]':
        var = p.split('[[')[-1].split(']]')[0]
        os.remove(f'answers/{var}.md')
