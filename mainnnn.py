import os

# define the name of the directory to be created
path = "tmp/"

try:
	os.mkdir(path)
except OSError:
	print ("Creation of the directory %s failed" % path)
else:
	print ("Successfully created the directory %s " % path)