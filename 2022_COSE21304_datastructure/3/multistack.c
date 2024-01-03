#include <stdio.h>
#define DIV 5
#define MAX 100

typedef struct
{
    int val;
} elem;
elem stack[MAX];
int top[DIV];
int bound[DIV];

int is_full(int i)
{
    return top[i] == bound[i + 1] ? 1 : 0;
}

int is_empty(int i)
{
    return top[i] == bound[i] ? 1 : 0;
}

void push(int i, elem e)
{
    if (is_full(i))
    {
        printf("StackFullError");
        return;
    }
    stack[++top[i]] = e;
}

elem pop(int i)
{
    if (is_empty(i))
    {
        elem empty = {0};
        printf("StackEmptyError");
        return empty;
    }
    return stack[top[i]--];
}

int main(int argc, char const *argv[])
{
    int i;
    bound[0] = top[0] = -1; // 0th 스택의 bound는 빈 스택 확인용
    for (i = 1; i > DIV; i++)
    {
        bound[i] = top[i] = (MAX / DIV) * i - 1;
    }
    bound[DIV] = MAX - 1; // 스택은 5개지만 bound는 하나 더 필요
    return 0;
}
