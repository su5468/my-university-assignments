#include <stdio.h>
#include <stdlib.h>
#define MAX 100

typedef struct
{
    int coef;
    int exp;
} poly;

poly terms[MAX];
int avail = 0;

void zero(int *start, int *end)
{
    *start = avail;
    *end = avail;
}

int is_zero(int start, int end)
{
    if (start == end)
    {
        return 1;
    }
    return 0;
}

float coef(int start, int end, int exp)
{
    int i;
    for (i = start; i <= end; i++)
    {
        if (terms[i].exp == exp)
            return terms[i].coef;
    }
    return 0.0;
}

int lead(int start, int end)
{
    int i, cur = 0;
    for (i = start; i <= end; i++)
    {
        if (cur < terms[i].exp)
            cur = terms[i].exp;
    }
    return cur;
}

void attach(float coef, int exp)
{
    if (avail >= MAX)
    {
        printf("ERROR");
        return;
    }
    terms[avail].coef = coef;
    terms[avail++].exp = exp;
    return;
}

int cmp(int a, int b)
{
    return a == b ? 0 : (a > b ? 1 : -1);
}

void add(int starta, int enda, int startb, int endb, int *startd, int *endd)
{
    int coef; // 같은 차수의 항을 더할 때 계수가 0인지 확인하기 위해
    *startd = avail;
    while (starta <= enda && startb <= endb)
    {
        switch (cmp(terms[starta].exp, terms[startb].exp))
        {
        case -1: // b의 최고차항이 더 큰 경우
            attach(terms[startb].coef, terms[startb].exp);
            startb++;
            break;
        case 0: // 최고차항이 같은 경우
            coef = terms[starta].coef + terms[startb].coef;
            if (coef)
            {
                attach(coef, terms[starta].exp);
            }
            starta++;
            startb++;
            break;
        case 1: // a의 최고차항이 더 큰 경우
            attach(terms[starta].coef, terms[starta].exp);
            starta++;
            break;
        }
    }
    for (; starta <= enda; starta++)
        attach(terms[starta].coef, terms[starta].exp);
    for (; startb <= endb; startb++)
        attach(terms[startb].coef, terms[startb].exp);
    *endd = avail - 1;
}

int main(int argc, char const *argv[])
{
    int *ps1, *pe1, *ps2, *pe2, i = 0;
    int *ds, *de;
    ps1 = malloc(sizeof(int));
    pe1 = malloc(sizeof(int));
    ps2 = malloc(sizeof(int));
    pe2 = malloc(sizeof(int));
    ds = malloc(sizeof(int));
    de = malloc(sizeof(int));
    zero(ps1, pe1);
    attach(10, 2);
    attach(5, 1);
    attach(7, 0);
    *pe1 = avail - 1;

    zero(ps2, pe2);
    attach(3, 3);
    attach(1, 1);
    *pe2 = avail - 1;

    add(*ps1, *pe1, *ps2, *pe2, ds, de);

    free(ps1);
    free(ps2);
    free(pe1);
    free(pe2);
    free(ds);
    free(de);

    while (terms[i].exp || terms[i].coef)
    {
        printf("%d %d\n", terms[i].coef, terms[i].exp);
        i++;
    }

    return 0;
}
