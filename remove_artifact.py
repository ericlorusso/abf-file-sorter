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
		section_max = np.asarray(channel)
		section_max = section_max[section_max.shape[0]-1:]
		Max = np.amin(section_max[np.amin(section_max):])
		argmax = np.argmin(section_max[np.amin(section_max):])
		sections_for_min = []
		for section in channel:
			sections_for_min.append(section.asarray()[:3700])
		matrix_for_min = np.asarray(sections_for_min)
		Min = np.amin(matrix_for_min)
		argmin = np.argmin(matrix_for_min)
			

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
