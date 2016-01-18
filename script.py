from collections import defaultdict
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import time

def findAgeGroups(file_user, file_epoch):
	age_range = set()
	for line in open(file_user):
		words = line.strip().split(',')
		if words[1]!="age_range":
			age_range.add(words[1])
	print age_range


def epochConversion(file_song):
	fp = open("epoch.csv", 'w')
	for line in open(file_song):
		words = line.strip().split(',')
		if words[-2] != "end_timestamp":
			t = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(float(words[-2])))
			words.append(t.split(" ")[1])
			fp.write(','.join(words))
			fp.write("\n")
		else:
			words.append("actual_time")
			fp.write(','.join(words))
			fp.write("\n")
	fp.close()



def plotGraph(D):
	my_xticks = D.keys()
	plt.xticks(range(len(D)), my_xticks)
	plt.plot(range(len(D)), D.values())
	plt.show()


def plotMultipleGraphs(maleD, femaleD, unknownD):
	my_xticks = maleD.keys()
	plt.xticks(range(len(maleD)), my_xticks)

	plt.plot(range(len(maleD)), maleD.values(), color = 'r')
	red_patch = mpatches.Patch(color='red', label='male')

	plt.plot(range(len(femaleD)), femaleD.values(), color = 'g')
	green_patch = mpatches.Patch(color = 'g', label = 'female')

	plt.plot(range(len(unknownD)), unknownD.values(), color = 'b')
	blue_patch = mpatches.Patch(color = 'b', label = 'unknown')

	plt.legend(handles =[red_patch, green_patch, blue_patch])
	plt.show()


def countBasedStatisctics(file_song, file_user):
	set_male = set()
	set_female = set()
	set_unknown = set()

	for line in open(file_user):
		words = line.strip().split(',')
		if words[0] == 'male':
			set_male.add(words[-1])
		elif words[0] == 'female':
			set_female.add(words[-1])
		elif words[0] == 'unknown':
			set_unknown.add(words[-1])

	count_male = 0
	count_female = 0
	count_unknown = 0

	ms_male = 0
	ms_female = 0
	ms_unknown = 0

	context_dict = defaultdict(int)
	male_context = defaultdict(int)
	female_context = defaultdict(int)
	unknown_context = defaultdict(int)

	product_dict = defaultdict(int)
	male_product = defaultdict(int)
	female_product = defaultdict(int)
	unknown_product = defaultdict(int)

	for line in open(file_song):
		words = line.strip().split(',')
		if words[-1] in set_male:
			count_male += 1
			ms_male += int(words[0])
			male_context[words[1]] += 1
			male_product[words[3]] += 1

		elif words[-1] in set_female:
			count_female += 1
			ms_female += int(words[0])
			female_context[words[1]] += 1
			female_product[words[3]] += 1

		elif words[-1] in set_unknown:
			count_unknown += 1
			ms_unknown += int(words[0])
			unknown_context[words[1]] += 1
			unknown_product[words[3]] += 1

		if words[1] != "context":
			context_dict[words[1]] += 1
		if words[3] != "product":
			product_dict[words[3]] += 1
	print "\n\n"
	print "+++++++++++++++++++++++++++++++++++++++++++++"

	print "Male Listeners : ", count_male
	print "Female Listeners : ", count_female
	print "Unknown Listeners : ", count_unknown
	"""my_xticks = ["male", "female", "unknown"]
	plt.xticks([1,2,3], my_xticks)
	plt.bar([1,2,3], [count_male, count_female, count_unknown])
	plt.show()"""

	print "+++++++++++++++++++++++++++++++++++++++++++++"

	print "Male Time : ", ms_male
	print "Female Time : ", ms_female
	print "Unknown Time : ", ms_unknown
	"""my_xticks = ["male", "female", "unknown"]
	plt.xticks([1,2,3], my_xticks)
	plt.bar([1,2,3], [ms_male, ms_female, ms_unknown])
	plt.show()"""

	print "+++++++++++++++++++++++++++++++++++++++++++++"

	print "context dictionary:", context_dict
	#plotGraph(context_dict)
	print "male context: ", male_context
	print "female context: ", female_context
	print "unknown context: ", unknown_context
	#plotMultipleGraphs(male_context, female_context, unknown_context)

	print "+++++++++++++++++++++++++++++++++++++++++++++"

	print "product dictionary:", product_dict
	plotGraph(product_dict)
	print "male product: ", male_product
	print "female product: ", female_product
	print "unknown product: ", unknown_product
	#plotMultipleGraphs(male_product, female_product, unknown_product)
	print "+++++++++++++++++++++++++++++++++++++++++++++"
	print "\n\n"




if __name__=="__main__":
	countBasedStatisctics("end_song_sample.csv", "user_data_sample.csv")
	epochConversion("end_song_sample.csv")
	findAgeGroups("user_data_sample.csv", "epoch.csv")