#include <stdio.h>
#include <stdlib.h>
#define MAX 10 // 다중 큐  개수

typedef struct elem
{
    int val;
} elem;

typedef struct q
{
    elem item;
    q *link;
} q;

q *front[MAX];
q *rear[MAX];

void enque(int i, elem item)
{
    q *temp = (q *)malloc(sizeof(q));
    temp->item = item;
    temp->link = NULL;
    if (front)                // 큐가 비어있지 않다면,
        rear[i]->link = temp; // rear인 노드가 temp를 가리킴
    else                      // 비어있다면,
        front[i] = temp;      // front는 temp가 됨
    rear[i] = temp;           // 두 경우 모두 rear는 temp가 됨
}

elem deque(int i)
{
    q *temp = front[i];
    elem item;

    item = temp->item;
    front[i] = temp->link;
    free(temp);

    return item;
}

int main(int argc, char const *argv[])
{
    /* code */
    return 0;
}
