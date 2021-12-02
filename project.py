from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
import re

# notes and bugs
# need a way to throw error if theres no match
# function name gets separated bc it has spaces (sa sample)

##### GLOBAL VARIABLES #####
code = ""

##### FUNCTIONS #####
def read_file(filename):

	file = open(filename, "r")

	contents = file.read() 
	
	file.close()

	return contents

def show_file_contents(contents):
	text_editor.delete(1.0, END) # make sure text editor is clear
	text_editor.insert(1.0, contents) # print contents to GUI

def select_file():
	file_path = fd.askopenfilename(title="Open a LOLCODE file..", filetypes=(("lol files", ".lol"),)) # open a file dialog that shows .lol files only
	if len(file_path) == 0: return # no file selected

	file_contents = read_file(file_path) # get the file contents
	show_file_contents(file_contents) # show file contents to GUI

def remove_comments(src_code):
	# remove multiline comments
	src_code = re.sub("(^|\n| )OBTW[^TLDR]*TLDR( |\n|$)", "", src_code)
	
	# remove single line comments
	src_code = re.sub("(^|\n| )BTW.*", "", src_code)

	return src_code

def remove_whitespaces(src_code):
	temp = []

	for line in src_code:
		line = line.strip() # remove leading and trailing whitespaces
		if line != "":
			temp.append(line) # append line only if it is an empty string

	return temp

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

	# tokenize
	# assuming na di required ang newline sa YARN
	print(code)
	tokens = []
	# iterate through every line
	for line in code:
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

	print(tokens)

def run():
	global code

	code = text_editor.get(1.0,'end-1c') # get the input from Text widget
	code = remove_comments(code)
	code = code.split("\n")
	code = remove_whitespaces(code)
	tokenize(code)


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
text_editor = Text(ul_frame, width=55, height=20)
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
console = Text(main_frame)
console.pack(expand=True, fill=BOTH)

### start the app ###
root.mainloop()

