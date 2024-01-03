#include <stdio.h>
#include <string.h>
#define MAX 100

typedef struct tt tt;
typedef struct tt // ThreadedTree
{
    char lt;   // LeftThread
    tt *lc;    // LeftChild
    char data; //
    tt *rc;    // RightChild
    char rt;   // RightThread
};

tt tree[MAX];              // tree[0] is head node
tt *q[MAX];                // queue used to levelorder
int rear = -1, front = -1; // queue rear and front

void addq(tt *v) // enqueue
{
    if (rear == MAX - 1)
        return; // nothing happens if full
    q[++rear] = v;
}

tt *delq(void) // dequeue
{
    if (front == rear)
        return NULL; // returns NULL if empty
    return q[++front];
}

void inorder(tt *p) // ASS1. inorder without thread
{
    if (!p->lt) // if has left child then recurse
        inorder(p->lc);
    printf(" %c", p->data);
    if (!p->rt) // if has right child then recurse
        inorder(p->rc);
}

void levelorder(tt *p) // ASS2. levelorder using queue
{
    // queue is declared in global
    // empty tree will filtered in main func
    addq(p);
    for (;;)
    {
        p = delq(); // get node pointer from q
        if (p)
        {
            printf(" %c", p->data); // print it
            if (!p->lt)             // add children
                addq(p->lc);
            if (!p->rt)
                addq(p->rc);
        }
        else
            break;
    }
}

tt *insucc(tt *p) // finds next node
{
    tt *temp;
    temp = p->rc;            // temp is right child or (thread) parent
    if (!p->rt)              // has right child
        while (!temp->lt)    // that child has left child
            temp = temp->lc; // left terminal
    return temp;             // right child's left terminal
}

void inorder2(tt *p) // ASS3. inorder with thread(using insucc)
{
    tt *temp = p;
    for (;;)
    {
        temp = insucc(temp);
        if (temp == p) // if empty then break
            break;
        printf(" %c", temp->data);
    }
}

void rins(tt *parent, tt *child) // right insert to terminal
{
    // since it'll be used to make tree, assume that parent is always terminal
    child->rc = parent->rc;
    child->lc = parent;
    child->rt = child->lt = 1; // always 1 since parent is terminal
    parent->rc = child;
    parent->rt = 0;
}

void lins(tt *parent, tt *child) // left insert to terminal
{
    // since it'll be used to make tree, assume that parent is always terminal
    child->lc = parent->lc;
    child->rc = parent;
    child->rt = child->lt = 1; // always 1 since parent is terminal
    parent->lc = child;
    parent->lt = 0;
}

int main(int argc, char const *argv[])
{
    // set the tree
    char string[] = "/*+1462"; // can change input string
    int len = strlen(string);  // 7
    int i;

    if (!len)                // exception handling when string is ""
    {                        // strictly, "" is different from " ", but output is almost same
        strcpy(string, " "); // if need strict handling, just print three ""s using if-else
        len = 1;
    }

    tree[0].lt = tree[0].rt = 0;        // head node : thread false, both child self
    tree[0].lc = tree[0].rc = &tree[0]; // why rc is self? cuz tree[1] will copy that(look below)

    for (i = 1; i <= len; i++)
    {
        tree[i].data = string[i - 1];     // assign data
        if (i % 2)                        // i is odd
            rins(&tree[i / 2], &tree[i]); //
        else                              // i is even
            lins(&tree[i / 2], &tree[i]);
    }

    printf("<Threaded Binary Tree>\n\n");
    printf("1. Inorder traversal\n");
    inorder(&tree[1]);
    printf("\n\n2. Levelorder traversal\n");
    levelorder(&tree[1]);
    printf("\n\n3. Inorder successor\n");
    inorder2(&tree[0]);

    return 0;
}
