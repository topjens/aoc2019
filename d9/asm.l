%{
#include <stdio.h>
#include <stdlib.h>

#define YY_DECL int yylex()

#include "asm.tab.h"
%}

%%

[ \t] ;
[\n]    return NEWLINE;
,       return ',';
\(-?[0-9]*\) {yytext[0] = ' '; yytext[yyleng] = ' '; yylval.i = atoi(yytext); return RINT;}
\[-?[0-9]*\] {yytext[0] = ' '; yytext[yyleng] = ' '; yylval.i = atoi(yytext); return AINT;}
-?[0-9]* {yylval.i = atoi(yytext); return INT;}
add     return ADD;
mul     return MUL;
in      return IN;
out     return OUT;
jt      return JT;
jf      return JF;
less    return LESS;
equ     return EQU;
adb     return ADB;
hlt     return HLT;

%%

int main()
	{
		yyin = stdin;

		do {
			yyparse();
		} while(!feof(yyin));

		return 0;
	}

void yyerror(const char *s)
	{
		fprintf(stderr, "Error reading file: %s\n", s);
		exit(EXIT_FAILURE);
	}
