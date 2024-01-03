#include <stdio.h>
#define MAX 100

typedef enum
{
    lp,
    rp,
    pl,
    mi,
    ti,
    di,
    mo,
    eo,
    op
} prec;

prec stack[MAX];
char expr[MAX];

prec pop(int *top)
{
    return stack[(*top)--];
}

void push(prec p, int *top)
{
    stack[++(*top)] = p;
    return;
}

//                 (,  ),  +,  -,  *,  /,  %, eos
static int isp[] = {0, 19, 12, 12, 13, 13, 13, 0};  // instack
static int icp[] = {20, 19, 12, 12, 13, 13, 13, 0}; // incoming

prec get_tok(char *sym, int *n)
{
    *sym = expr[(*n)++];
    printf("hi : %c\n\n", *sym);
    switch (*sym)
    {
    case '(':
        return lp;
    case ')':
        return rp;
    case '+':
        return pl;
    case '-':
        return mi;
    case '/':
        return di;
    case '*':
        return ti;
    case '%':
        return mo;
    case '\0':
        return eo;
    default:
        return op;
    }
}

char ret_tok(prec tok)
{
    switch (tok)
    {
    case pl:
        return '+';
    case mi:
        return '-';
    case di:
        return '/';
    case ti:
        return '*';
    case mo:
        return '%';
    case eo:
        return '\0';
    }
}

void convert(void)
{
    char sym;
    prec tok;
    int top = 0, n = 0; // 스택 top에 eos가 있으므로 top = 0
    stack[0] = eo;

    printf("%s\n", expr);

    for (tok = get_tok(&sym, &n); tok != eo; tok = get_tok(&sym, &n))
    {
        if (tok == op) // 피연산자면 그냥 출력
            printf("%c", sym);
        else if (tok = rp) // 우측 괄호면 스택 꺼내면서 괄호는 빼고 다 출력
        {
            while (stack[top] != lp)
                printf("%c", ret_tok(pop(&top)));
            pop(&top);
        }
        else // 우선순위 비교해서 pop하고 push
        {
            while (isp[stack[top]] >= icp[tok])
                printf("%c", ret_tok(pop(&top)));
            push(tok, &top);
        }
    }
    while ((tok = pop(&top)) != eo)
        printf("%c", ret_tok(tok));
    printf("\n");
}

int main(int argc, char const *argv[])
{
    scanf("%s", expr);

    convert();
    return 0;
}
