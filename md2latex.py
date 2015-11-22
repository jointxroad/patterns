#!/usr/bin/python

# This converts a veeeery specific subset of markdown to LaTeX. 
# Takes MD from stdin, produces headless LaTeX (to be included in a complete file) in stdout

import fileinput
import re

# States the main loop can be in
STATE_DEFAULT = 0
STATE_LIST = 1
STATE_DESCRIPTION = 2
STATE_REPEAT = 3

# Functions for translating between MD and LaTeX. Each gets the match object and the current state as input
# And returns the new state

def section(r, state):
	return (state, "\\section{%s}" % (r.group(1)))

def subsection(r, state):
	return (state, "\\subsection{%s}" % (r.group(1))
)

def subsubsection(r, state):
	return (state, "\\subsubsection{%s}" % (r.group(1)))

def itemize(r, state):
	s = state
	o = ""

# If we are in a default state, start the list 
	if s == STATE_DEFAULT:
		o = "\\begin{itemize}\n"
		s = STATE_LIST

	o = o + "\t\\item %s" % (r.group(1))

	return (s, o)

def description(r, state):
	s = state
	o = ""

# Start the list if necessary
	if s == STATE_DEFAULT:
		o = "\\begin{description}\n"
		s = STATE_DESCRIPTION
	
	o = o + "\t\\item[%s] %s" % (r.group(1), r.group(2))

	return (s, o)

def ref(r, state):
# The references appear in itemized lists and such so we want to continue parsing the next 
# patterns after this. Thus, return STATE_REPEAT
	return (STATE_REPEAT, r.group(1) + r.group(2) + " \\ref{%s}" % r.group(3) + r.group(4)) 

def image(r, state):
	label = r.group(1)
	caption = r.group(2)
	img = r.group(3)
	return (state, """\t\t\\begin{figure}[htp]
			\\begin{center}
				\\includegraphics[width=1\\textwidth]{%s}
				\\caption{%s}
				\\label{%s}
			\\end{center}
		\\end{figure}""" % (img, caption, label))

def default(r, state):
	s = state 
	o = ""

# Apparently we have received the end of a list, so close them properly
	if s == STATE_LIST:
		o = "\\end{itemize}\n"
		s = STATE_DEFAULT
	
	if s == STATE_DESCRIPTION:
		o = "\\end{description}\n"
		s = STATE_DEFAULT

	o = o +  r.group(1)
	return (s, o)

# Yes, a dict would be nicer as this is only key-value pairs
# but we want the specific order of the regexps so array it is 
patterns = [
		{'r':'(.*)\[(\w*)\]\(\#(\w*)\)(.*)', 'f':ref},
		{'r':'^\#\s(.*)', 'f':section},
		{'r':'^\#\#\s(.*)', 'f':subsection},
		{'r':'^\#\#\#\s(.*)', 'f':subsubsection},
		{'r':'^\s\*\s\*\*([\w\s]*)\*\*(.*)', 'f':description},
		{'r':'^\s\*\s(.*)', 'f':itemize},
		{'r':'<a\sname\=\"(.*)\"></a>!\[(.*)\]\((.*)\)', 'f':image},
		{'r':'(.*)', 'f':default}

	]


#----------
# Main body
#----------
state = STATE_DEFAULT

print "% Pattern boundary "
# Iterate over the lines from stdin
for l in fileinput.input():
	o = l
	# for each pattern _in specific order_
	for p in patterns:
		m = re.match(p['r'], o)
		if m:
			(state, o) = p['f'](m, state)
			# Should we continue with the rest of the regexps or not?
			if state != STATE_REPEAT:
				print o
				break
			else:
				state = STATE_DEFAULT



