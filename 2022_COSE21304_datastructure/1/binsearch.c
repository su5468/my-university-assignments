#include <stdio.h>
#define LEN 10
int bs(int n, int arr[], int l, int r)
{
    int m = (l + r) / 2;

    if (arr[m] > n)
        return bs(n, arr, l, m - 1);
    else if (arr[m] < n)
        return bs(n, arr, m + 1, r);
    return m;
}

int main(int argc, char const *argv[])
{
    int arr[LEN];
    int i, n;

    for (i = 0; i < LEN; i++)
        arr[i] = i;

    scanf("%d", &n);

    printf("%d\n", bs(n, arr, 0, LEN));

    return 0;
}
