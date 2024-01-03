#include <stdio.h>

int gcd(int a, int b)
{
    if (b == 0)
        return a;
    else if (a == 0)
        return b;
    return gcd(b, a % b);
}

int main(int argc, char const *argv[])
{
    int a, b;
    scanf("%d %d", &a, &b);

    printf("%d", gcd(a, b));
    return 0;
}
