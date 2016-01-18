from collections import defaultdict

def genderID(userfile):
	maleid = set()
	femaleid = set()
	unknownid = set()

	for line in open(userfile):
		words = line.strip().split(',')
		if words[0] == 'male':
			maleid.add(words[-1])
		elif words[0] == 'female':
			femaleid.add(words[-1])
		elif words[0] == 'unknown':
			unknownid.add(words[-1])
	return maleid, femaleid, unknownid

maleid, femaleid, unknownid = genderID("user_data_sample.csv")

fp = open("Warm-up.csv", 'w')
fp.write("userid, gender, trackid")
fp.write("\n")

for line in open("end_song_sample.csv"):
	words = line.strip().split(',')
	if words[0] == "ms_played":
		continue

	if words[-1] in maleid:
		fp.write(words[-1]+',male,'+str(words[2]))
		fp.write("\n")

	if words[-1] in femaleid:
		fp.write(words[-1]+',female,'+str(words[2]))
		fp.write("\n")

	if words[-1] in unknownid:
		fp.write(words[-1]+',unknown,'+str(words[2]))
		fp.write("\n")

fp.close()

maledict = defaultdict(set)
femaledict = defaultdict(set)
unknowndict = defaultdict(set)

for line in open("Warm-up.csv"):
	words = line.strip().split(',')
	if words[0] == "userid":
		continue
	if words[0] in maleid:
		maledict[words[0]].add(words[2])
	if words[0] in femaleid:
		femaledict[words[0]].add(words[2])
	if words[0] in unknownid:
		unknowndict[words[0]].add(words[2])
print maledict
fp = open("Warm-up-final.csv", 'w')
fp.write("gender, userid, numtracks")
fp.write("\n")
for key, value in maledict.iteritems():
	fp.write("male,"+key+','+str(len(maledict[key])))
	fp.write("\n")
for key, value in femaledict.iteritems():
	fp.write("female,"+key+','+str(len(femaledict[key])))
	fp.write("\n")
for key, value in unknowndict.iteritems():
	fp.write("unknown,"+key+','+str(len(unknowndict[key])))
	fp.write("\n")
fp.close()




