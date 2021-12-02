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
	numbr = r"-?[0-9]+"
	numbar = r"-?[0-9]+[\.][0-9]*"
	yarn = r"(?<=['\"]).*(?=['\"])"
	strdelimiter = r"['\"]"
	troof = r"(WIN|FAIL)"
	typeLiteral = r"(NUMBR|NUMBAR|YARN|TROOF|NOOB)"

	# keywords
	howizi = r"HOW[ ]+IZ[ ]+I"
	hai = r"HAI"
	kthxbye = r"KTHXBYE"
	ihasa = r"I[ ]+HAS[ ]+A"
	itz = r"ITZ"
	r = r"\bR\b"
	sumof = r"SUM[ ]+OF"
	diffof = r"DIFF[ ]+OF"
	produktof = r"PRODUKT[ ]+OF"
	quoshuntof = r"QUOSHUNT[ ]+OF"
	modof = r"MOD[ ]+OF"
	biggrof = r"BIGGR[ ]+OF"
	smallrof = r"SMALLR[ ]+OF"
	bothof = r"BOTH[ ]+OF"
	eitherof = r"EITHER[ ]+OF"
	wonof = r"WON[ ]+OF"
	notKey = r"NOT"
	anyof = r"ANY[ ]+OF"
	allof = r"ALL[ ]+OF"
	bothsaem = r"BOTH[ ]+SAEM"
	diffrint = r"DIFFRINT"
	smoosh = r"SMOOSH"
	maek = r"MAEK"
	isnowa = r"IS[ ]+NOW[ ]+A"
	visible = r"VISIBLE"
	gimmeh = r"GIMMEH"
	orly = r"O[ ]+RLY\?"
	yarly = r"YA[ ]+RLY"
	mebbe = r"MEBBE"
	nowai = r"NO[ ]+WAI"
	oic = r"OIC"
	wtf = r"WTF\?"
	omg = r"OMG"
	omgwtf = r"OMGWTF"
	iminyr = r"IM[ ]+IN[ ]+YR[ ]+"
	uppin = r"UPPIN"
	nerfin = r"NERFIN"
	yr = r"YR"
	til = r"TIL"
	wile = r"WILE"
	imouttayr = r"IM[ ]+OUTTA[ ]+YR"
	foundyr = r"FOUND[ ]+YR"
	ifusayso = r"IF[ ]+U[ ]+SAY[ ]+SO"
	gtfo = r"GTFO"
	mkay = r"MKAY"
	an = r"AN"
	a = r"\bA\b"
	iiz = r"I[ ]+IZ"

	# identifiers
	identifier = r"[a-zA-Z][a-zA-Z0-9_]*"


	regEx = [numbr, numbar, yarn, strdelimiter, troof, typeLiteral, howizi, hai, kthxbye, ihasa, itz, r, sumof, diffof, produktof, quoshuntof, modof, biggrof, smallrof, bothof, eitherof, wonof, notKey, anyof, allof, bothsaem, diffrint, smoosh, maek, a, isnowa, visible, gimmeh, orly, yarly, mebbe, nowai, oic, wtf, omg, omgwtf, iminyr, uppin, nerfin, yr, til, wile, imouttayr, foundyr, ifusayso, gtfo, mkay, an, identifier]

	# problem: both saem gets separated the second time. no clue why
	allTokens = []
	while True:
		for r in regEx:
			# search for the token in r
			token = re.search(r"^([ ]*"+r+r"[ ]*)", line)
			if token:
				# remove the match from the line and remove the spaces
				unspacedtoken = token.group().strip(r"^([ ]+)([ ]+)$")
				line = line.replace(token.group(), "")

				# append to allTokens
				allTokens.append(unspacedtoken)

				# end the loop pag nahanap na, proceed to find the next one so iloloop ulit yung regex
				break

		# check if line is wala na
		if re.match(r"^(\s*\n*)$", line):
			break

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