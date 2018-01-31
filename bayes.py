import bz2
import csv

now = 2016
born = 2000
p_t = .005

p_now = {}
p_born = {}

with bz2.BZ2File("data/babynames.csv.bz2", "rb") as names_f:
	reader = csv.reader(names_f)
	reader.next() # Skip headings
	for row in reader:
		r_year = int(row[0])
		r_name = row[2]
		r_p = float(row[4])
		if r_year == born:
			p_born[r_name] = r_p
		if r_year == now:
			p_now[r_name] = r_p

# P(t)|P(name) =
# P(name)|P(t) * P(t)
# -------------------
# P(name)
#
# P(name) = P(t)*P(name,2018) + (1-P(t))*P(name,2000)
#
# P(name)|P(t) ~= P(name,2000) (for our purposes, good enough)

def val_or_zero(d, key):
	if key in d: return d[key]
	else: return 0

def p_name_born(name):
	return val_or_zero(p_born, name)

def p_name_now(name):
	return val_or_zero(p_now, name)

def bayes(name):
	p_name_given_t = p_name_now(name)
	p_name_given_not_t = p_name_born(name)
	num = p_name_given_t * p_t
	den = p_t*p_name_given_t + (1-p_t)*p_name_given_not_t
	return num/den

by_bayes = []
for name in p_born:
	b = bayes(name)
	# Ignore b == 0, they're outlier names
	if b > 0:
		by_bayes.append((b, name))
by_bayes.sort()

for i in range(10):
	t = by_bayes[i]
	name = t[1]
	b = t[0]
	print("{} ({})".format(name, b))
