import bz2
import csv

now = 2016
born = 2000
p_t = .005

name = "Silas"

p_now = None
p_born = None

with bz2.BZ2File("data/babynames.csv.bz2", "rb") as names_f:
	reader = csv.reader(names_f)
	reader.next() # Skip headings
	for row in reader:
		r_year = int(row[0])
		r_name = row[2]
		r_p = float(row[4])
		if r_name == name:
			if r_year == born:
				p_born = r_p
			if r_year == now:
				p_now = r_p
				# now has to be after born. ready...
				if not p_born is None and not p_now is None:
					break
				else:
					print "Fatal error not in birth thingy"

# P(t)|P(name) =
# P(name)|P(t) * P(t)
# -------------------
# P(name)
#
# P(name) = P(t)*P(name,2018) + (1-P(t))*P(name,2000)
#
# P(name)|P(t) ~= P(name,2000) (for our purposes, good enough)

def bayes():
	p_name_given_t = p_born
	p_name_given_not_t = p_now
	num = p_name_given_t * p_t
	den = p_t*p_name_given_t + (1-p_t)*p_name_given_not_t
	return num/den

print bayes()
