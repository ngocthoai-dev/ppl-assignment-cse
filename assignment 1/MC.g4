// 1652579
grammar MC;

@lexer::header {
from lexererr import *
}

@lexer::members {
def emit(self):
    tk = self.type
    if tk == self.UNCLOSE_STRING:
        result = super().emit();
        raise UncloseString(result.text);
    elif tk == self.ILLEGAL_ESCAPE:
        result = super().emit();
        raise IllegalEscape(result.text);
    elif tk == self.ERROR_CHAR:
        result = super().emit();
        raise ErrorToken(result.text);
    else:
        return super().emit();
}

options{
    language=Python3;
}

program: declaration+ EOF;

mcType: primType | VOIDTYPE;
primType: INTTYPE | FLOATTYPE | BOOLEANTYPE | STRINGTYPE;
outputPara: primType LSB RSB;
literal: INTLIT | FLOATLIT | BOOLLIT | STRINGLIT;
funcall: (ID LP expList? RP) | builtInFunc;
expList: exp (CM exp)*;

// Declaration
declaration: varDec | funcDec;
varDec: primType varDecId (CM varDecId)* SEMI;
varDecId: ID | ID LSB INTLIT RSB;
funcDec: (mcType | outputPara) ID LP paraList? RP blockSt;
paraList: paraDec (CM paraDec)*;
paraDec: primType (ID | ID LSB RSB);

// Statements
statement:  noIfStatement | ifSt;
noIfStatement: (doWhileSt | breakSt | continueSt | returnSt | expSt) SEMI | forSt | blockSt;
ifSt: ifElseSt | ifNoElseSt;
ifElseSt: IF LP exp RP ifElseSt ELSE ifElseSt | noIfStatement;
ifNoElseSt: IF LP exp RP ifSt | IF LP exp RP ifElseSt ELSE ifNoElseSt;
doWhileSt: DO statement+ WHILE exp;
forSt: FOR LP exp SEMI exp SEMI exp RP statement;
breakSt: BREAK;
continueSt: CONTINUE;
returnSt: RETURN exp?;
expSt: exp;
blockSt: LB (statement | varDec)* RB;

// Expression
exp: exp1 ASSIGN exp | exp1;
exp1 : exp1 OR exp2 | exp2;
exp2 : exp2 AND exp3 | exp3;
exp3 : exp4 (EQ|NEQ) exp4 | exp4;
exp4 : exp5 (LT|LTE|GT|GTE) exp5 | exp5;
exp5 : exp5 (ADD|SUB) exp6 | exp6;
exp6 : exp6 (DIV|MUL|MOD) exp7 | exp7;
exp7 : (SUB|NOT) exp7 | exp8;
exp8 : exp9 LSB exp RSB | exp9;
exp9 : LP exp RP | operand;
operand: ID | literal | funcall;
//exp: LP exp RP
//| exp LSB exp RSB
//| <assoc=right> (SUB | NOT) exp
//| <assoc=left> exp (MUL | DIV | MOD) exp
//| <assoc=left> exp (ADD | SUB) exp
//| relationalExp (LT | LTE | GT | GTE) relationalExp
//| equalityExp (EQ | NEQ) equalityExp
//| <assoc=left> exp AND exp
//| <assoc=left> exp OR exp
//| <assoc=right> exp ASSIGN exp
//| operand;
//relationalExp: LP exp RP
//| relationalExp LSB relationalExp RSB
//| <assoc=right> (SUB | NOT) relationalExp
//| <assoc=left> relationalExp (MUL | DIV | MOD) relationalExp
//| <assoc=left> relationalExp (ADD | SUB) relationalExp
//| operand;
//equalityExp: LP exp RP
//| equalityExp LSB equalityExp RSB
//| <assoc=right> (SUB | NOT) equalityExp
//| <assoc=left> equalityExp (MUL | DIV | MOD) equalityExp
//| <assoc=left> equalityExp (ADD | SUB) equalityExp
//| relationalExp (LT | LTE | GT | GTE) relationalExp
//| operand;
//operand: ID | literal | arrayElement | funcall;
//arrayElement: (funcall | ID) LSB exp RSB;

// built in function
builtInFunc: intFunc | floatFunc | boolFunc | stringFunc | lineFunc;
intFunc: GETINT LP RP | PUTINT LP exp RP;
floatFunc: GETFLOAT LP RP | PUTFLOAT LP exp RP;
boolFunc: PUTBOOL LP exp RP;
stringFunc: PUTSTRING LP exp RP;
lineFunc: LINEFUNC LP RP;

/*---------------------------------------------*/
// KW: BOOLEANTYPE | BREAK | CONTINUE | ELSE | FOR | FLOATTYPE | IF | INTTYPE | RETURN | VOIDTYPE | DO | WHILE | TRUE | FALSE | STRINGTYPE;

// Types
INTTYPE: 'int';
VOIDTYPE: 'void';
FLOATTYPE: 'float';
BOOLEANTYPE: 'boolean';
STRINGTYPE: 'string';

// Keywords
BREAK: 'break';
CONTINUE: 'continue';
ELSE: 'else';
FOR: 'for';
IF: 'if';
RETURN: 'return';
DO: 'do';
WHILE: 'while';

// Operators
ADD: '+';
SUB: '-';
MUL: '*';
DIV: '/';
NOT: '!';
MOD: '%';
OR: '||';
AND: '&&';
NEQ: '!=';
EQ: '==';
LT: '<';
GT: '>';
LTE: '<=';
GTE: '>=';
ASSIGN: '=';

// Literal
BOOLLIT: TRUE | FALSE;
INTLIT: DIGIT+;
FLOATLIT: ((DIGIT* '.'? DIGIT+)|(DIGIT+ '.'? DIGIT*))(('E'|'e')'-'? DIGIT+)?;
ID: LETTER (LETTER | DIGIT)*;
fragment DIGIT: [0-9];
fragment LETTER: [a-zA-Z_];
STRINGLIT: '"'String'"'{self.text = self.text[1:len(self.text)-1]};
fragment String: ('\\'[bfrnt"\\]|~["\r\n\\])*;

// boolean option
TRUE: 'true';
FALSE: 'false';

// Separators
LP: '(';
RP: ')';
LB: '{';
RB: '}';
LSB: '[';
RSB: ']';
SEMI: ';';
CM: ',';

// Built-in Functions
GETINT: 'getInt';
PUTINT: 'putInt' | 'putIntLn';
GETFLOAT: 'getFloat';
PUTFLOAT: 'putFloat' | 'putFloatLn';
PUTBOOL: 'putBool' | 'putBoolLn';
PUTSTRING: 'putString' | 'putStringLn';
LINEFUNC: 'putLn';

// Whitespace, Block comment, Line comment
WS : [ \t\r\n]+ -> skip;
BLOCKCMT: '/*'.*?'*/' -> skip;
LINECMT: '//'~[\r\n]* -> skip;

// Illegal escape, Unclosed string, Error character
ILLEGAL_ESCAPE: '"'String?('\\'~[bfrnt"\\]) {self.text = self.text[1:];};
UNCLOSE_STRING: '"'String?(~'"'|[\r\n])? {
if self.text[len(self.text)-1:len(self.text)] == '\r' or self.text[len(self.text)-1:len(self.text)] == '\n':
    self.text = self.text[1:len(self.text)-1];
else:
    self.text = self.text[1:];};
ERROR_CHAR: FLOATLIT '.' | ~[0-9]+ '.' [e|E] | .;