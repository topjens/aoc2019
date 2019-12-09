#include <stdio.h>

struct password {
	char digit0;
	char digit1;
	char digit2;
	char digit3;
	char digit4;
	char digit5;
};

int compare(int number, struct password *p)
{
	int pass = p->digit0 * 100000 + \
		p->digit1 * 10000 + \
		p->digit2 * 1000 + \
		p->digit3 * 100 + \
		p->digit4 * 10 + \
		p->digit5;

	return (pass == number);
}

void increase(struct password *p)
{
	p->digit5++;
	if(p->digit5 > 9) {
		p->digit5 = 0;
		p->digit4++;
	}
	if(p->digit4 > 9) {
		p->digit4 = 0;
		p->digit3++;
	}
	if(p->digit3 > 9) {
		p->digit3 = 0;
		p->digit2++;
	}
	if(p->digit2 > 9) {
		p->digit2 = 0;
		p->digit1++;
	}
	if(p->digit1 > 9) {
		p->digit1 = 0;
		p->digit0++;
	}
}

int adj_same(struct password *p)
{
	if(p->digit0 == p->digit1 && p->digit1 != p->digit2)
		return 1;
	if(p->digit1 == p->digit2 && p->digit0 != p->digit1 && p->digit2 != p->digit3)
		return 1;
	if(p->digit2 == p->digit3 && p->digit1 != p->digit2 && p->digit3 != p->digit4)
		return 1;
	if(p->digit3 == p->digit4 && p->digit2 != p->digit3 && p->digit4 != p->digit5)
		return 1;
	if(p->digit4 == p->digit5 && p->digit3 != p->digit4)
		return 1;
	return 0;
}

int increasing(struct password *p)
{
	if(p->digit0 > p->digit1)
		return 0;
	if(p->digit1 > p->digit2)
		return 0;
	if(p->digit2 > p->digit3)
		return 0;
	if(p->digit3 > p->digit4)
		return 0;
	if(p->digit4 > p->digit5)
		return 0;
}

int get_number(struct password *p)
{
	int pass = p->digit0 * 100000 +					\
		p->digit1 * 10000 + \
		p->digit2 * 1000 + \
		p->digit3 * 100 + \
		p->digit4 * 10 + \
		p->digit5;

	return pass;
}

int main(int argc, char *argv[])
{
	struct password p = {2, 4, 6, 5, 1, 5};

	while(!compare(739105, &p)) {
		/* printf("t: %d\n", get_number(&p)); */
		increase(&p);
		if(!adj_same(&p))
			continue;
		if(!increasing(&p))
			continue;
		printf("%d\n", get_number(&p));
	}
}
