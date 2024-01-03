#include <stdio.h>

int fact(int a)
{
    if (a == 0)
        return 1;
    else
    {
        return a * fact(a - 1);
    }
}

int main(int argc, char const *argv[])
{
    int n;
    scanf("%d", &n);

    printf("%d", fact(n));
    return 0;
}