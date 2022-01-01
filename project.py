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
	code = text_editor.get(1.0,'end-1c') # get the input from Text widget
	code = remove_comments(code)
	code = code.split("\n")
	code = remove_whitespaces(code)
	tokenize(code)

def remove_comments(src_code):
	# remove multiline comments
	src_code = re.sub(r"(^|\n)( |\t)*OBTW\s*(\s+((?!TLDR).)*)*\n( |\t)*TLDR( |\t)*(?=(\n|$))", r"\nOBTW\nTLDR\n", src_code) 
	
	# remove single line comments
	src_code = re.sub(r"(^|\s)BTW.*", "\nBTW", src_code)

	return src_code

def remove_whitespaces(src_code):
	temp = []

	for line in src_code:
		line = line.strip() # remove leading and trailing whitespaces
		if line != "":
			temp.append(line) # append line only if it is not an empty string

	return temp

def findMatch(line):
	# lagay yung mga regex here

	#Literal(0-4)
	yarn = r"(\")(.*?)(\")"
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

	# problem: both saem gets separated the second time. no clue why
	# note: PANO PAG WALANG MATCH AT ALL
	allTokens = []
	classify = []
	while line: # we search for tokens at the front of the line over and over, iterating thru the tokens every time until empty na yung line.
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
					classify.append("Unknown Keyword")

				# end the loop pag nahanap na, proceed to find the next one so iloloop ulit yung regex
				break

	return allTokens, classify

def tokenize(code):
	# NOTE
		# throw error if may OBTW or TLDR na nasa same line as other statements?
		# implement this sa checking syntax siguro, for now tokenizing
			# we check if there's an OBTW and TLDR in there maybe? tas throw error if meron
			# this does not match lines na may OBTW na kasama with other lines

	# tokenize
	# assuming na di required ang newline sa YARN
	global tokens

	tokens = []
	classifications = []
	# iterate through every line
	for line in code:
		# separate everything, ignore all spaces
		# check keywords by:
		# creating regex just as a string
		# putthing them in a list
		# iterate through the list
		# if there is a match, we append the match to the list of tokens

		# we look for matches and put them in the list token
		token, classify = findMatch(line)
		tokens.append(token)
		classifications.append(classify)

	fill_table(lexemes_table, tokens, classifications)

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

### start the app ###
root.mainloop()
