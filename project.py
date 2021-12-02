import re

# notes and bugs
# need a way to throw error if theres no match
# function name gets separated bc it has spaces (sa sample)

# return a list of every line from input file
def read_file(filename):
	try:
		file = open(filename, "r")

		# open and tokenize file
		data = file.read()

		# need na basahin yung whole file tas tsaka itokenize kasi nakakaloka iignore yung multiline comments pag sineparate kaagad

		file.close()

	except:
		print("[Error] No such file or directory: " + filename) # error reading file

	return data

def findMatch(line):
	# lagay yung mga regex here

	# literals
	numbr = "-?[0-9]+"
	numbar = "-?[0-9]+[\\.][0-9]*"
	yarn = "(?<=['\"]).*(?=['\"])"
	strdelimiter = "['\"]"
	troof = "(WIN|FAIL)"
	typeLiteral = "(NUMBR|NUMBAR|YARN|TROOF|NOOB)"

	# keywords
	howizi = "HOW[ ]+IZ[ ]+I"
	hai = "HAI"
	kthxbye = "KTHXBYE"
	ihasa = "I[ ]+HAS[ ]+A"
	itz = "ITZ"
	r = "\bR\b"
	sumof = "SUM[ ]+OF"
	diffof = "DIFF[ ]+OF"
	produktof = "PRODUKT[ ]+OF"
	quoshuntof = "QUOSHUNT[ ]+OF"
	modof = "MOD[ ]+OF"
	biggrof = "BIGGR[ ]+OF"
	smallrof = "SMALLR[ ]+OF"
	bothof = "BOTH[ ]+OF"
	eitherof = "EITHER[ ]+OF"
	wonof = "WON[ ]+OF"
	notKey = "NOT"
	anyof = "ANY[ ]+OF"
	allof = "ALL[ ]+OF"
	bothsaem = "BOTH[ ]+SAEM"
	diffrint = "DIFFRINT"
	smoosh = "SMOOSH"
	maek = "MAEK"
	a = "\bA\b"
	isnowa = "IS[ ]+NOW[ ]+A"
	visible = "VISIBLE"
	gimmeh = "GIMMEH"
	orly = "O[ ]+RLY\\?"
	yarly = "YA[ ]+RLY"
	mebbe = "MEBBE"
	nowai = "NO[ ]+WAI"
	oic = "OIC"
	wtf = "WTF\\?"
	omg = "\bOMG\b"
	omgwtf = "OMGWTF"
	iminyr = "IM[ ]+IN[ ]+YR[ ]+"
	uppin = "UPPIN"
	nerfin = "NERFIN"
	yr = "\bYR\b"
	til = "TIL"
	wile = "WILE"
	imouttayr = "IM[ ]+OUTTA[ ]+YR"
	foundyr = "FOUND[ ]+YR"
	ifusayso = "IF[ ]+U[ ]+SAY[ ]+SO"
	gtfo = "GTFO"
	mkay = "MKAY"
	an = "AN"
	iiz = "I[ ]+IZ"

	# identifiers
	identifier = "[a-zA-Z][a-zA-Z0-9_]*"


	regEx = [numbr, numbar, yarn, strdelimiter, troof, typeLiteral, howizi, hai, kthxbye, ihasa, itz, r, sumof, diffof, produktof, quoshuntof, modof, biggrof, smallrof, bothof, eitherof, wonof, notKey, anyof, allof, bothsaem, diffrint, smoosh, maek, a, isnowa, visible, gimmeh, orly, yarly, mebbe, nowai, oic, wtf, omg, omgwtf, iminyr, uppin, nerfin, yr, til, wile, imouttayr, foundyr, ifusayso, gtfo, mkay, an, identifier]

	allTokens = []
	for r in regEx:
		# search for the token in r
		token = re.search("^([ ]*"+r+"[ ]*)", line)
		if token:
			# remove the match from the line
			unspacedtoken = re.sub("^([ ]+)([ ]+)$", "", token.group())
			line = re.sub(token.group(), "", line)
			allTokens.append(unspacedtoken)

	return allTokens

def tokenize(code):
	# NOTE
		# throw error if may OBTW or TLDR na nasa same line as other statements?
		# implement this sa checking syntax siguro, for now tokenizing
			# we check if there's an OBTW and TLDR in there maybe? tas throw error if meron
			# this does not match lines na may OBTW na kasama with other lines

	# remove multiline comments
	code = re.sub("(OBTW).*?(TLDR\n)", "", code, flags=re.DOTALL)
	# remove single line comments
	code = re.sub("(.)*BTW(.)*(\n)*", "", code)

	# tokenize
	# assuming na di required ang newline sa YARN

	# separate every line
	lines = code.split("\n")

	tokens = []
	# iterate through every line
	for line in lines:
		#literal = re.search("(?<=['\"]).*?(?=['\"])", line)
		#yarn = ""

		# if there's a string literal:
		#if literal:
			# remove the string literal and replace them with a space
		#	newline = re.sub("(?<=['\"]).*?(?=['\"])", " ", line)
		#	yarn = literal.group()

		# separate everything, ignore all spaces
		# check keywords by:
		# creating regex just as a string
		# putthing them in a list
		# iterate through the list
		# if there is a match, we append the match to the list of tokens

		# we look for matches and put them in the list token
		token = findMatch(line)


		# iterate through every token for this line and append them to the final tokens list
		for t in token:
			# add to dictionary? IDK
			tokens.append(t)


		#separated = line.split()
		#print(separated)

		# add each element of separated to tokens
		#for e in separated:
			# this will add the string literal in between the ""
		#	if e=="\"" and yarn!="":
		#		tokens.append(e)
		#		tokens.append(yarn)
		#		yarn = ""

		#	tokens.append(e)

	print(tokens)


src_code_lines = read_file("files/sample.lol")
tokenize(src_code_lines)