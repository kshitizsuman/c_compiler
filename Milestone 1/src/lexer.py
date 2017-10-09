import sys
sys.path.insert(0, "../..")

import ply.lex as lex

reserved = (
	'RETURN', 'SHORT', 'SIGNED', 'SIZEOF','STATIC', 'STRUCT', 'SWITCH', 'TYPEDEF','CHAR', 'CONST', 'CONTINUE', 'DEFAULT', 'DO', 'DOUBLE', 'ELSE', 'ENUM', 'EXTERN','AUTO', 'BREAK', 'CASE',  'FLOAT', 'FOR', 'GOTO', 'IF', 'INT', 'LONG', 'REGISTER','UNION', 'UNSIGNED', 'VOID', 'VOLATILE', 'WHILE','RESTRICT','INLINE',
)

tokens = reserved + (
	'IDENTIFIER', 'TYPEID', 'I_CONSTANT', 'F_CONSTANT', 'STRINGLITERAL', 'CCONST','PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MOD','OR_OP', 'AND_OP', 'NOT_OP', 'XOR', 'LNOT','LEFT_OP', 'RIGHT_OP', 'LOR', 'LAND', 'LT_OP', 'LE_OP', 'GT_OP', 'GE_OP', 'EQ_OP', 'NE_OP','EQUALS', 'MUL_ASSIGN','DIV_ASSIGN','MOD_ASSIGN','ADD_ASSIGN','SUB_ASSIGN','LEFT_ASSIGN','RIGHT_ASSIGN','AND_ASSIGN','OR_ASSIGN','XOR_ASSIGN','INC_OP', 'DEC_OP','PTR_OP','CONDOP','LPAREN', 'RPAREN','LBRACKET', 'RBRACKET','LBRACE', 'RBRACE','COMMA', 'PERIOD', 'SEMI', 'COLON','ELLIPSIS','ALIGNAS','ALIGNOF','BOOL','COMPLEX','GENERIC','IMAGINARY','NORETURN','STATIC_ASSERT','THREAD_LOCAL','FUNC_NAME',
)

rdict = {}
for i in reserved:
	rdict[i.lower()] = i

t_ignore = ' \t\x0c'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MOD = r'%'
t_OR_OP = r'\|'
t_AND_OP = r'&'
t_NOT_OP = r'~'
t_XOR = r'\^'
t_LEFT_OP = r'<<'
t_RIGHT_OP = r'>>'
t_LOR = r'\|\|'
t_LAND = r'&&'
t_LNOT = r'!'
t_LT_OP = r'<'
t_GT_OP = r'>'
t_LE_OP = r'<='
t_GE_OP = r'>='
t_EQ_OP = r'=='
t_NE_OP = r'!='
t_EQUALS = r'='
t_MUL_ASSIGN = r'\*='
t_DIV_ASSIGN = r'/='
t_MOD_ASSIGN = r'%='
t_ADD_ASSIGN = r'\+='
t_SUB_ASSIGN = r'-='
t_LEFT_ASSIGN = r'<<='
t_RIGHT_ASSIGN = r'>>='
t_AND_ASSIGN = r'&='
t_OR_ASSIGN = r'\|='
t_XOR_ASSIGN = r'\^='
t_INC_OP = r'\+\+'
t_DEC_OP = r'--'
t_PTR_OP = r'->'
t_CONDOP = r'\?'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_COMMA = r','
t_PERIOD = r'\.'
t_SEMI = r';'
t_COLON = r':'
t_ELLIPSIS = r'\.\.\.'
t_ALIGNAS = r'_Alignas'
t_ALIGNOF = r'_Alignof'
t_BOOL = r'_Bool'
t_COMPLEX = r'_Complex'
t_GENERIC = r'_Generic'
t_IMAGINARY = r'_Imaginary'
t_NORETURN = r'_Noreturn'
t_STATIC_ASSERT = r'_Static_assert'
t_THREAD_LOCAL = r'_Thread_local'
t_FUNC_NAME = r'__func__'
t_I_CONSTANT = r'\d+([uU]|[lL]|[uU][lL]|[lL][uU])?'
t_F_CONSTANT = r'((\d+)(\.\d+)(e(\+|-)?(\d+))? | (\d+)e(\+|-)?(\d+))([lL]|[fF])?'
t_STRINGLITERAL = r'\"([^\\\n]|(\\.))*?\"'
t_CCONST = r'(L)?\'([^\\\n]|(\\.))*?\''

def t_IDENTIFIER(t):
	r'[A-Za-z_][\w_]*'
	t.type = rdict.get(t.value, "IDENTIFIER")
	return t

def t_NEWLINE(t):
	r'\n+'
	t.lexer.lineno += t.value.count("\n")

def t_comment(t):
	r'/\*(.|\n)*?\*/ | //(.)*?\n'
	t.lexer.lineno += t.value.count('\n')

def t_preprocessor(t):
	r'\#(.)*?\n'
	t.lexer.lineno += 1

def t_error(t):
	print("Error : %s" % str(t.value[0]))
	t.lexer.skip(1)

lexer = lex.lex()
if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "{token type, token name, line nunmber, index relative to start of input}"
		lex.runmain(lexer)
	else:
		fo = open(str(sys.argv[1]), "r+")
		data = fo.read()
		fo.close()
		print "{token type, token name, line nunmber, index relative to start of input}"
		lex.runmain(lexer, data)
