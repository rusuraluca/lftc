%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define YYDEBUG 1

int yylex(void);
void yyerror(char *s);
%}

%token PROGRAM
%token LIST
%token WHILE
%token INT
%token STRING
%token CHAR
%token FOR
%token VAR
%token IF
%token ELSE
%token OUT
%token IN
%token FINISH
%token RETURN

%token plus
%token minus
%token multiply
%token divide
%token modulo
%token lessOrEqual
%token moreOrEqual
%token less
%token more
%token equal
%token assign
%token different
%token isequal
%token not
%token plusequal
%token minusequal
%token divideequal
%token timesequal
%token or
%token and

%token leftCurlyBracket
%token rightCurlyBracket
%token leftRoundBracket
%token rightRoundBracket
%token leftBracket
%token rightBracket
%token semicolon
%token comma
%token colon
%token apostrophe
%token quote

%token identifier
%token integer_constant
%token char_constant
%token string_constant

%start program

%%

program : PROGRAM cmpdstmt

stmt : simplstmt semicolon | structstmt

cmpdstmt : leftCurlyBracket stmtlist rightCurlyBracket

stmtlist : stmt | stmt stmtlist

simplstmt : assignstmt | iostmt | declaration | arraydecl | returnstmt | expression

returnstmt: RETURN expression | RETURN

declaration : type identifier | type assignstmt

arraydecl : LIST type leftBracket integer_constant rightBracket identifier

assignstmt : identifier assign expression

expression : expression plus term | expression minusequal term | expression minus term | expression plusequal term | arrayaccess | term

arrayaccess : identifier leftBracket integer_constant rightBracket | identifier leftBracket identifier rightBracket

term : term multiply factor | term divide factor | term timesequal factor | term divideequal factor | term modulo factor | factor

factor : leftBracket expression rightBracket | identifier | constant

constant : integer_constant | string_constant | char_constant

iostmt : IN leftRoundBracket identifier rightRoundBracket | OUT leftRoundBracket identifier rightRoundBracket | OUT leftRoundBracket constant rightRoundBracket

type : INT | CHAR | STRING

structstmt : ifstmt | whilestmt

ifstmt : IF condition cmpdstmt | IF condition cmpdstmt ELSE cmpdstmt

whilestmt : WHILE condition cmpdstmt

condition : expression relation expression | negation | condition and condition | condition or condition

negation : not expression

relation : less | lessOrEqual | equal | more | moreOrEqual | isequal | different

%%

void yyerror(char *s) {
    fprintf(stderr, "%s\n", s);
}

extern FILE *yyin;

int main(int argc, char **argv)
{
	if(argc>1) yyin :  fopen(argv[1],"r");
	if(argc>2 && !strcmp(argv[2],"-d")) yydebug = 1;
	if(!yyparse()) fprintf(stderr, "\tProgram is syntactically correct.\n");
}