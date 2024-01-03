#include <stdio.h>
#include <stdlib.h>
#define MAX 6

typedef struct node node;
typedef struct node
{
    int v;   // vertex
    node *e; // edge
};

typedef struct
{
    int c;   // count
    node *e; // edge
} head;

head *graph[MAX];

void *add(int p, int v) // p: parent num, v: vertex num
{                       // add edge from p to v, reversed order
    node *temp;
    temp = (node *)malloc(sizeof(node));
    temp->v = v;
    temp->e = graph[p]->e;
    graph[p]->e = temp;
    graph[v]->c++;
}

void topsort(head *graph[], int n) // ASS. topological order
{
    int i, j, k;
    int top = -1;
    node *p;

    for (i = 0; i < n; i++) // push to stack
    {
        if (!graph[i]->c)
        {
            graph[i]->c = top;
            top = i;
        }
    }
    for (i = 0; i < n; i++)
    {
        if (top == -1) // error handling (unnecessary)
        {
            printf("\n Network has a cycle.\n");
            exit(1);
        }
        j = top; // pop from stack
        top = graph[top]->c;

        printf("%d, ", j);

        for (p = graph[j]->e; p; p = p->e)
        {
            k = p->v;
            graph[k]->c--;
            if (!graph[k]->c) // push to stack
            {
                graph[k]->c = top;
                top = k;
            }
        }
    }
}

int main(int argc, char const *argv[])
{
    int i;

    for (i = 0; i < MAX; i++) // allocate memory and initialize
    {
        graph[i] = (head *)malloc(sizeof(head));
        graph[i]->c = 0;
        graph[i]->e = NULL;
    }

    add(3, 5); // add edges, reversed order
    add(3, 4);
    add(2, 5);
    add(2, 4);
    add(1, 4);
    add(0, 3);
    add(0, 2);
    add(0, 1);

    topsort(graph, 6);
    printf("\b\b "); // delete last ',' char for aesthetical purpose (unnecessary)
    return 0;
}
