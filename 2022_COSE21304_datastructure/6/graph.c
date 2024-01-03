#include <stdio.h>
#include <stdlib.h>
#define MAX 100

typedef struct q q;
typedef struct q
{
    int v;
    q *e;
};

q *graph[MAX];
char visited[MAX];

void addq(q *front, q *rear, int v)
{
    /* ycgh */
}

int delq(q *front)
{
    /* ycgh */
}

void bfs(int v)
{
    q *w, *front, *rear;
    front = rear = NULL;
    printf("%d", v);
    visited[v] = 1;
    addq(&front, &rear, v);
    while (front)
    {
        v = delq(&front);
        for (w = graph[v], w; w = w->e;)
        {
            if (!visited[w->v])
            {
                printf("%d", w->v);
                addq(&front, &rear, w->v);
                visited[w->v] = 1;
            }
        }
    }
}

int main(int argc, char const *argv[])
{

    return 0;
}
