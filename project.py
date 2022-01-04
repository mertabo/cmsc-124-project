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
        # reset some variables
        global line_number, tokens
        line_number = 0
        console.delete(1.0, END)

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
        global regExDigit
        
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

        regExDigit = [numbr, numbar]
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
                                #       classify.append("String Delimiter")
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
        console.insert(END, contents) # print contents to GUI
        console.insert(END, "\n") # print contents to GUI

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
        global line_number, expression
        token = get_current_token(0)
        
        expression = []
        # VARIABLE DECLARATION
        if token=="I HAS A" and not is_code_block:
                print("I HAS A")

        # ARITHMETIC OPERATIONS
        elif token=="SUM OF":
                result = (sum_of(tokens[line_number]))
                line_number += 1
                if result: #if syntactically correct, solve
                        get_value(expression)
                return result
        elif token=="DIFF OF":
                result = diff_of(tokens[line_number])
                line_number += 1
                if result: #if syntactically correct, solve
                        get_value(expression)
                return result
        elif token=="PRODUKT OF":
                result = prod_of(tokens[line_number])
                line_number += 1
                if result: #if syntactically correct, solve
                        get_value(expression)
                return result
        elif token=="QUOSHUNT OF":
                result = quo_of(tokens[line_number])
                line_number += 1
                if result: #if syntactically correct, solve
                        get_value(expression)
                return result
        elif token=="MOD OF":
                result = mod_of(tokens[line_number])
                line_number += 1
                if result: #if syntactically correct, solve
                        get_value(expression)
                return result
        elif token=="BIGGR OF":
                result = biggr_of(tokens[line_number])
                line_number += 1
                if result: #if syntactically correct, solve
                        get_value(expression)
                return result
        elif token=="SMALLR OF":
                result = smallr_of(tokens[line_number])
                line_number += 1
                if result: #if syntactically correct, solve
                        get_value(expression)
                return result

        # BOOLEAN OPERATIONS
        elif token=="BOTH OF":
                result = bool_op(tokens[line_number])
                line_number += 1
                if result: #if syntactically correct, solve
                        eval_troof(expression)
                return result
        elif token=="EITHER OF":
                result = bool_op(tokens[line_number])
                line_number += 1
                if result: #if syntactically correct, solve
                        eval_troof(expression)
                return result
        elif token=="WON OF":
                result = bool_op(tokens[line_number])
                line_number += 1
                if result: #if syntactically correct, solve
                        eval_troof(expression)
                return result
        elif token=="NOT":
                result = bool_op(tokens[line_number])
                line_number += 1
                if result: #if syntactically correct, solve
                        eval_troof(expression)
                return result
        elif token=="ALL OF":
                result = bool_op(tokens[line_number])
                line_number += 1
                if result: #if syntactically correct, solve
                        eval_troof(expression)
                return result
        elif token=="ANY OF":
                result = bool_op(tokens[line_number])
                line_number += 1
                if result: #if syntactically correct, solve
                        eval_troof(expression)
                return result

        # COMPARISON OPERATIONS
        elif token=="BOTH SAEM":
                return both_saem(tokens[line_number])
        elif token=="DIFFRINT":
                return diffrint(tokens[line_number])

        # CONCATENTATION
        elif token=="SMOOSH":
                print("SMOOSH")

        # TYPECAST
        elif token=="MAEK":
                print("MAEK")

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
                print("WTF?")
        # LOOP
        elif token=="IM IN YR":
                print("IM IN YR")

        #### FUNCTIONS FUNCTIONS FUNCTIONS FUNCTIONS FUNCTIONS FUNCTIONS FUNCTIONS 
        #### FUNCTIONS FUNCTIONS FUNCTIONS FUNCTIONS FUNCTIONS FUNCTIONS FUNCTIONS 
        #### FUNCTIONS FUNCTIONS FUNCTIONS FUNCTIONS FUNCTIONS FUNCTIONS FUNCTIONS 
        
        # MISUSED KEYWORDS
        elif token=="ITZ" or token=="R" or token=="YA RLY" or token=="NO WAI" or token=="O RLY?" or token=="OMG" or token=="OMGWTF" or token=="OIC" or token=="UPPIN" or token=="NERFIN" or token=="TIL" or token=="WILE" or token=="IM OUTTA YR" or token=="YR" or token=="MEBBE" or token=="MKAY" or token=="AN" or token=="A" or token=="IS NOW A":
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

#FUNCTIONS FOR ARITHMETIC OPERATIONS
def get_value(listOp):
        global symbols
        listOp = listOp[::-1]
       
        final_expr = "("
        for index, element in enumerate(listOp):
                if element == "max":
                        final_expr = "max" + final_expr +"," + listOp[index+1]+")"
                        del listOp[index+1]
                elif element == "min":
                        final_expr = "min" + final_expr +"," + listOp[index+1]+")"
                        del listOp[index+1]
                elif index in range(0,3):
                        final_expr = final_expr + element
                elif index == 3:
                        final_expr = final_expr + ")" + element
                elif (index % 2) == 0:
                        final_expr = "(" + final_expr + element + ")"
                else:
                        final_expr = final_expr + element
        if (len(listOp)) == 3:
                final_expr = final_expr + ")"
       
        result = (eval(final_expr)) #return computed value
        symbols["IT"] = result
        
def check_digit(token):
        global expr 
        is_valid = False
        if (bool(re.match(regExDigit[0], token))): #check if numbr:
                expr = token
                is_valid = True
        elif (bool(re.match(regExDigit[1], token))): #check if numbar:
                expr = token
                is_valid = True
        elif (bool(re.match(r"[a-zA-Z][a-zA-Z0-9_]*", token))): #if identifier check if value is numbr/numbar
                if token in symbols.keys():
                        if symbols[token].isnumeric():
                                expr = symbols[token]
                                is_valid = True
        #elif typecast(line[-1]): # check if typecasting is valid
                #is_valid = True
        return is_valid

def check_implicit(line):
        if (line[0] == '"' or line[0] == "'") and (line[-1] == '"' or line[-1] == "'"):
                del line[0]
                del line[-1]
                if len(line) == 1:
                        return check_digit(line[0])
                else:
                        return False
        else:
                return False
        
def next_op(line):

        if line == []:
                return True
        elif line[0] == "SUM OF":
                return sum_of(line)
        elif line[0] == "DIFF OF":
                return diff_of(line)
        elif line[0] == "PRODUKT OF":
                return prod_of(line)
        elif line[0] == "QUOSHUNT OF":
                return quo_of(line)
        elif line[0] == "MOD OF":
                return mod_of(line)
        elif line[0] == "BIGGR OF":
                return biggr_of(line)
        elif line[0] == "SMALLR OF":
                return smallr_of(line)
        else:
                output_console("error at: " + get_line(line_number))
                return False

def check_nested(line):
        global expression
        if line[-1] == "AN":
                del line[-1]
                del line[0]
                if (len(line)==1):
                        expression.append(line[-1])
                        return check_digit(line[-1])
                elif (len(line)==3):
                        expression.append(line[1])
                        return check_implicit(line)
                else:
                        return next_op(line)
                                
        else:
                output_console("error at: " + get_line(line_number))
                return False

def sum_of(line):
        global expression, expr
        
        if check_digit(line[-1]):
                del line[-1]
                expression.append(expr)
                expression.append("+")
                return check_nested(line)
        elif check_implicit(line[-3:]):
                del line[-3:]
                expression.append(expr)
                expression.append("+")
                return check_nested(line)
        else:
                output_console("error at: " + get_line(line_number))
                return False


def diff_of(line):
        if check_digit(line[-1]):
                del line[-1]
                expression.append(expr)
                expression.append("-")
                return check_nested(line)
        elif check_implicit(line[-3:]):
                del line[-3:]
                expression.append(expr)
                expression.append("-")
                return check_nested(line)
        else:
                output_console("error at: " + get_line(line_number))
                return False
        
def prod_of(line):
        if check_digit(line[-1]):
                del line[-1]
                expression.append(expr)
                expression.append("*")
                return check_nested(line)
        elif check_implicit(line[-3:]):
                del line[-3:]
                expression.append(expr)
                expression.append("*")
                return check_nested(line)
        else:
                output_console("error at: " + get_line(line_number))
                return False

def quo_of(line):
        if check_digit(line[-1]):
                del line[-1]
                expression.append(expr)
                expression.append("/")
                return check_nested(line)
        elif check_implicit(line[-3:]):
                del line[-3:]
                expression.append(expr)
                expression.append("/")
                return check_nested(line)
        else:
                output_console("error at: " + get_line(line_number))
                return False

def mod_of(line):
        if check_digit(line[-1]):
                del line[-1]
                expression.append(expr)
                expression.append("%")
                return check_nested(line)
        elif check_implicit(line[-3:]):
                del line[-3:]
                expression.append(expr)
                expression.append("%")
                return check_nested(line)
        else:
                output_console("error at: " + get_line(line_number))
                return False

def biggr_of(line):
        if check_digit(line[-1]):
                del line[-1]
                return check_nested(line)
                expression.append(expr)
                expression.append("max")
        elif check_implicit(line[-3:]):
                del line[-3:]
                expression.append(expr)
                expression.append("max")
                return check_nested(line)
        else:
                output_console("error at: " + get_line(line_number))
                return False

def smallr_of(line):
        if check_digit(line[-1]):
                del line[-1]
                expression.append(expr)
                expression.append("min")
                return check_nested(line)
        elif check_implicit(line[-3:]):
                del line[-3:]
                expression.append(expr)
                expression.append("min")
                return check_nested(line)
        else:
                output_console("error at: " + get_line(line_number))
                return False

#FUNCTIONS FOR BOOLEAN OPERATORS
def eval_troof(expression):
        global symbols
        final_expr = ""
        for index, element in enumerate(expression):
                if element == "WIN":
                        expression[index] = "True"
                elif element == "FAIL":
                        expression[index] = "False"
                        
        for index, element in enumerate(expression):
                if element == "not ":
                        final_expr = element + final_expr
                else:
                        final_expr = final_expr + element 

        result = (eval(final_expr))
        
        if result == True:
                result = "WIN"
        else:
                result = "FAIL"

        symbols["IT"] = result
                
                        
def check_troof(token):
        is_valid = False
        global troof
        
        if (bool(re.match(r"(WIN|FAIL)", token))): #check if troof:
                troof = token
                is_valid = True
        elif (bool(re.match(r"[a-zA-Z][a-zA-Z0-9_]*", token))): #if identifier check if value is numbr/numbar
                if token in symbols.keys():
                        if (bool(re.matched(r"(WIN|FAIL)",symbols[token]))):
                                troof = symbols[token]
                                is_valid = True
        #elif typecast(line[-1]): # check if implicit typecasting is valid
                #is_valid = True
        return is_valid

def next_op_allany(line, operation):

        global expression, troof

        if line[0] == "NOT":
                del line[0]
                expression.append("not ")
                if check_troof(line[0]):
                        expression.append(troof)
                        del line[0]
                        if line and line[0] == "AN":
                                del line[0]
                                if line == []:
                                        return True
                                else:
                                        expression.append(operation)
                                        return next_op_allany(line, operation)
                        elif line == []:
                                return True
                        
        elif line[0] == 'BOTH OF' or line[0] == 'EITHER OF' or line[0] == 'WON OF':
                if check_troof(line[1]):
                        expression.append(troof)
                        del line[1]
                        if line[0] == 'BOTH OF':
                                expression.append(" and ")
                        elif line[0] == 'EITHER OF':
                                expression.append(" or ")
                        elif line[0] == 'WON OF':
                                expression.append(" ^ ")
                        else:
                                return False
                        del line[0]
                        if line[0] == "AN":
                                del line[0]
                                if check_troof(line[0]):
                                        expression.append(troof)
                                        del line[0]
                                        if line and line[0] == "AN":
                                                expression.append(operation)
                                                del line[0]
                                                if line == []:
                                                        return True
                                                else:
                                                        return next_op_allany(line, operation)
                                        elif line == []:
                                                return True
                                        else:
                                                return False
                                else:
                                        return False
                        else:
                                return False
                else:
                        return False
        else:
                return False
        
def allany_of(line):
        global expression, troof

        if line[0] == "NOT":
                del line[0]
                expression.append("not ")
                if check_troof(line[0]):
                        expression.append(troof)
                        del line[0]
                        if line and line[0] == "AN":
                                del line[0]
                                if line == []:
                                        return True
                                else:
                                        allany_of(line)
                        elif line == []:
                                return True
                        
        elif line[0] == 'BOTH OF' or line[0] == 'EITHER OF' or line[0] == 'WON OF':
                if check_troof(line[1]):
                        expression.append(troof)
                        del line[1]
                        if line[0] == 'BOTH OF':
                                expression.append(" and ")
                        elif line[0] == 'EITHER OF':
                                expression.append(" or ")
                        elif line[0] == 'WON OF':
                                expression.append(" ^ ")
                        elif line[0] == 'ALL OF' and line[-1] == 'MKAY':
                                del line[0]
                                del line[-1]
                                return next_op_allany(line, ' and ')
                        elif line[0] == 'ANY OF' and line[-1] == 'MKAY':
                                del line[0]
                                del line[-1]
                                return next_op_allany(line, ' or ')
                        else:
                                return False
                        del line[0]
                        if line[0] == "AN":
                                del line[0]
                                if check_troof(line[0]):
                                        expression.append(troof)
                                        del line[0]
                                        if line and line[0] == "AN":
                                                del line[0]
                                                if line == []:
                                                        return True
                                                else:
                                                        return allany_of(line)
                                        elif line == []:
                                                return True
                                        else:
                                                return False
                                else:
                                        return False
                        else:
                                return False
                else:
                        return False
        else:
                return False
        
        
def bool_op(line):
        global expression
        if line[0] == "ALL OF" and line[-1] == "MKAY":
                del line[0]
                del line[-1]
                result = next_op_allany(line, " and ")
        elif line[0] == 'ANY OF' and line[-1] == 'MKAY':
                del line[0]
                del line[-1]
                result = next_op_allany(line, " or ")
        elif line[-1] != 'MKAY':
                result = allany_of(line)
        else:
                result = False

        if result == False:
                output_console("error at: " + get_line(line_number))
        return result

#FUNCTIONS FOR COMPARISON OPERATIONS
def valid_number(token):
        global next_num
        if token.isnumeric():
                next_num = token
                return True
        elif token in symbols:
                if symbols[token].isnumeric():
                        next_num = symbols[token]
                        return True
        return False

def both_saem(line):
        global next_num, line_number
        line_number += 1
        if line[0] == "BOTH SAEM":
                del line[0]
                if valid_number(line[0]):
                        first_digit = next_num
                        del line[0]
                        if line[0] == "AN":
                                del line[0]
                                if valid_number(line[0]):
                                        second_digit = next_num
                                        del line[0]
                                        if line == []:
                                                result = (first_digit  == second_digit)
                                                if result:
                                                        symbols["IT"] = "WIN"
                                                        return True
                                                else:
                                                        symbols["IT"] = "FAIL"
                                                        return True
                                        else:
                                                output_console("error at: " + get_line(line_number))
                                                return False
                                elif line[0] == "BIGGR OF":
                                        del line[0]
                                        if line[0] == first_digit:
                                                del line[0]
                                                if line[0] == "AN":
                                                        del line[0]
                                                        if valid_number(line[0]):
                                                                second_digit = next_num
                                                                del line[0]
                                                                if line == []:
                                                                        result = (first_digit  >= second_digit)
                                                                        if result:
                                                                                symbols["IT"] = "WIN"
                                                                                return True
                                                                        else:
                                                                                symbols["IT"] = "FAIL"
                                                                                return True
                                        
                                                                else:
                                                                        output_console("error at: " + get_line(line_number))
                                                                        return False
                                                        else:
                                                                output_console("error at: " + get_line(line_number))
                                                                return False
                                                else:
                                                        output_console("error at: " + get_line(line_number))
                                                        return False
                                        else:
                                                output_console("error at: " + get_line(line_number))
                                                return False
                                elif line[0] == "SMALLR OF":
                                        del line[0]
                                        if line[0] == first_digit:
                                                del line[0]
                                                if line[0] == "AN":
                                                        del line[0]
                                                        if valid_number(line[0]):
                                                                second_digit = next_num
                                                                del line[0]
                                                                if line == []:
                                                                        result = (first_digit  <= second_digit)
                                                                        if result:
                                                                                symbols["IT"] = "WIN"
                                                                                return True
                                                                        else:
                                                                                symbols["IT"] = "FAIL"
                                                                                return True
                                        
                                                                else:
                                                                        output_console("error at: " + get_line(line_number))
                                                                        return False
                                                        else:
                                                                output_console("error at: " + get_line(line_number))
                                                                return False
                                                else:
                                                        output_console("error at: " + get_line(line_number))
                                                        return False
                                        else:
                                                output_console("error at: " + get_line(line_number))
                                                return False
                                else:
                                        output_console("error at: " + get_line(line_number))
                                        return False
                        else:
                                output_console("error at: " + get_line(line_number))
                                return False
                else:
                        output_console("error at: " + get_line(line_number))
                        return False
        else:
                output_console("error at: " + get_line(line_number))
                return False
def diffrint(line):
        global next_num, line_number
        line_number += 1
        if line[0] == "DIFFRINT":
                del line[0]
                if valid_number(line[0]):
                        first_digit = next_num
                        del line[0]
                        if line[0] == "AN":
                                del line[0]
                                if valid_number(line[0]):
                                        second_digit = next_num
                                        del line[0]
                                        if line == []:
                                                result = (first_digit  != second_digit)
                                                if result:
                                                        symbols["IT"] = "WIN"
                                                        return True
                                                else:
                                                        symbols["IT"] = "FAIL"
                                                        return True
                                        else:
                                                output_console("error at: " + get_line(line_number))
                                                return False
                                elif line[0] == "BIGGR OF":
                                        del line[0]
                                        if line[0] == first_digit:
                                                del line[0]
                                                if line[0] == "AN":
                                                        del line[0]
                                                        if valid_number(line[0]):
                                                                second_digit = next_num
                                                                del line[0]
                                                                if line == []:
                                                                        result = (first_digit  > second_digit)
                                                                        if result:
                                                                                symbols["IT"] = "WIN"
                                                                                return True
                                                                        else:
                                                                                symbols["IT"] = "FAIL"
                                                                                return True
                                        
                                                                else:
                                                                        output_console("error at: " + get_line(line_number))
                                                                        return False
                                                        else:
                                                                output_console("error at: " + get_line(line_number))
                                                                return False
                                                else:
                                                        output_console("error at: " + get_line(line_number))
                                                        return False
                                        else:
                                                output_console("error at: " + get_line(line_number))
                                                return False
                                elif line[0] == "SMALLR OF":
                                        del line[0]
                                        if line[0] == first_digit:
                                                del line[0]
                                                if line[0] == "AN":
                                                        del line[0]
                                                        if valid_number(line[0]):
                                                                second_digit = next_num
                                                                del line[0]
                                                                if line == []:
                                                                        result = (first_digit  < second_digit)
                                                                        if result:
                                                                                symbols["IT"] = "WIN"
                                                                                return True
                                                                        else:
                                                                                symbols["IT"] = "FAIL"
                                                                                return True
                                        
                                                                else:
                                                                        output_console("error at: " + get_line(line_number))
                                                                        return False
                                                        else:
                                                                output_console("error at: " + get_line(line_number))
                                                                return False
                                                else:
                                                        output_console("error at: " + get_line(line_number))
                                                        return False
                                        else:
                                                output_console("error at: " + get_line(line_number))
                                                return False
                                else:
                                        output_console("error at: " + get_line(line_number))
                                        return False
                        else:
                                output_console("error at: " + get_line(line_number))
                                return False
                else:
                        output_console("error at: " + get_line(line_number))
                        return False
        else:
                output_console("error at: " + get_line(line_number))
                return False
        
        
def find_end_block(needed_token, incrementor, start, end):
        max_length = len(tokens)
        if start >= max_length and end >= max_length:
                return -1

        count = 1
        for i in range(start, end):
                token = tokens[i][0]
                if token==needed_token:
                        count -= 1
                elif token in incrementor:
                        count += 1

                if count==0:
                        return i
        return -1

                
def if_then():
        # MEBBE MEBBE MEBBE MEBBE MEBBE MEBBE MEBBE
        # MEBBE MEBBE MEBBE MEBBE MEBBE MEBBE MEBBE
        # MEBBE MEBBE MEBBE MEBBE MEBBE MEBBE MEBBE

        global line_number

        # O RLY?
        if get_line(line_number)=="O RLY?": 
                line_number += 1
        else:
                output_console("error at: " + get_line(line_number)) # NO O RLY? FOUND
                return False

        # YA RLY
        index_ya_rly = find_line("YA RLY", line_number, line_number+1)

        if index_ya_rly > -1 and get_line(index_ya_rly)=="YA RLY":
                line_number += 1
        else:
                output_console("error at: " + get_line(line_number)) # NO YA RLY FOUND
                return False

        # OIC
        index_oic = find_end_block("OIC", ["O RLY?", "WTF?"], line_number, len(tokens))
        has_oic = index_oic > -1 and get_line(index_oic)=="OIC"

        if has_oic:
                # NO WAI
                index_no_wai = find_line("NO WAI", line_number, index_oic+1)
                has_no_wai = index_no_wai > -1 and get_line(index_no_wai)=="NO WAI"

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
                output_console("error at: " + get_line(index_oic)) # NO OIC FOUND
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

### start the app ###
root.mainloop()
