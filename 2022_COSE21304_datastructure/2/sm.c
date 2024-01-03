#include <stdio.h>
#define MAX 100

typedef struct
{
    int row;
    int col;
    int val;
} elem;

void transpose(elem sm[], elem res[])
{
    int count[MAX] = {0}; // 각 col에 있는 원소 개수
    int position[MAX];    // 각 col의 시작 위치
    int i, j;             // for문 변수 및 결과 행렬에서 값을 채워야 하는 위치
    res[0].row = sm[0].col;
    res[0].col = sm[0].row; // 결과행렬 0번 인덱스의 메타데이터 확인
    res[0].val = sm[0].val;
    for (i = 1; i <= sm[0].val; i++)
    {
        count[sm[i].col]++; // 입력행렬 전체 순회하며 col별 개수 파악
    }
    position[0] = 1; // 0이 아니라 1인 이유: 0은 메타데이터 인덱스
    for (i = 1; i <= sm[0].col; i++)
    {
        position[i] = position[0] + count[i - 1]; // 각 col별 시작 위치 파악
    }

    for (i = 1; i <= sm[0].val; i++)
    {
        j = position[sm[i].col]++; // 먼저 해당 col의 시작 위치 할당하고 값을 증가
        res[j].row = sm[i].col;
        res[j].col = sm[i].row;
        res[j].val = sm[i].val;
    }
}

int main(int argc, char const *argv[])
{
    int i;         // 출력 위한 i 변수
    elem res[MAX]; // 결과 행렬
    elem sm[MAX] = {{3, 3, 2},
                    {1, 1, 6},
                    {2, 0, 4}}; // 3,3 크기, 1,1에 6 2,0에 4가 있는 희소행렬
    transpose(sm, res);

    for (i = 1; i <= sm[0].val; i++)
    {
        printf("%d%d%d\n", sm[i].row, sm[i].col, sm[i].val);
    }

    printf("\n");

    for (i = 1; i <= res[0].val; i++)
    {
        printf("%d%d%d\n", res[i].row, res[i].col, res[i].val);
    }
    return 0;
}
