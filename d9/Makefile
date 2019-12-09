all: asm

asm.tab.c asm.tab.h: asm.y
	bison -d asm.y

lex.yy.c: asm.l asm.tab.h
	flex asm.l

asm: lex.yy.c asm.tab.c asm.tab.h
	gcc -o asm asm.tab.c lex.yy.c -lfl

clean:
	rm -f asm asm.tab.c lex.yy.c asm.tab.h
