import os
import util
import numpy as np
import shutil
import stfio
from collections import Counter


def spread(avg, std, vals, j):
	return abs(vals[j] - avg) / std

def get_feature(avg, std, vals, i):
	return abs(spread(avg, std, vals, i) - (spread(avg, std, vals, i - 1) + spread(avg, std, vals, i + 1)) / 2)
	


def process_file(path, OUT):
	if path.endswith('.abf'):
		rec = stfio.read(path)
		for channel in rec:
			positive_candidates = list()
			negative_candidates = list()
			for section_num in range(len(channel)):
				section = channel[section_num]
				vals = section.asarray()
				mean = vals.mean()
				std = vals.std()
				pos_tups = []
				neg_tups = []
				for i in range(1, len(section)-1):
					tup = (i, section[i], get_feature(mean, std, vals, i))
					if section[i] > 0:
						pos_tups.append(tup)
					else:
						neg_tups.append(tup)
				pos_tups.sort(key=lambda x: x[2], reverse=True)
				neg_tups.sort(key=lambda x: x[2], reverse=True)
				if len(pos_tups) > 0 and len(neg_tups) > 0:
					positive_candidates.append(pos_tups[0][0])
					negative_candidates.append(neg_tups[0][0])
			if len(pos_tups) == 0 or len(neg_tups) == 0:
				print("file is weird")
				OUT.write("%s,%s,%s\n" % (path,"invalid","invalid"))
				continue
			data_pos = Counter(positive_candidates)
			pos_index = data_pos.most_common(1)[0]
			data_neg = Counter(negative_candidates)
			neg_index = data_neg.most_common(1)[0]
			
			print("file:", path)			
			print("positive:", pos_tups[0])
			print("negative:", neg_tups[0])
			OUT.write("%s,%s,%s\n" % (path, pos_index, neg_index))
		
				
					
		



			
def main():	
	THRESHOLD = 10000
	input_dir = './output/steps'
	OUT = open("./artifact_locations.csv", 'w')
	OUT.write("filename,pos_art_index,neg_art_index\n")
	for filename in os.listdir(input_dir):
		process_file(os.path.join(input_dir, filename), OUT)
			
	OUT.close()

				
				

					

	

			


if __name__ == "__main__":
	main()
