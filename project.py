# return a list of every line from input file
def read_file(filename):
	contents = []
	try:
		file = open(filename, "r")

		for line in file:
			contents.append(line.rstrip("\n"))

		file.close()

	except:
		print("[Error] No such file or directory: " + filename) # error reading file

	return contents

src_code_lines = read_file("files/sample.in")
print(src_code_lines)