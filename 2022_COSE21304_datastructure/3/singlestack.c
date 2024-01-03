#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct
{
    int val;
} elem;
elem *stack;
int top = -1;

void full(int cap)
{
    realloc(stack, 2 * cap * sizeof(*stack));
    cap *= 2;
}

char is_full(int cap)
{
    return top == cap ? 1 : 0;
}

char is_empty(void)
{
    return top == -1 ? 1 : 0;
}

void push(int cap, elem item)
{
    if (is_full(cap))
        full(cap);
    stack[++top] = item;
}

elem pop(void)
{
    if (is_empty())
    {
        elem n = {0};
        printf("StackEmptyError");
        return n;
    }
    return stack[top--];
}

char checksym(char sym) // 여는 괄호와 닫는 괄호 비교
{
    char val = pop().val;
    switch (sym)
    {
    case ')':
        if (val == '(')
            return 1;
        break;
    case '}':
        if (val == '{')
            return 1;
        break;
    case ']':
        if (val == '[')
            return 1;
        break;
    }
    return 0;
}

char checkparen(char str[], int cap)
{
    int ret = 1, i;
    char sym;
    elem e;
    for (i = 0; i < strlen(str); i++) // 문자열 전체 순회
    {
        sym = str[i];
        switch (sym)
        {
        case '(':
        case '{':
        case '[':
            e.val = sym;
            push(cap, e);
            break;

        case ')':
        case '}':
        case ']':
            if (is_empty())
                ret = 0;
            else
            {
                ret = checksym(sym);
            }
            break;
        }
    }
    if (!is_empty())
        ret = 0;
    return ret;
}

int main(int argc, char const *argv[])
{
    stack = (elem *)malloc(sizeof(*stack));
    int cap = 1;

    char exp[100];

    printf("%d", sizeof(elem));

    scanf("%s", exp);

    printf("%d", checkparen(exp, cap));

    return 0;
}
