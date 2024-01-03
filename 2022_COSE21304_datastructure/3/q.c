#include <stdio.h>
#include <stdlib.h>

typedef struct
{
    int val;
} elem;

elem *q;
int rear = -1;
int front = -1;
int cap = 1;

void copy(elem *start, elem *end, elem *dst)
{
    int i;
    for (i = 0; i < start - end; i++)
    {
        dst[i] = q[start - q + i];
    }
}

void full()
{
    elem *nq;
    nq = malloc(sizeof(*q) * 2 * cap);

    int start = (front + 1) % cap;
    if (start < 2)
        copy(q + start, q + start + cap - 1, nq);
    else
    {
        copy(q + start, q + cap, nq);
        copy(q, q + rear + 1, nq + cap - start);
    }
}

char is_full()
{
    return (rear + 1) % cap == front ? 1 : 0;
}

char is_empty()
{
    return front == rear ? 1 : 0;
}

void enq(elem e)
{
    if (is_full)
    {
        printf("QFull");
        full();
    }
    rear = (rear + 1) % cap;
    q[rear] = e;
}

elem deq()
{
    if (is_empty)
    {
        elem e = {0};
        printf("QEmptyError");
        return e;
    }
    front = (front + 1) % cap;
    return q[front];
}

int main(int argc, char const *argv[])
{
    q = (elem *)malloc(sizeof(*q));
    return 0;
}
