#include <stdio.h>
#include <stdlib.h>

typedef struct node
{
    int data;
    node *link;
} node;

void insert(node *last, node *node)
{
    if (!last) // 리스트가 비었다면,
    {
        last = node;       // 라스트는 자신
        node->link = node; // 자기순환
    }
    else // 비지 않았다면 링크 생성
    {
        node->link = last->link;
        last->link = node;
    }
}

int delete (node *node)
{
    /* single에 있는 함수들 참조 */
}

int length(node *last)
{
    node *temp; // 순회용 임시변수
    int c = 0;  // 카운트
    if (last)   // 비어있지 않다면
    {
        temp = last; // last 위치부터
        do
        {
            c++;
            temp = temp->link;  // 순회
        } while (temp != last); // do while인 이유는 처음에 temp==last이라
    }
    return c; // 개수리턴, 비었으면 0임
}

int main(int argc, char const *argv[])
{
    /* code */
    return 0;
}
