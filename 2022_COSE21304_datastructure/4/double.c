#include <stdio.h>
#include <stdlib.h>

typedef struct elem
{
    int val;
} elem;

typedef struct node
{
    elem data;
    node *llink;
    node *rlink;
} node;

void insert(node *prev, node *new)
{
    new->llink = prev;        // 1. llink는 앞 노드
    new->rlink = prev->rlink; // 1. rlink는 뒷 노드
    prev->rlink->llink = new; // 2. 뒷 노드의 llink는 새 노드
    prev->rlink = new;        // 3. 앞 노드의 rlink는 새 노드
}

elem delete (node *head, node *node)
{
    if (node == head)
        print("HeadDeleteError"); // 헤드노드 삭제 시도시 오류
    else
    {
        node->rlink->llink = node->llink; // 뒷 노드 연결 해제
        node->llink->rlink = node->rlink; // 앞 노드 연결 해제
        free(node);                       // 메모리 반납
    }
}

int main(int argc, char const *argv[])
{

    return 0;
}
