#include <stdio.h>

void towers(int n, char src, char dst, char aux)
{
    static int step = 0;

    printf("%d | %c %c %c\n", n, src, dst, aux);

    if (n == 1)
        printf("Step %d: %c to %c\n", ++step, src, dst);
    else
    {
        towers(n - 1, src, aux, dst);
        printf("Step %d: %c to %c\n", ++step, src, dst);
        towers(n - 1, aux, dst, src);
    }
    return;
}

int main(int argc, char const *argv[])
{
    int n;

    scanf("%d", &n);

    towers(n, 'A', 'C', 'B');

    return 0;
}
