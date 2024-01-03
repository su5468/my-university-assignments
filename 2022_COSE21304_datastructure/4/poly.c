#include <stdio.h>
#include <stdlib.h>

typedef struct poly
{
    int exp;
    float coef;
    poly *link;
} poly;

void attach(float coef, int exp, poly *ptr) // rear에 항 추가
{
    poly *temp = (poly *)malloc(sizeof(poly));

    temp->coef = coef;
    temp->exp = exp;

    ptr->link = temp; // rear 뒤에 항 연결
    ptr = temp;       // rear 이동
}

void erase(poly *ptr)
{
    poly *temp;

    while (ptr)
    {
        temp = ptr;
        ptr = ptr->link;
        free(temp);
    }
}

poly *add(poly *a, poly *b)
{
    poly *start, *c, *last;
    int done = 0, sum;
    start = a;
    c = (poly *)malloc(sizeof(poly));
    c->exp = -1;
    last = c;
    a = a->link; // 헤드 노드 건너뛰기
    b = b->link; // 헤드 노드 건너뛰기

    do
    {
        switch (a->exp > b->exp ? 1 : (a->exp < b->exp ? -1 : 0))
        {
        case -1: // a가 b보다 지수가 작음
            attach(b->coef, b->exp, last);
            b = b->link;
            break;
        case 0:             // a와 b의 지수 동일
            if (start == a) // 헤드 노드를 건너뛰었는데 값이 헤드와 같은 것이므로 둘 다 빈 식
                done = 1;
            else
            {
                sum = a->coef + b->coef;
                if (sum)                       // 두 계수의 합이 0이 아니면
                    attach(sum, a->exp, last); // 추가하고 진행
                a = a->link;
                b = b->link;
            }
            break;
        case 1: // a가 b보다 지수가 큼
            attach(a->coef, a->exp, last);
            a = a->link;
        }
    } while (!done);
    last->link = c; // 계산이 완료된 식을 원형 리스트로 만듦
    return c;
}

int main(int argc, char const *argv[])
{
    poly *head = (poly *)malloc(sizeof(poly));
    head->exp = -1;
    head->link = head;

    return 0;
}
