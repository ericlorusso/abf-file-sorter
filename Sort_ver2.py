import stfio
import numpy as np
import os
import util
import shutil

subdirs = {
	"c":"continuous",
	"rf":"repetitive_fire",
	"s":"steps",
	"ap":"action_potential",
	"u": "unknown"
}

target = "./output"

def classify_file(src, filename):
		
	if filename.endswith(".abf"):
		print("currently on file %s." % os.path.join(src, filename))
		rec = stfio.read(os.path.join(src,filename))
		array = np.asarray(rec)
		if rec[0].yunits == 'pA':
			shutil.copyfile(os.path.join(src, filename),os.path.join(target, subdirs["s"], filename))
		elif len(array[0]) > 1 and len(array[0][-1]) != len(array[0][-2]):
			shutil.copyfile(os.path.join(src, filename),os.path.join(target, subdirs["c"], filename))
		elif len(array[0][0]) >= 50000:
			shutil.copyfile(os.path.join(src, filename),os.path.join(target, subdirs["rf"], filename))
		elif len(array[0][0]) <= 50000:
			shutil.copyfile(os.path.join(src, filename),os.path.join(target, subdirs["ap"], filename))
		else:
			shutil.copyfile(os.path.join(src, filename),os.path.join(target, subdirs["u"], filename))	


def main():			
	src = "./input"
	util.resetDir(target)
	for key in subdirs.keys():
		os.mkdir(os.path.join(target, subdirs[key]))

	util.directory_walk(src, classify_file)

			


	
if __name__ == "__main__":
	main()

