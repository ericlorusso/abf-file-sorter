import os
import util
import numpy as np
import shutil
import stfio


def main():	
	THRESHOLD = 10000
	for filename in os.listdir('//home//eric//Desktop//Directory_Walking_Sort'):
		if filename.endswith('.abf'):
			rec = stfio.read(filename)
			trace_channel = np.asarray(rec[0])
			mean = trace_channel.mean(0)		
			max_check = max(mean)
			min_check = min(mean)
			final_trace = []
			error_trace = []
			print(max_check, min_check)
			for section in trace_channel:
				for k in range(len(trace_channel[0])):
					if mean[k] == max_check:					
						if abs((mean[k-1]-mean[k])/0.05)>=THRESHOLD:
							error_trace.append(section[k])
					elif mean[k] == min_check:
						if abs((mean[k-1]-mean[k])/0.05)>=THRESHOLD:
							error_trace.append(section[k])
					else:
						final_trace.append(section[k])
			MAX = max(final_trace)
			MIN = min(final_trace)
			print(MAX, MIN)
			print(error_trace)
			
			


				
				

					

	

			


if __name__ == "__main__":
	main()
