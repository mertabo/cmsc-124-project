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


	regEx = [numbr, numbar, strdelimiter, troof, typeLiteral, howizi, hai, kthxbye, ihasa, sumof, diffof, produktof, quoshuntof, modof, biggrof, smallrof, bothof, eitherof, wonof, notKey, anyof, allof, bothsaem, diffrint, smoosh, maek, isnowa, visible, gimmeh, orly, yarly, mebbe, nowai, oic, wtf, omg, omgwtf, iminyr, uppin, nerfin, yr, til, wile, imouttayr, foundyr, ifusayso, gtfo, mkay, identifier, an, a, itz, r, yarn]

	# problem: both saem gets separated the second time. no clue why
	# note: PANO PAG WALANG MATCH AT ALL
	allTokens = []
	noMatch = []
	while True: # we search for tokens at the front of the line over and over, iterating thru the tokens every time until empty na yung line.
		hasMatch = False
		for r in regEx:
			# search for the current r in the line. searches the FRONT of the line.
			token = re.search(r"^([ ]*"+r+r"[ ]*)", line)
			if token:
				hasMatch = True # gawing true, tas if irerepeat yung pagsearch, gagawin ulet false

				# remove the match from the line and remove the spaces
				unspacedtoken = token.group().strip(r"^([ ]+)([ ]+)$")
				line = line.replace(token.group(), "")

				# append to allTokens
				allTokens.append(unspacedtoken)

				# end the loop pag nahanap na, proceed to find the next one so iloloop ulit yung regex
				break

		if hasMatch==False:
			# if the front of the line has no match, remove.
			# lagay mo yung first token here
			unmatched = line.split()[0]
			line = line.replace(unmatched, "")

			# append to allTokens
			noMatch.append(unmatched)

		# check if line is wala na
		if re.match(r"^(\s*\n*)$", line):
			break

	return allTokens, noMatch

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
	noMatches = []
	# iterate through every line
	for line in code:
		# separate everything, ignore all spaces
		# check keywords by:
		# creating regex just as a string
		# putthing them in a list
		# iterate through the list
		# if there is a match, we append the match to the list of tokens

		# we look for matches and put them in the list token
		token, noMatches = findMatch(line)

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

