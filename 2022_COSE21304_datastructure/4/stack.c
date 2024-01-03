#include <stdio.h>
#include <stdlib.h>
#define MAX 10 // 다중 스택 개수

typedef struct elem // 스택에 들어갈 원소
{
    int val;
} elem;

typedef struct stack // 이름은 stack이지만 1칸짜리 노드임
{
    elem item;
    stack *link;
} stack;

stack *top[MAX];

void push(int i, elem item)
{
    stack *temp = (stack *)malloc(sizeof(stack));
    temp->item = item;
    temp->link = top[i]; // 탑 위에 새 원소
    top[i] = temp;       // 탑 위치를 올림
}

elem pop(int i)
{
    elem item; // 반환할 값
    stack *temp = top[i];
    // if (!temp)
    //     return stack_empty;
    item = temp->item;
    top[i] = temp->link;
    free(temp);
    return item;
}

int main(int argc, char const *argv[])
{
    /* code */
    return 0;
}
