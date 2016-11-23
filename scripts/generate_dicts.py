

from dashboard.models import Time as T, Node as N, Year as Y, Month as M, Day as D

# NODES DICT
nodes = [(n.id,n.name.replace(' ',''),) for n in N.objects.all().order_by('name')]

# TIMES DICT
times = {t.char_rep:t.id for t in T.objects.all()}

# YEARS DICT
years = {str(y.year):y.id for y in Y.objects.all()}

# MONTH DICT
months = {m.char_rep:m.id for m in M.objects.all()}

# DAYS DICT
days = {d.char_rep:d.id for d in D.objects.all()}
