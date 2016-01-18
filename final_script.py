from collections import defaultdict
from datetime import datetime, timedelta
from scipy import spatial
import scipy.cluster.hierarchy as hac
import scipy.spatial.distance as ssd
import numpy as np
import time
import math


#############################################
#### Helper Functions for Report 1 ##########
#############################################
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

def getavgCount(mydict, n):
	mycount = 0
	avgcount = 0
	for key, value in mydict.iteritems():
		if value == 1:
			mycount += 1
		avgcount += value
	return float(mycount)/n, float(avgcount)/n

def getTrackStats(mydict):
	mytrack = defaultdict(float)
	for key, value in mydict.iteritems():
		keys = key.strip().split(" ")
		mytrack[keys[1]] += value
	for key,value in mytrack.iteritems():
		value = float(value)/len(mytrack)
	return mytrack


def Report1(songfile, userfile):
	maleid, femaleid, unknownid = genderID(userfile)
	total_tracks = set()

	listenrecordmale = defaultdict(int)
	listenrecordfemale = defaultdict(int)
	listenrecordunknown = defaultdict(int)
	
	for line in open(songfile):
		words = line.strip().split(',')
		total_tracks.add(words[2])
		if words[-1] in maleid and words[2] != "":
			listenrecordmale[words[-1]+" "+words[2]] += 1
		elif words[-1] in femaleid and words[2] != "":
			listenrecordfemale[words[-1]+" "+words[2]] += 1
		elif words[-1] in unknownid and words[2] != "":
			listenrecordunknown[words[-1]+" "+words[2]] += 1

	unique_male, gen_male = getavgCount(listenrecordmale, len(total_tracks))
	unique_female, gen_female = getavgCount(listenrecordfemale, len(total_tracks))
	unique_unknown, gen_unknown = getavgCount(listenrecordunknown, len(total_tracks))
	print "unique tracks (male/female/unknown): ",unique_male, unique_female, unique_unknown
	print "avg total tracks(male/female/unknown): ",gen_male, gen_female, gen_unknown


	malestats = getTrackStats(listenrecordmale)
	fp = open("./Report1-malestats.csv", 'w')
	fp.write("trackid,num-repeats")
	fp.write("\n")
	for key, value in malestats.iteritems():
		fp.write(key+","+str((value/len(maleid))*1000))
		fp.write("\n")
	fp.close()

	femalestats = getTrackStats(listenrecordfemale)
	fp = open("./Report1-femalestats.csv", 'w')
	fp.write("trackid,num-repeats")
	fp.write("\n")
	for key, value in femalestats.iteritems():
		fp.write(key+","+str((value/len(femaleid))*1000))
		fp.write("\n")
	fp.close()

	unknownstats = getTrackStats(listenrecordunknown)
	fp = open("./Report1-unknownstats.csv", 'w')
	fp.write("trackid,num-repeats")
	fp.write("\n")
	for key, value in unknownstats.iteritems():
		fp.write(key+","+str((value/len(unknownid))*1000))
		fp.write("\n")
	fp.close()
#############################################
#### Report - 1 Complete ####################
#############################################	


#############################################
#### Helper Functions for Report 2 ##########
#############################################

def convertEpoch(myFile):
	fp = open("end_song_sample_2.csv", 'w')
	for line in open(myFile):
		words = line.strip().split(",")
		if words[-2] != "end_timestamp":
			t = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(float(words[-2])))
			words.append(t)
			fp.write(','.join(words))
			fp.write("\n")
		else:
			words.append("actual_time")
			fp.write(','.join(words))
			fp.write("\n")
	fp.close()

def Report2(songfile, userfile):
	convertEpoch(songfile)

	maleid, femaleid, unknownid = genderID(userfile)
	dates = set()
	maledict = defaultdict(float)
	femaledict = defaultdict(float)
	unknowndict = defaultdict(float)

	for line in open("end_song_sample_2.csv"):
		words = line.strip().split(',')
		dates.add(words[-1].strip().split(" ")[0])

	for line in open("end_song_sample_2.csv"):
		words = line.strip().split(',')
		if words[-2] in maleid:
			maledict[words[-1].strip().split(" ")[0]] += (float(words[0])/1000.)
		elif words[-2] in femaleid:
			femaledict[words[-1].strip().split(" ")[0]] += (float(words[0])/1000.)
		elif words[-2] in unknownid:
			unknowndict[words[-1].strip().split(" ")[0]] += (float(words[0])/1000.)
	
	fp = open("./Report2-male_listen_perday_secs.csv", 'w')
	fp.write("day,avg_time_seconds")
	fp.write("\n")
	for key, value in maledict.iteritems():
		fp.write(key+","+str(value/len(maleid)))
		fp.write("\n")
	fp.close()

	fp = open("./Report2-female_listen_perday_secs.csv", 'w')
	fp.write("day,avg_time_seconds")
	fp.write("\n")
	for key, value in femaledict.iteritems():
		fp.write(key+","+str(value/len(femaleid)))
		fp.write("\n")
	fp.close()

	fp = open("./Report2-unknown_listen_perday_secs.csv", 'w')
	fp.write("day,avg_time_seconds")
	fp.write("\n")
	for key, value in unknowndict.iteritems():
		fp.write(key+","+str(value/len(unknownid)))
		fp.write("\n")
	fp.close()

#############################################
#### Report - 2 Complete ####################
#############################################	

#############################################
##################### Report 3 ##############
#############################################
def Report3(songfile, userfile):
	maleid, femaleid, unknownid = genderID(userfile)

	fp = open("./Report3-numsessions-male.csv",'w')
	fp.write("maleid,numsessions,avgsessionlength")
	fp.write("\n")
	for userid in maleid:
		mydatetime = []
		session = 1
		duration = 0.0
		for line in open(songfile):
			words = line.strip().split(',')
			if userid == words[-2]:
				fulldate = datetime.strptime(words[-1], '%Y-%m-%d %H:%M:%S')
				mydatetime.append(fulldate)
		mydatetime.sort()
		print mydatetime
		for i in xrange(len(mydatetime)-1):
			if(mydatetime[i+1]- mydatetime[i] < timedelta(minutes = 5)):
				duration += (mydatetime[i+1]- mydatetime[i]).total_seconds()
			else:
				session += 1
				
		fp.write(userid+','+str(session)+','+str(duration/session))
		fp.write("\n")
	fp.close()

	fp = open("./Report3-numsessions-female.csv",'w')
	fp.write("femaleid,numsessions,avgsessionlength")
	fp.write("\n")
	for userid in femaleid:
		mydatetime = []
		session = 1
		duration = 0.0
		for line in open(songfile):
			words = line.strip().split(',')
			if userid == words[-2]:
				fulldate = datetime.strptime(words[-1], '%Y-%m-%d %H:%M:%S')
				mydatetime.append(fulldate)
		mydatetime.sort()
		for i in xrange(len(mydatetime)-1):
			if(mydatetime[i+1]- mydatetime[i] < timedelta(minutes = 15)):
				duration += (mydatetime[i+1]- mydatetime[i]).total_seconds()
			else:
				session += 1
				
		fp.write(userid+','+str(session)+','+str(duration/session))
		fp.write("\n")
	fp.close()

	fp = open("./Report3-numsessions-unknown.csv",'w')
	fp.write("unknownid,numsessions,avgsessionlength")
	fp.write("\n")
	for userid in unknownid:
		mydatetime = []
		session = 1
		duration = 0.0
		for line in open(songfile):
			words = line.strip().split(',')
			if userid == words[-2]:
				fulldate = datetime.strptime(words[-1], '%Y-%m-%d %H:%M:%S')
				mydatetime.append(fulldate)
		mydatetime.sort()
		for i in xrange(len(mydatetime)-1):
			if(mydatetime[i+1]- mydatetime[i] < timedelta(minutes = 15)):
				duration += (mydatetime[i+1]- mydatetime[i]).total_seconds()
			else:
				session += 1
				
		fp.write(userid+','+str(session)+','+str(duration/session))
		fp.write("\n")
	fp.close()
	


#############################################
#### Report - 3 Complete ####################
#############################################


#############################################
##################### Report 4 ##############
#############################################	

"""
def Report4(userfile):

	maleid, femaleid, unknownid = genderID(userfile)
	
	fp = open("./Report4-file.csv", 'w')
	fp.write('userid,gender,age-group,session-number,session-length')
	fp.write("\n")

	maledict = defaultdict(str)
	femaledict = defaultdict(str)
	unknowndict = defaultdict(str)

	for line in open(userfile):
		words = line.strip().split(',')
		if words[0] == "gender":
			continue
		if words[0] == "male":
			maledict[words[-1]] = words[1]
		elif words[0] == "female":
			femaledict[words[-1]] = words[1]
		elif words[0] == "unknown":
			unknowndict[words[-1]] = words[1]

	for line in open("Report3-numsessions-male.csv"):
		words = line.strip().split(',')
		if words[0] == "maleid":
			continue		
		try:
			mystr = maledict[words[0]].strip().split(" - ")
			val = float(mystr[0]) + (float(mystr[1])-float(mystr[0]))/2
			fp.write(words[0]+',-1,'+str(val)+','+words[1]+','+words[2])
			fp.write("\n")
		except:
			mystr = maledict[words[0]].strip().split("+")
			fp.write(words[0]+',-1,'+str(mystr[0])+','+words[1]+','+words[2])
			fp.write("\n")


	for line in open("Report3-numsessions-female.csv"):
		words = line.strip().split(',')
		if words[0] == "femaleid":
			continue
		try:
			mystr = femaledict[words[0]].strip().split(" - ")
			val = float(mystr[0]) + (float(mystr[1])-float(mystr[0]))/2
			fp.write(words[0]+',-1,'+str(val)+','+words[1]+','+words[2])
			fp.write("\n")
		except:
			mystr = femaledict[words[0]].strip().split("+")
			fp.write(words[0]+',-1,'+str(mystr[0])+','+words[1]+','+words[2])
			fp.write("\n")

	for line in open("Report3-numsessions-unknown.csv"):
		words = line.strip().split(',')
		if words[0] == "unknownid":
			continue
		try:
			mystr = unknowndict[words[0]].strip().split(" - ")
			val = float(mystr[0]) + (float(mystr[1])-float(mystr[0]))/2
			fp.write(words[0]+',-1,'+str(val)+','+words[1]+','+words[2])
			fp.write("\n")
		except:
			mystr = unknowndict[words[0]].strip().split("+")
			fp.write(words[0]+',-1,'+str(mystr[0])+','+words[1]+','+words[2])
			fp.write("\n")
	fp.close()

	dist=[]
	wordlist=[]

	for line in open('Report4-file.csv'):
		items = line.strip().split(",")
		if items[0] == "userid":
			continue
		wordlist.append(items[1]+" "+items[2])
		numlist = items[3:]
		dist.append(numlist)


	cosdist = np.asarray(dist)
	#print cosdist
	a = ssd.pdist(cosdist, 'cosine')
	#print a
	a = np.clip(a,0,max(a))

	z = hac.linkage(a, 'average')
	#print z[:,2]
	#z = np.clip(z,0,max(z[:,2]))

	#fcluster thresholds z by 0.5 times
	#the max of the closest element
	arr = hac.fcluster(z, 0.5*max(z[:,2]), 'distance')
	#print arr
	uniquearr = set(arr)
	#print uniquearr


	for uniqueitem in uniquearr:
		print "%d"%(uniqueitem)
		for i in xrange(len(arr)):
			if arr[i]==uniqueitem:
				print wordlist[i]

	


#############################################
#### Report - 4 Complete ####################
#############################################
	"""
def main():
	#Report1("end_song_sample.csv", "user_data_sample.csv")
	#Report2("end_song_sample.csv", "user_data_sample.csv")
	Report3("end_song_sample_2.csv", "user_data_sample.csv")
	#Report4("user_data_sample.csv")

if __name__=="__main__":
	main()