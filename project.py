from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
import tkinter.scrolledtext as scrolledtext
import re

# notes and bugs
# need a way to throw error if theres no match
# function name gets separated bc it has spaces (sa sample)

##### PROCESS #####
# open file -> print file to text editor -> click execute (run) -> remove comments -> remove whitespaces -> tokenize (update global variable tokens then get the classification of each token)
# fill lexemes table (lexical analyzer)

##### GLOBAL VARIABLES #####
tokens = []
line_number = 0
symbols = {"IT": "NOOB"}
# for loops
is_break = False 
in_loop = []

##### FUNCTIONS #####
def select_file():
	file_path = fd.askopenfilename(title="Open a LOLCODE file..", filetypes=(("lol files", ".lol"),)) # open a file dialog that shows .lol files only
	if len(file_path) == 0: return # no file selected

	file_contents = read_file(file_path) # get the file contents
	show_file_contents(file_contents) # show file contents to GUI

def read_file(filename):

	file = open(filename, "r")

	contents = file.read() 
	
	file.close()

	return contents

def show_file_contents(contents):
	text_editor.delete(1.0, END) # make sure text editor is clear
	text_editor.insert(1.0, contents) # print contents to GUI

def run():
	# reset variables
	global tokens, line_number, symbols, is_break, in_loop
	tokens = []
	line_number = 0
	symbols = {"IT": "NOOB"}
	is_break = False 
	in_loop = []
	console["state"] = "normal"
	console.delete(1.0, END)
	console["state"] = "disabled"

	code = text_editor.get(1.0,'end-1c') # get the input from Text widget
	if code.strip()=='': return # no input

	code = remove_comments(code)
	code = code.split("\n")
	code = remove_whitespaces(code)
	
	tokenize(code)
	has_lexical_errors = console.get(1.0,'end-1c') # get the input from Text widget
	
	if has_lexical_errors: return # has unknown keywords

	tokens = remove_comment_delims()
	syntax_analyzer()

def remove_comments(src_code):
	# remove multiline comments
	src_code = re.sub(r"(^|\n)( |\t)*OBTW\s*(\s+((?!TLDR).)*)*\n( |\t)*TLDR( |\t)*(?=(\n|$))", r"\nOBTW\nTLDR", src_code) 
	
	# remove single line comments
	src_code = re.sub(r"(^|\s)BTW( |\t)*(( |\t)+.*)?(?=(\n|$))", "\nBTW", src_code)

	return src_code

def remove_whitespaces(src_code):
	temp = []

	for line in src_code:
		line = line.strip() # remove leading and trailing whitespaces
		if line != "":
			temp.append(line) # append line only if it is not an empty string

	return temp

def findMatch(line):
	#Literal(0-4)
	yarn = r"(\")([^\"]*)(\")"
	numbr = r"-?[0-9]+"
	numbar = r"-?[0-9]+[\.][0-9]*"
	troof = r"(WIN|FAIL)"
	typeLiteral = r"(NUMBR|NUMBAR|YARN|TROOF|NOOB)"

	#String Delimiter(5)
	strdelimiter = r"['\"]"
	#Code Delimiter(6-7)
	hai = r"HAI"
	kthxbye = r"KTHXBYE"

	#Variable Declaration(8)
	ihasa = r"I[ |\t]+HAS[ |\t]+A"

	#Variable Assignment(9)
	itz = r"ITZ"

	#Output Keyword(10)
	visible = r"VISIBLE"

	#Input Keyword(11)
	gimmeh = r"GIMMEH"

	#Assignment Keywords(12)
	r = r"\bR\b"
	
	#Flow Control Keywords(13-27)
	#If-Else Keywords
	yarly = r"YA[ |\t]+RLY"
	nowai = r"NO[ |\t]+WAI"
	orly = r"O[ |\t]+RLY\?"
	
	#Switch-Case Keywords
	omg = r"OMG"
	omgwtf = r"OMGWTF"
	oic = r"OIC"
	wtf = r"WTF\?"

	#Loop Keywords
	uppin = r"UPPIN"
	nerfin = r"NERFIN"
	til = r"TIL"
	wile = r"WILE"
	imouttayr = r"IM[ |\t]+OUTTA[ |\t]+YR"
	yr = r"YR"
	iminyr = r"IM[ |\t]+IN[ |\t]+YR"
	mebbe = r"MEBBE"

	#Concatenation Keywords(28-29)
	smoosh = r"SMOOSH"
	mkay = r"MKAY"
	
	#Connector Keywords(30-31)
	an = r"AN"
	a = r"\bA\b"

	#Comparison Keywords(32-33)
	bothsaem = r"BOTH[ |\t]+SAEM"
	diffrint = r"DIFFRINT"
	
	#Boolean Keywords(34-39)
	bothof = r"BOTH[ |\t]+OF"
	eitherof = r"EITHER[ |\t]+OF"
	wonof = r"WON[ |\t]+OF"
	notKey = r"NOT"
	anyof = r"ANY[ |\t]+OF"
	allof = r"ALL[ |\t]+OF"
	
	#Arithmetic Keywords(40-46)
	sumof = r"SUM[ |\t]+OF"
	diffof = r"DIFF[ |\t]+OF"
	produktof = r"PRODUKT[ |\t]+OF"
	quoshuntof = r"QUOSHUNT[ |\t]+OF"
	modof = r"MOD[ |\t]+OF"
	biggrof = r"BIGGR[ |\t]+OF"
	smallrof = r"SMALLR[ |\t]+OF"

	#Comment Delimiter(47-49)
	btw = r"BTW"
	obtw = r"OBTW"
	tldr = r"TLDR"

	#Casting Keywords(50-51)
	maek = r"MAEK"
	isnowa = r"IS[ |\t]+NOW[ |\t]+A"

	#Return Keywords(52-53)
	foundyr = r"FOUND[ |\t]+YR"
	gtfo = r"GTFO"

	#Calling Keyword(54)
	iiz = r"I[ |\t]+IZ"

	#Function Delimiter(55-56)
	howizi = r"HOW[ |\t]+IZ[ |\t]+I"
	ifusayso = r"IF[ |\t]+U[ |\t]+SAY[ |\t]+SO"

	#Variable Identifier(57)
	identifier = r"[a-zA-Z][a-zA-Z0-9_]*"

	#Unknown Keyword (58)
	unknown = r".*?"

	regEx = [yarn, numbr, numbar, troof, typeLiteral,
		strdelimiter, hai, kthxbye, ihasa, itz, visible, gimmeh,
		r, yarly, nowai, orly, omg, omgwtf, oic, wtf, uppin,
		nerfin, til, wile, imouttayr, yr, iminyr, mebbe,
		smoosh, mkay, an, a, bothsaem, diffrint, bothof, eitherof, wonof, notKey, anyof, allof,
		sumof, diffof, produktof, quoshuntof, modof, biggrof, smallrof,
		btw, obtw, tldr, maek, isnowa, foundyr, gtfo, iiz, howizi, ifusayso,
		identifier, unknown]

	allTokens = []
	classify = []

	while line: # we search for tokens until line is empty
		for index, r in enumerate(regEx):
			# search for the current r in the line. searches the FRONT of the line.
			token_regex = r"^"+r+r"(\s+|$)"
			token = re.search(token_regex, line)

			if token:
				# remove the match from the line and remove the spaces
				unspacedtoken = token.group().strip()
				line = re.sub(token_regex, "", line)

				# append to allTokens
				allTokens.append(unspacedtoken)

				#classify token
				if index == 0:
					o_delim = token.group(1) # string delimiter
					string = token.group(2) # actual yarn
					c_delim = token.group(3) # string delimiter
					
					allTokens[-1] = o_delim
					allTokens.append(string)
					allTokens.append(c_delim)

					classify.append("String Delimiter")
					classify.append("Literal")
					classify.append("String Delimiter")
				elif index in range(1,5):
					classify.append("Literal")
				# elif index == 5: // check if this is still necessary before deleting
				# 	classify.append("String Delimiter")
				elif index in range(6,8):
					classify.append("Code Delimiter")
				elif index == 8:
					classify.append("Variable Declaration")
				elif index == 9:
					classify.append("Variable Assignment")
				elif index == 10:
					classify.append("Output Keyword")
				elif index == 11:
					classify.append("Input Keyword")
				elif index == 12:
					classify.append("Assignment Keyword")
				elif index in range(13,28):
					classify.append("Flow Control Keyword")
				elif index in range(28,30):
					classify.append("Concatenation Keyword")
				elif index in range(30,32):
					classify.append("Connector Keyword")
				elif index in range(32,34):
					classify.append("Comparison Keyword")
				elif index in range(34,40):
					classify.append("Boolean Keyword")
				elif index in range(40,47):
					classify.append("Arithmetic Keyword")
				elif index in range(47,50):
					classify.append("Comment Delimiter")
				elif index in range(50,52):
					classify.append("Casting Keyword")
				elif index in range(52,54):
					classify.append("Return Keyword")
				elif index == 54:
					classify.append("Calling Keyword")
				elif index in range(55,57):
					classify.append("Function Delimiter")
				elif index == 57:
					classify.append("Variable Identifier")
				else:
					output_console("error::unknown keyword: " + unspacedtoken)
					classify.append("Unknown Keyword")

				# end the loop pag nahanap na, proceed to find the next one so iloloop ulit yung regex
				break

	return allTokens, classify

def tokenize(code):
	global tokens

	tokens = []
	classifications = []

	for line in code: # iterate through every line
		token, classify = findMatch(line) # get the tokens and their class of each line
		tokens.append(token)
		classifications.append(classify)

	fill_table(lexemes_table, tokens, classifications) # fill the lexemes table in the GUI

def fill_table(tree, lhs, rhs):
	# make sure table is clear
	for element in tree.get_children():
		tree.delete(element)

	count = 0

	for i in range(len(lhs)): # per line
		for j in range(len(lhs[i])): # per token
			lhs_value = lhs[i][j]
			rhs_value = rhs[i][j]

			tree.insert(parent='', index=END, text=count, values=(lhs_value, rhs_value)) # print to GUI
			count += 1

##### SYNTAX ANALYZER #####

def find_line(needed_token, start, end):
	max_length = len(tokens)
	if start < max_length and end <= max_length:
		for i in range(start, end):
			if tokens[i][0]==needed_token: # found the line where token is found
				return i
	return -1

def get_line(index):
	string = ''

	if index >= len(tokens): # out of bounds
		return "KTHXBYE"

	for word in tokens[index]: # get the whole line as string at line index
		string += word + ' '

	return string.strip() 

def remove_comment_delims():
	global tokens
	length = len(tokens)
	new_tokens = []

	for i in range(length):
		string = get_line(i)
		if string=="BTW": # single line comment
			continue
		elif string=="OBTW" and get_line(i+1)=="TLDR": # opening multi line comment
			continue
		elif string=="TLDR" and i-1 >= 0: # closing multi line comment TLDR
			if get_line(i-1)=="OBTW":
				continue
		new_tokens.append(tokens[i])

	return new_tokens

def output_console(contents):
	console["state"] = "normal"
	console.insert(END, contents) # print contents to GUI
	console.insert(END, "\n") # print contents to GUI
	console["state"] = "disabled"

def syntax_analyzer():
	global tokens

	if get_line(0)=="HAI": # check if program starts with HAI only
		i = find_line("KTHXBYE", 0, len(tokens)) # check if there is KTHXBYE
		
		if i > -1:
			tokens = tokens[:i] # exclude everything after the [first] KTHXBYE
			tokens.pop(0) # exclude everything before the [first] HAI
			if tokens and parse_comments(): # check for comment errors
				while line_number < len(tokens): # check the rest of the code
					if not statement(False):
						break 
		else:
			output_console("error at: " + get_line(i)) # program has no KTHXBYE
	else: # program does not start with HAI
		output_console("error at: " + get_line(line_number))

def parse_comments():
	for i in range(len(tokens)):
		line = tokens[i]
		if ("OBTW" in line) or ("TLDR" in line): # comment error found
			output_console("error at: " + get_line(i))
			return False

	return True # no errors in comments

def get_current_token(index):
	current_line = tokens[line_number]

	if index >= len(current_line):
		return None
	else:
		return current_line[index]

def check_token(needed_token, index):
	global line_number

	current_token = get_current_token(index)

	if not current_token: # reached the EOL
		line_number += 1 
		return 0
	elif current_token==needed_token: # correct syntax
		return index+1
	else:
		return -1 # wrong syntax

def statement(is_code_block):
	# THIS IS WHERE THE ACTUAL START OF ANALYZING THE STATEMENTS
	global line_number
	token = get_current_token(0)

	# VARIABLE DECLARATION
	if token=="I HAS A" and not is_code_block:
		print("I HAS A")

	# ARITHMETIC OPERATIONS
	elif token=="SUM OF":
		print("SUM OF")
	elif token=="DIFF OF":
		print("DIFF OF")
	elif token=="PRODUKT OF":
		print("PRODUKT OF")
	elif token=="QUOSHUNT OF":
		print("QUOSHUNT OF")
	elif token=="MOD OF":
		print("MOD OF")
	elif token=="BIGGR OF":
		print("BIGGR OF")
	elif token=="SMALLR OF":
		print("SMALLR OF")

	# BOOLEAN OPERATIONS
	elif token=="BOTH OF":
		print("BOTH OF")
	elif token=="EITHER OF":
		print("EITHER OF")
	elif token=="WON OF":
		print("WON OF")
	elif token=="NOT":
		print("NOT")
	elif token=="ALL OF":
		print("ALL OF")
	elif token=="ANY OF":
		print("ANY OF")

	# COMPARISON OPERATIONS
	elif token=="BOTH SAEM":
		print("BOTH SAEM")
	elif token=="DIFFRINT":
		print("DIFFRINT")

	# CONCATENTATION
	elif token=="SMOOSH":
		print("SMOOSH")

	# TYPECAST
	elif token=="MAEK":
		if typecast(tokens[line_number], "IT"):
			line_number += 1
			return True

	# INPUT/OUTPUT
	elif token=="VISIBLE":
		print("VISIBLE")
	elif token=="GIMMEH":
		print("GIMMEH")

	# IF-THEN
	elif token=="O RLY?":
		return if_then()

	# SWITCH CASE
	elif token=="WTF?":
		return switch_case()

	# LOOP
	elif token=="IM IN YR":
		return loop()
		# print("IM IN YR")

	#### FUNCTIONS FUNCTIONS FUNCTIONS FUNCTIONS FUNCTIONS FUNCTIONS FUNCTIONS 
	#### FUNCTIONS FUNCTIONS FUNCTIONS FUNCTIONS FUNCTIONS FUNCTIONS FUNCTIONS 
	#### FUNCTIONS FUNCTIONS FUNCTIONS FUNCTIONS FUNCTIONS FUNCTIONS FUNCTIONS 
	
	# MISUSED KEYWORDS
	elif token=="GTFO" and is_code_block and in_loop:
		global is_break
		is_break = True
		line_number += 1
		return True

	elif token=="GTFO" or token=="ITZ" or token=="R" or token=="YA RLY" or token=="NO WAI" or token=="O RLY?" or token=="OMG" or token=="OMGWTF" or token=="OIC" or token=="UPPIN" or token=="NERFIN" or token=="TIL" or token=="WILE" or token=="IM OUTTA YR" or token=="YR" or token=="MEBBE" or token=="MKAY" or token=="AN" or token=="A" or token=="IS NOW A":
		output_console("error at: " + get_line(line_number))
		return False
	
	else:
		regex = r"[a-zA-Z][a-zA-Z0-9_]*$"
		
		if re.search(regex, token): # [RE]ASSIGNMENTS
			print("IDENTIFIER")
		else: # UNKNOWN PATTERN
			output_console("error at: " + get_line(line_number))
			return False

	line_number += 1
	return True

def is_numeric(token):
	return token.replace('.','',1).replace('-','',1).isdigit()

def loop_expr(token_list):
	# call expression
	return True

def cast(variable, needed_type):
	# NOOB, "", 0 -> FAIL
	# OTHERS -> WIN
	# WIN -> NUMBR, NUMBAR (1[.0])
	# FAIL -> NUMBR, NUMBAR (0[.0])
	# NUMBR <-> NUMBAR
	# NUMBR, NUMBAR(2 DECIMAL) <-> YARN
	if needed_type=="NOOB":
		return "NOOB"

	elif needed_type=="TROOF":
		if variable in ["WIN", "FAIL"]:
			return variable
		elif variable in ["NOOB", '', 0]:
			return "FAIL"
		else:
			return "WIN"
	
	elif needed_type=="YARN":
		if type(variable)==str:
			return variable
		elif type(variable)==int or type(variable)==float:
			return str(variable)
	
	elif needed_type=="NUMBR":
		if type(variable)==int:
			return variable
		elif type(variable)==float:
			return int(variable)
		elif variable=="WIN":
			return 1
		elif variable=="FAIL":
			return 0
		elif is_numeric(variable):
			return int(eval(variable))

	elif needed_type=="NUMBAR":
		if type(variable)==float:
			return variable
		elif type(variable)==int:
			return float(variable)
		elif variable=="WIN":
			return 1.0
		elif variable=="FAIL":
			return 0.0
		elif is_numeric(variable):
			return float(eval(variable))

	return False

def typecast(token_list, dest):
	valid_types = ['TROOF', 'YARN', 'NUMBR', 'NUMBAR', 'NOOB']
	type_result = line[-1]

	# check if type is valid
	if type_result not in valid_types:
		output_console("error::type must be TROOF, YARN, NUMBR, NUMBAR, or NOOB at: " + get_line(line_number))
		return False

	# check if has A
	has_a = "A" in line
	expr_end = -2 if has_a else -1
	expr_result = loop_expr(token_list[1:expr_end])
	value = ''

	if expr_result: # expression
		value = 'IT' 
	elif src in symbols.keys(): # variable
		value = line[1]
	else:
		output_console("error::in expression or variable at: " + get_line(line_number))
		return False
	
	value = symbols[value]
	result = cast(value, type_result) # typecast

	if result==False: # typecast failed
		output_console("error::cannot be typecasted at: " + get_line(line_number))
		return False	

	symbols[dest] = result # store the result to dest
	return True

def find_end_block(needed_token, incrementor, start, end):
	max_length = len(tokens)
	if start >= max_length and end > max_length:
		return -1

	count = 1
	for i in range(start, end):
		token = tokens[i][0]

		if token==needed_token:
			count -= 1
		elif token in incrementor:
			count += 1

		if count==0: # found the pair/end of block code
			return i
	return -1

def find_keyword(needed_token, start, end):
	while start < end:
		token = tokens[start][0]
		if token=="O RLY?" or token=="WTF?": # skip if-else and switch-case
			start = find_end_block("OIC", ["O RLY?", "WTF?"], start+1, end)
			if start < 0:
				return -1 
		elif token=="IM IN YR": # skip loops
			start = find_end_block("IM OUTTA YR", ["IM IN YR"], start+1, end)
			if start < 0:
				return -1
		elif token==needed_token:
			return start
		start += 1
	return -2 # no keyword found

def validate_blocks(start, end): # checks if blocks are valid and non-empty
	#IM IN YR
	#YA RLY, NO WAI, OMG, OMGWTF, GTFO, OIC, IM OUTTA YR
	invalid = ["YA RLY", "NO WAI", "OMG", "OMGWTF", "OIC", "IM OUTTA YR"]

	for i in range(start, end):
		next_statement = tokens[i+1][0]
		line = tokens[i]
		token = line[0]
		if token=="OMG": # check if valid OMG
			length = len(line)
			if length == 2:
				literal = line[1]
				if is_numeric(literal) or literal in ["WIN", "FAIL"]: 
					pass
			elif length == 4:
				if line[1]=='"':
					pass
			else:
				return [False, i]
			if next_statement in invalid:
				return [False, i+1]
		elif token=="IM IN YR": # check if valid loop
			if len(line) > 7:
				regex = re.compile(r"^[a-zA-Z][a-zA-Z0-9_]*$")
				if (not regex.search(line[1])) or (line[2] not in ["UPPIN", "NERFIN"]) or (line[3]!="YR") or (line[4] not in symbols.keys()) or (line[5] not in ["TIL", "WILE"]) or (not loop_expr(line[6:])): 
					return [False, i]
			else:
				return [False, i]
			if next_statement in invalid:
				return [False, i+1]
		elif token=="IM OUTTA YR":
			if len(line) != 2:
				output_console("error at: " + get_line(i))
				return False

			# label
			label_regex = re.compile(r"^[a-zA-Z][a-zA-Z0-9_]*$")
			try:
				label_regex.search(line[1]).group()
			except:
				output_console("error at: " + get_line(i))
				return False
		elif token=="OIC":
			if get_line(i) != token:
				return [False, i]
		elif token in invalid:
			if get_line(i) != token:
				return [False, i]
			if next_statement in invalid:
				return [False, i+1]

	return [True, end]

def if_then():
	# MEBBE MEBBE MEBBE MEBBE MEBBE MEBBE MEBBE
	# MEBBE MEBBE MEBBE MEBBE MEBBE MEBBE MEBBE
	# MEBBE MEBBE MEBBE MEBBE MEBBE MEBBE MEBBE

	global line_number, tokens

	# O RLY?
	if get_line(line_number)=="O RLY?": 
		line_number += 1
	else:
		output_console("error::expected O RLY? at: " + get_line(line_number)) # NO O RLY? FOUND
		return False

	# YA RLY
	index_ya_rly = find_line("YA RLY", line_number, line_number+1)
	has_ya_rly = index_ya_rly > -1 

	if has_ya_rly:
		line_number += 1
	else:
		output_console("error::expected YA RLY at: " + get_line(line_number)) # NO YA RLY FOUND
		return False

	# OIC
	index_oic = find_end_block("OIC", ["O RLY?", "WTF?"], line_number, len(tokens))
	has_oic = index_oic > -1 and get_line(index_oic)=="OIC"

	if has_oic:
		# NO WAI
		index_no_wai = find_keyword("NO WAI", line_number, index_oic)
		has_no_wai = index_no_wai > -1 and get_line(index_no_wai)=="NO WAI"

		# verify all blocks found inside (even in nested if then)
		is_valid = validate_blocks(index_ya_rly, index_oic)

		if not is_valid[0]:
			output_console("error at: " + get_line(is_valid[1]))
			return False

		# check the value of IT
		it = symbols["IT"]
		fail = ['', 0, "NOOB"]

		if it in fail: # FALSE
			if has_no_wai: # has NO WAI clause
				line_number = index_no_wai+1
			else: # no NO WAI clause
				line_number = index_oic+1
				return True
		elif has_no_wai: # TRUE
			del tokens[index_no_wai:index_oic] # delete the NO WAI part
			index_oic -= (index_oic - index_no_wai)

		while line_number < index_oic:
			if not statement(True):
				return False

		line_number = index_oic+1
		return True

	else:
		output_console("error::expected OIC") # NO OIC FOUND
		return False

def switch_case():
	global line_number, tokens

	# WTF?
	if get_line(line_number)=="WTF?": 
		line_number += 1
	else:
		output_console("error at: " + get_line(line_number)) # NO O RLY? FOUND
		return False

	# OIC
	index_oic = find_end_block("OIC", ["O RLY?", "WTF?"], line_number, len(tokens))
	has_oic = index_oic > -1 and get_line(index_oic)=="OIC"

	if has_oic:
		# check if WTF? OIC has contents
		if index_oic-line_number==0:
			output_console("error at: " + get_line(line_number))
			return False

		# OMG
		index_omg = find_line("OMG", line_number, line_number+1)
		has_omg = index_omg > -1

		# OMGWTF
		index_omgwtf = find_keyword("OMGWTF", line_number, index_oic)
		has_omgwtf = index_omgwtf > -1 and get_line(index_omgwtf)=="OMGWTF"

		# flag
		matched = False
		# cases
		cases = []

		if has_omg: 
			# find the indices of the cases that are connected to the current block of switch case only
			cases =[index_omg]

			index_omg += 1
			while index_omg < index_oic:
				index_omg = find_keyword("OMG", index_omg, index_oic)
				if index_omg == -1: # error within nested block
					output_console("error at: " + get_line(index_oic))
					return False
				elif index_omg == -2: # no [more] OMG
					break
				cases.append(index_omg)
				index_omg += 1

			# verify all blocks found inside (even in nested switch cases)
			is_valid = validate_blocks(cases[0], index_oic)

			if not is_valid[0]:
				output_console("error at: " + get_line(is_valid[1]))
				return False

			# check the value of IT
			it = symbols["IT"]
			if it=="NOOB":
				it = "FAIL"
			
			# find where it matches
			for case in cases:
				token = tokens[case][1]
				if token=='"': # string
					token = tokens[case][2]
				elif is_numeric(token): # numbr/numbar
					token = eval(token)
				if token==it:
					line_number = case+1
					matched = True
					break

		else: # if no OMG, there must be OMGWTF
			if index_omgwtf != line_number and index_oic-index_omgwtf==1:
				output_console("error::expected OMG or OMGWTF at: " + get_line(line_number))
				return False

		if not matched:
			if not has_omgwtf: # no match, no default case
				line_number = index_oic+1
				return True
			else:
				line_number = index_omgwtf+1 

		# GTFO
		index_gtfo = find_keyword("GTFO", line_number, index_oic)
		has_gtfo = index_gtfo > -1 and get_line(index_gtfo)=="GTFO"

		end = index_oic

		if has_gtfo:
			end = index_gtfo

		# remove the OMGWTF statement between matched case until end if there are any
		if index_omgwtf in range(line_number, end):
			tokens.pop(index_omgwtf)
			end -= 1
			index_oic -= 1

		# remove OMG statements between matched case until end if there are any
		count = 0
		for case in cases:
			if case in range(line_number, end):
				tokens.pop(case-count)
				end -= 1
				index_oic -= 1
				count += 1

		# delete statements that wont run
		del tokens[end:index_oic]
		index_oic -= (index_oic - end)

		# run the statements
		while line_number < index_oic:
			if not statement(True):
				return False

		line_number = index_oic+1
		return True

	else:
		output_console("error::expected OIC") # NO OIC FOUND
		return False

def loop():
	global tokens, line_number, is_break, in_loop
	in_loop.append(True)

	# IM IN YR
	index_im_in_yr = line_number
	if len(tokens[index_im_in_yr]) < 7:
		output_console("error::expected IM IN YR <label> <operation> YR <variable> [TIL|WILE <expression>] at: " + get_line(index_im_in_yr))
		return False

	line = tokens[index_im_in_yr]
	label = line[1]
	operation = line[2]
	variable = line[4]
	clause = line[5]
	expression = loop_expr(line[6:])
	im_in_yr = get_line(index_im_in_yr)

	# label
	label_regex = re.compile(r"^[a-zA-Z][a-zA-Z0-9_]*$")
	try:
		label_regex.search(line[1]).group()
	except:
		output_console("error::invalid label at: " + im_in_yr)
		return False

	# operation
	if operation not in ["UPPIN", "NERFIN"]:
		output_console("error::expected UPPIN or NERFIN at: " + im_in_yr)
		return False

	# YR
	if line[3]!="YR":
		output_console("error::expected YR at: " + im_in_yr)
		return False		

	# variable
	if variable not in symbols.keys():
		output_console("error::undeclared variable " + variable + " at: " + im_in_yr)
		return False
	elif cast(symbols[variable], "NUMBR")==False:
		output_console("error::variable " + variable + " cannot be casted to numerical value at: " + im_in_yr)
		return False

	symbols[variable] = cast(symbols[variable], "NUMBR")

	# TIL/WILE
	if clause not in ["TIL", "WILE"]:
		output_console("error::expected TIL or WILE at: " + im_in_yr)
		return False

	# expr
	if not expression:
		output_console("error::expected expression at: " + im_in_yr)
		return False

	# IM OUTTA YR
	index_im_outta_yr = line_number
	has_im_outta_yr = False

	while index_im_outta_yr < len(tokens):
		index_im_outta_yr = find_line(index_im_outta_yr, len(tokens))
		if index_im_outta_yr == -1:
			break
		if tokens[index_im_outta_yr][1] == label:
			has_im_outta_yr = True
			break
		index_im_outta_yr += 1

	if has_im_outta_yr:
		# verify nested blocks
		is_valid = validate_blocks(index_im_in_yr, index_im_outta_yr)

		if not is_valid[0]:
			output_console("error at: " + get_line(is_valid[1]))
			return False 

		# result of expression in IT
		it = cast(symbols["IT"], "TROOF")
		should_run = False

		if clause=="TIL":
			should_run = True if it=="FAIL" else False
		else:
			should_run = True if it=="WIN" else False

		increment = 1 if operation=="UPPIN" else -1

		# loop the statements while expression is valid or no GTFO
		while should_run and not is_break:
			while line_number < index_im_outta_yr:
				if not statement(True):
					return False
			symbols[variable] += increment
			loop_expr(line[6:])
			it = symbols["IT"]
			it = cast(it, "TROOF")
			should_run = False

			if clause=="TIL":
				should_run = True if it=="FAIL" else False
			else:
				should_run = True if it=="WIN" else False

		is_break = False
		in_loop.pop(-1)
		line_number = index_im_outta_yr+1
		return True

	else:
		output_console("error::expected IM OUTTA YR " + label) # NO IM OUTTA YR FOUND
		return False



##### GUI #####
# instantiate tkinter window
root = Tk()
root.title("LOLTERPRETER")

# maximize window size
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry(str(w) + "x" + str(h))

# instantiate main frame
main_frame = Frame(root)
main_frame.pack(expand=True, fill=BOTH)
main_frame.pack_propagate(0)

### UPPER FRAME ###
upper_frame = Frame(main_frame)
upper_frame.pack()

# instantiate three frames for the upper frame
ul_frame = Frame(upper_frame)
um_frame = Frame(upper_frame)
ur_frame = Frame(upper_frame)

ul_frame.grid(row=0, column=0)
um_frame.grid(row=0, column=1, sticky="ns")
ur_frame.grid(row=0, column=2, sticky="ns")

### UPPER LEFT FRAME ###
# file explorer
select_file_btn = Button(ul_frame, text="Select file..", command=select_file)
select_file_btn.pack(fill=X)

# text editor
text_editor = scrolledtext.ScrolledText(ul_frame, width=55, height=20)
text_editor.pack()

### UPPER MIDDLE FRAME (LEXEMES TABLE) ###
lexemes_label = Label(um_frame, text="Lexemes") 
lexemes_label.pack()

# lexemes table
lexemes_table = ttk.Treeview(um_frame, show="headings")

# define columns
lexemes_table["columns"] = ("lexeme", "classification")

# define headings
lexemes_table.heading("lexeme", text="Lexeme")
lexemes_table.heading("classification", text="Classification")

# scrollbar
lexemes_scrollbar = ttk.Scrollbar(um_frame, orient=VERTICAL, command=lexemes_table.yview)
lexemes_table.configure(yscroll=lexemes_scrollbar.set)
lexemes_scrollbar.pack(fill=Y, side=RIGHT)

lexemes_table.pack(expand=True, fill=BOTH)

### UPPER RIGHT FRAME (SYMBOL TABLE) ###
symbtable_label = Label(ur_frame, text="Symbol Table") 
symbtable_label.pack()

# symbol table
symbtable_table = ttk.Treeview(ur_frame, show="headings")

# define columns
symbtable_table["columns"] = ("identifier", "value")

# define headings
symbtable_table.heading("identifier", text="Identifier")
symbtable_table.heading("value", text="Value")

# scrollbar
symbtable_scrollbar = ttk.Scrollbar(ur_frame, orient=VERTICAL, command=symbtable_table.yview)
symbtable_table.configure(yscroll=symbtable_scrollbar.set)
symbtable_scrollbar.pack(fill=Y, side=RIGHT)

symbtable_table.pack(expand=True, fill=BOTH)

### EXECUTE/RUN BUTTON ###
run_btn = Button(main_frame, text="EXECUTE", command=run)
run_btn.pack(pady=5, fill=X)

### CONSOLE ###
console = scrolledtext.ScrolledText(main_frame)
console.pack(expand=True, fill=BOTH)
console["state"] = "disabled"

### start the app ###
root.mainloop()
