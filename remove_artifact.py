import os
import util
import numpy as np
import shutil
import stfio

THRESHOLD = 1900


def clean_artifacts(payload_dir, filename, OUT):
	if filename.endswith(".abf") == False:
		return
	if "step" not in payload_dir:
		return
	print("on file: %s" % os.path.join(payload_dir, filename))
	rec = stfio.read(os.path.join(payload_dir,filename))
	for channel in rec:
		for section in channel:
			section = section.asarray()
			thresh_crossed = False
			value_to_copy = None
			for k in range(len(section))[1:]:
				if thresh_crossed == False: 
					#iterating over single section. check for impulse spikes
					if abs((section[k] - section[k-1])) >= THRESHOLD:
						print("threshold crossed at k = %d", k)
						thresh_crossed = True
						value_to_copy = section[k-2]
						section[k] = value_to_copy
				else:
					#currently inside an artifact peak.
					if abs((section[k] - section[k-1])) >= THRESHOLD:
						print("exited threshold")
						# you've just crashed back to the normal values. Stop copying & reset flag
						thresh_crossed = False
						value_to_copy = None
					else:
						# you're still in the middle of an artifact peak
						print("still in theshold")
						section[k] = value_to_copy

	cleaned_vals = np.asarray(rec)
	Min = np.amin(cleaned_vals)
	Max = np.amax(cleaned_vals)
	argmax = np.argmax(cleaned_vals)
	argmin = np.argmin(cleaned_vals)
	output_line = [os.path.join(payload_dir, filename), len(rec[0][0]), argmin % len(rec[0][0])+1, Min, argmax % len(rec[0][0])+1, Max]
	output_line = [str(x) for x in output_line]
	OUT.write(",".join(output_line))
	OUT.write('\n')
	

			


if __name__ == "__main__":
	input_dir = "./output"
	output_dir = "./output_min_max"
	util.resetDir(output_dir)
	aggregate_list = ["filepath", "interval length", "argmin", "min", "argmax", "max"]
	OUT = open(os.path.join(output_dir, "min_max_stuff.csv"), "a")
	OUT.write(",".join(aggregate_list))
	OUT.write("\n")
	util.directory_walk(input_dir, clean_artifacts, OUT)
	OUT.close()
