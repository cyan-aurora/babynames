import argparse
import bz2
import csv

parser = argparse.ArgumentParser()
parser.add_argument("born", type=int, help="the year you were born")
parser.add_argument("--now", type=int, default=2016, help="how many tnames to show")
parser.add_argument("--gender", choices=["M","F","any","neutral"], help="only display names from this gender. Data only includes M/F, any uses M+F, neutral finds M/F ~= .5")
parser.add_argument("--neutral-weight", type=float, default=2, help="how heavily to weight gender-neutrality vs probability")
parser.add_argument("--display", type=int, default=10, help="how many tnames to show")
parser.add_argument("--check", type=str, help="display the bayes' rule probability for a given name")
args = parser.parse_args()

p_t = .005

p_now = {}
p_born = {}

with bz2.BZ2File("data/babynames.csv.bz2", "rb") as names_f:
	reader = csv.reader(names_f)
	reader.next() # Skip headings
	for row in reader:
		r_year = int(row[0])
		r_gender = row[1]
		r_name = row[2]
		r_p = float(row[4])
		if r_year == args.born:
			p_born[(r_name, r_gender)] = r_p
		if r_year == args.now:
			p_now[(r_name, r_gender)] = r_p

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

def p_name(d, name):
	if args.gender == "M" or args.gender == "F":
		return val_or_zero(d, (name, args.gender))
	elif args.gender == "any" or args.gender == "neutral":
		return val_or_zero(d, (name, "M")) + val_or_zero(d, (name, "F"))

def bayes(name):
	p_name_given_t = p_name(p_now, name)
	p_name_given_not_t = p_name(p_born, name)
	num = p_name_given_t * p_t
	den = p_t*p_name_given_t + (1-p_t)*p_name_given_not_t
	if den == 0:
		return 0
	return num/den

def fmt_percent(f):
	return "{:.3%}".format(f)

def neutral(m, f):
	if f == 0 or m == 0:
		return 0
	error = 1 - abs(m-f)/(m+f)
	return error

def value(bayes, neutral):
	# Small numbers are better for bayes so subtract neutrality
	# Multiply times .02 to make --neutral-weight sane numbers like 10
	return bayes - args.neutral_weight * .01 * neutral

if args.check:
	print fmt_percent(bayes(args.check))
else:
	by_value = []
	for (name, gender) in p_born:
		b = bayes(name)
		# Ignore b == 0, they're outlier names
		if b > 0:
			if args.gender == "neutral":
				m = val_or_zero(p_born, (name, "M"))
				f = val_or_zero(p_born, (name, "F"))
				v = value(b, neutral(m, f))
			else:
				v = b
			if not ((v, name)) in by_value:
				by_value.append((v, name))
	by_value.sort()

	for i in range(args.display):
		t = by_value[i]
		name = t[1]
		b = t[0]
		print "{} ({})".format(name, fmt_percent(b)) 

