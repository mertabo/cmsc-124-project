from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
import tkinter.scrolledtext as scrolledtext
import re

##### GLOBAL VARIABLES #####
tokens = []
line_number = 0
symbols = {"IT": "NOOB"}
# for operations
expression = []
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
	global tokens, line_number, symbols, expression, is_break, in_loop
	tokens = []
	line_number = 0
	symbols = {"IT": "NOOB"}
	expression = []
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
				elif index in range(1,3):
					allTokens[-1] = eval(unspacedtoken)
					classify.append("Literal")					
				elif index in range(3,5):
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
			lhs_value = str(lhs[i][j])
			rhs_value = str(rhs[i][j])

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
		string += str(word) + ' '

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
				fill_table(symbtable_table, [list(symbols.keys())], [list(symbols.values())])
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
		return i_has_a()

	# OPERATIONS
	elif token in ["SUM OF", "DIFF OF", "PRODUKT OF", "QUOSHUNT OF", "MOD OF", "BIGGR OF", "SMALLR OF", "BOTH OF", "EITHER OF", "WON OF", "NOT", "ALL OF", "ANY OF", "BOTH SAEM", "DIFFRINT"]:
		if eval_expr(tokens[line_number]):
			line_number += 1
			return True
		else:
			return False

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
			return assignment()
		else: # UNKNOWN PATTERN
			output_console("error at: " + get_line(line_number))
			return False

	line_number += 1
	return True

def is_numeric(token):
	return token.replace('.','',1).replace('-','',1).isdigit()

def is_literal(token):
	# NUMBR, NUMBAR, YARN, TROOF
	if token=='"':
		return "YARN"
	elif type(token)==int:
		return "NUMBR"
	elif type(token)==float:
		return "NUMBAR"
	elif token in ["WIN", "FAIL"]:
		return "TROOF"
	elif token=="NOOB":
		return token

	return False

def is_valid_identifier(token):
	# no keywords must be used as identifiers
	regex = re.compile(r"[a-zA-Z][a-zA-Z0-9_]*$")
	keywords = ["WIN", "FAIL", "NUMBR", "NUMBAR", "YARN", "TROOF", "NOOB", "HAI", "KTHXBYE", "I HAS A", "ITZ", "VISIBLE", "GIMMEH", "R", "YA RLY", "NO WAI", "O RLY?", "OMG", "OMGWTF", "OIC", "WTF?", "UPPIN", "NERFIN", "TIL", "WILE", "IM OUTTA YR", "YR", "IM IN YR", "MEBBE", "SMOOSH", "MKAY", "AN", "A", "BOTH SAEM", "DIFFRINT", "BOTH OF", "EITHER OF", "WON OF", "NOT", "ANY OF", "ALL OF", "SUM OF", "DIFF OF", "PRODUKT OF", "QUOSHUNT OF", "MOD OF", "BIGGR OF", "SMALLR OF", "BTW", "OBTW", "TLDR", "MAEK", "IS NOW A", "FOUND YR", "GTFO","I IZ","HOW IZ I" ,"IF U SAY SO"]

	if not regex.search(token) or token in keywords:
		return False

	return True

def eval_expr(token_list):
	if len(token_list) < 2:
		output_console("error::missing operand/s at: " + get_line(line_number))
		return False

	token = token_list[0]

	# ARITHMETIC OPERATIONS
	if token=="SUM OF":
		if not is_valid_operation_call(token_list):
			return False
		result = operations(token_list, "+", True)
		if result or result==0:
			return True
		else:
			return False
	elif token=="DIFF OF":
		if not is_valid_operation_call(token_list):
			return False
		result = operations(token_list, "-", True)
		if result or result==0:
			return True
		else:
			return False
	elif token=="PRODUKT OF":
		if not is_valid_operation_call(token_list):
			return False
		result = operations(token_list, "*", True)
		if result or result==0:
			return True
		else:
			return False
	elif token=="QUOSHUNT OF":
		if not is_valid_operation_call(token_list):
			return False
		result = operations(token_list, "/", True)
		if result or result==0:
			return True
		else:
			return False
	elif token=="MOD OF":
		if not is_valid_operation_call(token_list):
			return False
		result = operations(token_list, "%", True)
		if result or result==0:
			return True
		else:
			return False
	elif token=="BIGGR OF":
		if not is_valid_operation_call(token_list):
			return False
		result = operations(token_list, "BIGGR", True)
		if result or result==0:
			return True
		else:
			return False
	elif token=="SMALLR OF":
		if not is_valid_operation_call(token_list):
			return False
		result = operations(token_list, "SMALLR", True)
		if result or result==0:
			return True
		else:
			return False

	# BOOLEAN OPERATIONS
	elif token=="BOTH OF":
		if not is_valid_operation_call(token_list):
			return False
		result = operations(token_list, "and", "TROOF")
		if result or result==0:
			return True
		else:
			return False
	elif token=="EITHER OF":
		if not is_valid_operation_call(token_list):
			return False
		result = operations(token_list, "or", "TROOF")
		if result or result==0:
			return True
		else:
			return False
	elif token=="WON OF":
		if not is_valid_operation_call(token_list):
			return False
		result = operations(token_list, "^", "TROOF")
		if result or result==0:
			return True
		else:
			return False
	elif token=="NOT":
		if not is_valid_operation_call(token_list):
			return False
		result = operations(token_list, "NOT", "TROOF")
		if result or result==0:
			return True
		else:
			return False
	elif token=="ALL OF":
		return any_all(token_list)
	elif token=="ANY OF":
		return any_all(token_list)
		
	# COMPARISON OPERATIONS
	elif token=="BOTH SAEM":
		if not is_valid_operation_call(token_list):
			return False
		result = operations(token_list, "==", False)
		if result or result==0:
			return True
		else:
			return False
	elif token=="DIFFRINT":
		if not is_valid_operation_call(token_list):
			return False
		result = operations(token_list, "!=", False)
		if result or result==0:
			return True
		else:
			return False

	return True

###START OF OPERATIONS###

def find_end_any_all(token_list):
	if "MKAY" in token_list:
		return token_list.index("MKAY")
	return -1 # no MKAY

def find_second_op(token_list):
	if len(token_list) < 2:
		return -1

	count = 1
	ops = ["SUM OF", "DIFF OF", "PRODUKT OF", "QUOSHUNT OF", "MOD OF", "BIGGR OF", "SMALLR OF", "BOTH OF", "EITHER OF", "WON OF"]
	others = ["ALL OF", "ANY OF"]
	i = 0
	end = len(token_list)

	while i < end:
		if token_list[i] in ops:
			count += 1
		elif token_list[i] in others:
			i = find_end_any_all(token_list[i:])
			if i==-1:
				return -1
		elif token_list[i] == "AN":
			count -= 1
		if count == 0:
			return i
		i += 1

	return -1 # no second operand

def is_valid_operation_call(token_list):
	op_count = 0
	ans_count = 0

	ops = ["SUM OF", "DIFF OF", "PRODUKT OF", "QUOSHUNT OF", "MOD OF", "BIGGR OF", "SMALLR OF", "BOTH OF", "EITHER OF", "WON OF"]
	others = ["ANY OF", "ALL OF"]
	i = 0
	end = len(token_list)

	# end must be literal/variable
	if not is_literal(token_list[-1]):
		output_console("error at: " + get_line(line_number))
		return False

	while i < end:
		if token_list[i] in ops:
			op_count += 1
		elif token_list[i] == "AN":
			ans_count += 1
		elif token_list[i] in others:
			i = find_end_any_all(token_list[i:])
			if i==-1:
				return False
		i += 1

	if op_count==ans_count:
		# check if operands are separated by AN
		for i in range(len(token_list)-1):
			gap = 1
			current_lit = is_literal(token_list[i])
			if current_lit=="YARN":
				gap = 3
				if i+gap >= len(token_list):
					break
			current_var = token_list[i] in symbols.keys()

			next_lit = is_literal(token_list[i+gap])
			next_var = token_list[i+gap] in symbols.keys()
			
			if current_lit and (next_lit or next_var):
				output_console("error::expected AN at: " + get_line(line_number))
				return False
			elif current_var and (next_lit or next_var):
				output_console("error::expected AN at: " + get_line(line_number))
				return False

		return True

	output_console("error at: " + get_line(line_number))
	return False # some operator is not binary

def eval_op(token_list, typecast_to):
	# typecast_to = False, TROOF, True (numbr/numbar)
	# evaluates the operand
	operand = token_list[0]
	literal = is_literal(operand)
	result = 0
	length = len(token_list)


	if literal: # literal
		if (literal=="NUMBR" or literal=="NUMBAR") and typecast_to!="TROOF":
			result = operand
		elif literal=="YARN" and typecast_to=="TROOF":
			result = "FAIL" if token_list[1]!='"' else "WIN"
		elif typecast_to=="TROOF":
			result = cast(operand, "TROOF")
			if bool(result) and result==False:
				output_console("error::operand cannot be typecasted at: " + get_line(line_number))
				return False
		elif literal=="YARN" and "." in operand:
			result = cast(token_list[1], "NUMBAR")
			if bool(result) and result==False:
				output_console("error::operand cannot be typecasted at: " + get_line(line_number))
				return False
		elif literal=="YARN":
			result = cast(token_list[1], "NUMBR")
			if bool(result) and result==False:
				output_console("error::operand cannot be typecasted at: " + get_line(line_number))
				return False
		else:
			result = cast(operand, "NUMBR")
			if bool(result) and result==False:
				output_console("error::operand cannot be typecasted at: " + get_line(line_number))
				return False

	elif operand in symbols.keys(): # variable
		result = symbols[operand]

		if typecast_to==False:
			pass
		elif typecast_to=="TROOF":
			if result in ["WIN", "FAIL"]:
				pass
			elif result=="NOOB":
				result = "FAIL"
			elif type(result)==str:
				result = "FAIL" if result=="" else "WIN"
			else:
				result = cast(result, "TROOF")
				if bool(result) and result==False:
					output_console("error::operand cannot be typecasted at: " + get_line(line_number))
					return False	
		elif type(result)==str and "." in result:
			result = cast(result, "NUMBAR")
			if bool(result) and result==False:
				output_console("error::operand cannot be typecasted at: " + get_line(line_number))
				return False
		else:
			result = cast(result, "NUMBR")
			if bool(result) and result==False:
				output_console("error::operand cannot be typecasted at: " + get_line(line_number))
				return False

	elif eval_expr(token_list): # expression
		result = symbols["IT"]

		if typecast_to==False:
			pass
		elif typecast_to=="TROOF":
			if result in ["WIN", "FAIL"]:
				pass
			elif result=="NOOB":
				result = "FAIL"
			elif type(result)==str:
				result = "FAIL" if result=="" else "WIN"
			else:
				result = cast(result, "TROOF")
				if bool(result) and result==False:
					output_console("error::operand cannot be typecasted at: " + get_line(line_number))
					return False
		elif type(result)==str and "." in result:
			result = cast(result, "NUMBAR")
			if bool(result) and result==False:
				print("here")
				output_console("error::operand cannot be typecasted at: " + get_line(line_number))
				return False
		else:
			result = cast(result, "NUMBR")
			if bool(result) and result==False:
				output_console("error::operand cannot be typecasted at: " + get_line(line_number))
				return False

	return result

def operations(token_list, operation, typecast_to):
	global line_number

	if len(token_list) < 2:
		output_console("error::missing operand at: " + get_line(line_number))
		return False

	# operands may be literal, var, expr of type NUMBR/NUMBAR
	first_op = token_list[1]
	index_second_op = 3

	# if NOT, no 2nd operand
	if operation!="NOT":
		# find 2nd operand
		index_second_op = find_second_op(token_list[1:])

		if index_second_op==-1:
			output_console("error::expected an operand at: " + get_line(line_number))
			return False

		index_second_op += 2
		if index_second_op >= len(token_list):
			output_console("error::expected an operand at: " + get_line(line_number))
			return False

		second_op = token_list[index_second_op]

		# evaluate operands
		rhs = eval_op(token_list[index_second_op:], typecast_to)
		if bool(rhs) and rhs==False:
			return False

		end = index_second_op + 1

		del token_list[index_second_op:]
		token_list.append(rhs)
	else:
		if first_op=='"':
			index_second_op = 5

	lhs = eval_op(token_list[1:index_second_op-1], typecast_to)
	if bool(lhs) and lhs==False:
		return False

	if typecast_to=="TROOF":
		lhs = True if lhs=="WIN" else False

	result = 0
	if operation=="BIGGR":
		result = eval("max("+str(lhs)+","+str(rhs)+")")
	elif operation=="SMALLR":
		result = eval("min("+str(lhs)+","+str(rhs)+")")
	elif operation=="NOT":
		result = eval("not "+str(lhs))
	else:
		result = eval(str(lhs)+" "+operation+" "+str(rhs))
	
	if typecast_to=="TROOF":
		result = "WIN" if result==True else "FAIL"

	symbols["IT"] = result
	return result

def any_all(token_list):
	# check if self nesting
	if "ALL OF" in token_list[1:] or "ANY OF" in token_list[1:]:
		output_console("error::nesting of ALL/ANY OF is not allowed at: " + get_line(line_number))
		return False

	# find end
	index_mkay = find_end_any_all(token_list)
	if index_mkay < 0:
		output_console("error::expected MKAY at: " + get_line(line_number))
		return False

	# check if there's unexpected token/s after MKAY
	if index_mkay!=len(token_list)-1:
		output_console("error::expected EOL at: " + get_line(line_number))
		return False

	# check if token before MKAY is literal/variable
	if not is_literal(token_list[index_mkay-1]) and not token_list[index_mkay-1] in symbols.keys():
		output_console("error::expected an operand at: " + get_line(line_number))
		return False

	# check if second token is not AN
	if token_list[1]=="AN":
		output_console("error::expected an operand at: " + get_line(line_number))
		return False		

	# get operands
	operands = []
	start = 1
	end = 0
	nested = []
	ops = ["SUM OF", "DIFF OF", "PRODUKT OF", "QUOSHUNT OF", "MOD OF", "BIGGR OF", "SMALLR OF", "BOTH OF", "EITHER OF", "WON OF", "BOTH SAEM", "DIFFRINT"]

	for token in token_list:
		if token in ops:
			nested.append(True)
		if token=="AN" and nested:
			nested.pop()
		elif token=="AN" or token=="MKAY":
			operands.append(token_list[start:end])
			start = end+1
		end += 1

	# evaluate the operands
	evaluated_ops = []

	for op in operands:
		result = eval_op(op, "TROOF")
		if result:
			evaluated_ops.append(result)
		else:
			# output_console("error at: " + get_line(line_number))
			return False

	# evaluate operands
	result = ''
	operation = "and" if token_list[0]=="ALL OF" else "or"

	for i in range(len(evaluated_ops)):
		evaluated_ops[i] = True if evaluated_ops[i]=="WIN" else False
		result += str(evaluated_ops[i]) 
		if i != len(evaluated_ops)-1:
			result += " " + operation + " "

	symbols["IT"] = eval(result)
	return True

###END OF OPERATIONS###

def i_has_a():
	global line_number
	line = tokens[line_number]
	length = len(line)

	if length < 2:
		output_console("error::unexpected EOL at: " + get_line(line_number))
		return False

	# get the variable
	l_value = line[1]

	if not is_valid_identifier(l_value):
		output_console("error::invalid variable at: " + get_line(line_number))
		return False

	if l_value in symbols.keys():
		output_console("error::redeclaration at: " + get_line(line_number))
		return False		

	if length==2: # uninitialized
		symbols[l_value] = "NOOB"
	elif length >= 4 and line[2]=="ITZ": # initialized
		r_value = line[3]
		if is_literal(r_value)=="YARN" and length==6: # yarn
			symbols[l_value] = line[4]
		elif is_literal(r_value) and length==4: # other literals
			symbols[l_value] = r_value
		elif r_value in symbols.keys() and length==4: # variable
			symbols[l_value] = symbols[r_value]
		elif eval_expr(line[3:]): # expression
			symbols[l_value] = symbols["IT"]
		else:
			output_console("error::in the literal, variable, or expression at: " + get_line(line_number))
			return False
	else:
		output_console("error at: " + get_line(line_number))
		return False

	line_number += 1
	return True

def assignment():
	global line_number

	line = tokens[line_number]
	length = len(line)

	# check if line has valid length
	if length < 3:
		output_console("error::unexpected EOL at: " + get_line(line_number))
		return False

	# check if lhs is an existing variable
	lhs = line[0]
	
	if lhs not in symbols.keys():
		output_console("error::undeclared variable at: " + get_line(line_number))
		return False

	# check if the next token is R or IS NOW A
	if line[1]=="IS NOW A":
		if length != 3:
			output_console("error at: " + get_line(line_number))
			return False
		line[1] = "R"
		line.insert(2, "MAEK")
		length = len(line)
	elif line[1]!="R":
		output_console("error::expected R or IS NOW A at: " + get_line(line_number))
		return False

	# check if rhs is literal, variable, typecast, or expr
	rhs = line[2]
	value = ''
	eol = False

	if is_literal(rhs)=="YARN" and length==5:
		symbols[lhs] = line[3]
	elif is_literal(rhs) and length==3:
		symbols[lhs] = rhs
	elif rhs in symbols.keys() and length==3:
		symbols[lhs] = symbols[rhs]
	elif rhs=="MAEK":
		if not typecast(line[2:], lhs):
			return False
	elif eval_expr(line[2:]):
		symbols[lhs] = symbols["IT"]
	else:
		output_console("error at: " + get_line(line_number))
		return False

	# update line number and return true
	line_number += 1
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
		elif type(variable)==int:
			return str(variable)
		elif type(variable)==float:
			return(str(round(variable, 2)))

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
	type_result = token_list[-1]

	# check if type is valid
	if type_result not in valid_types:
		output_console("error::type must be TROOF, YARN, NUMBR, NUMBAR, or NOOB at: " + get_line(line_number))
		return False

	# check if has A
	has_a = "A" in token_list
	expr_end = -2 if has_a else -1
	expr_result = eval_expr(token_list[1:expr_end])
	value = token_list[1]

	if expr_result: # expression
		value = 'IT' 
	elif len(token_list[1:expr_end])!=1 or value not in symbols.keys(): # variable
		output_console("error::in expression or variable at: " + get_line(line_number))
		return False

	value = symbols[value]

	# special case for explicit casting
	if value=="NOOB":
		if type_result=="NUMBR":
			symbols[dest] = 0 # store the result to dest
			return True
		elif type_result=="NUMBAR":
			symbols[dest] = 0.0 # store the result to dest
			return True
		elif type_result=="YARN":
			symbols[dest] = '' # store the result to dest
			return True
	
	result = cast(value, type_result) # typecast

	if result==False: # typecast failed
		output_console("error::cannot be typecasted at: " + get_line(line_number))
		return False	

	symbols[dest] = result # store the result to dest
	return True

###CODE BLOCKS###

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
			literal = is_literal(line[1])
			if literal==False:
				return [False, i]
			elif literal=="YARN" and length!=4:
				return [False, i]
			elif literal in ["NUMBR", "NUMBAR", "TROOF"] and length!=2:
				return [False, i]
			if next_statement in invalid:
				return [False, i+1]
		elif token=="IM IN YR": # check if valid loop
			if len(line) > 7:
				regex = re.compile(r"^[a-zA-Z][a-zA-Z0-9_]*$")
				if (not regex.search(line[1])) or (line[2] not in ["UPPIN", "NERFIN"]) or (line[3]!="YR") or (line[4] not in symbols.keys()) or (line[5] not in ["TIL", "WILE"]) or (eval_expr(line[6:])==False): 
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
	expression = eval_expr(line[6:])
	im_in_yr = get_line(index_im_in_yr)

	# label
	if not is_valid_identifier(label):
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
			eval_expr(line[6:])
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
