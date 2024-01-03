#include <stdio.h>
#include <stdlib.h>

typedef struct node
{
    int data;
    node *link
} node;

node *ptr = NULL;
node *avail = NULL;

node *get_node(void)
{
    node *ret;
    if (avail)
    {
        ret = avail;
        avail = avail->link;
    }
    else
        ret = (node *)malloc(sizeof(node));
    return ret;
}

void ret_node(node *p) // 반환할 노드 p를 가용공간의 앞에 붙임
{
    p->link = avail;
    avail = p;
}

void erase(node *p) // 원형 연결리스트 전체를 일괄 반납
{
    node *temp;
    if (p)
    {
        temp = p->link;  // 추후 avail이 가리킬 노드
        p->link = avail; // 고리를 끊고 avail에 연결
        avail = temp;    // temp로 리스트의 시작 위치 이동
        p = NULL;
    }
}

node *create(int a, int b)
{
    node *first, *second;
    first = get_node();
    second = get_node();

    first->data = a;
    second->data = b;

    first->link = second;
    second->link = NULL;

    ptr = first;

    return first;
}

void insert(node *first, int n) // first 노드의 뒤에 원소 삽입
{
    node *temp;
    temp = get_node();
    temp->data = n;
    if (first) // first가 NULL이라면 temp가 첫 노드가 된다
    {
        temp->link = first->link;
        first->link = temp;
    }
    else
    {
        temp->link = NULL;
        ptr = temp;
    }
}

void delete (node *first, node *temp)
{              // first는 변수 이름이 이래서 그렇지 그냥 이전 노드임
    if (first) // first가 있다=이전 노드가 있다
        first->link = temp->link;
    else                 // 아니다=첫 노드를 삭제한다
        ptr = ptr->link; // temp->link도 가능
    ret_node(temp);
}

void print_node(node *ptr)
{
    for (; ptr; ptr = ptr->link)
        printf("%d\n", ptr->data);
}

node *concate(node *p1, node *p2)
{
    node *temp;
    if (!p1) // 둘 중 하나가 빈 리스트면 나머지 반환
        return p2;
    if (!p2)
        return p1;
    for (temp = p1; temp->link; temp = temp->link)
        ;            // p1을 NULL이 나올 때까지 순회
    temp->link = p2; // p1의 끝과 p2의 시작 연결
    return p1;
}

node *inverse(node *lead)
{
    node *middle, *trail;
    middle = NULL; // 처음에 NULL로 몸통 초기화
    while (lead)
    {
        trail = middle; // 꼬리, 몸통, 머리 순으로 전진
        middle = lead;
        lead = lead->link;
        middle->link = trail; // 몸통에서 꼬리로 연결
    }
    return middle; // 머리가 NULL이므로 몸통이 마지막 노드가 됨
}

node *inverse2(node *head)
{
    node *prev, *curr, *next;
    curr = head;        // 시작지점에 몸통 위치
    next = prev = NULL; // 나머지는 다 NULL

    while (curr)
    {
        next = curr->link; // next를 전진
        curr->link = prev; // 포인터의 방향을 전환
        prev = curr;       // prev 전진
        curr = next;       // curr 전진
    }
    head = prev; // 시작 지점을 prev로 변경
    return head; // curr=NULL이므로 prev가 마지막 노드
}

int main(int argc, char const *argv[])
{
    ptr = get_node();
    ptr = create(10, 20);

    return 0;
}
