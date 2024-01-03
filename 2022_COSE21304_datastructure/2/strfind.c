#include <stdio.h>
#include <string.h>
#define MAX 100

void first(char *str, char *pat)
{
    char *res;
    if (res = strstr(str, pat))
    {
        printf("%s in %s\n", res, str);
    }
    else
    {
        printf("notfound\n");
    }
}

void second(char *str, char *pat)
{
    int i, j;

    for (i = 0; i < strlen(str); i++) // 원본문자열 순회
    {
        for (j = 0; j < strlen(pat); j++) // 패턴문자열 순회
        {
            if (str[i + j] != pat[j]) // 문자열이 다르면 벗어나서 다음으로
                break;
        }
        if (j >= strlen(pat)) // 벗어나지 않고 마쳤다면 완료
        {
            printf("%s in %s\n", str + i, str);
            return;
        }
    }

    printf("notfound");
}

void third(char *str, char *pat)
{
    int i, j;

    for (i = 0; i < strlen(str) - strlen(pat) + 1; i++)
    {
        for (j = 0; j < strlen(pat); j++)
        {
            if (str[i + j] != pat[j])
                break;
        }
        if (j >= strlen(pat))
        {
            printf("%s in %s\n", str + i, str);
            return;
        }
    }
    printf("notfound");
}

int main(int argc, char const *argv[])
{
    char str[MAX];
    char pat[MAX];
    strcpy(str, "hello spam");
    strcpy(pat, "sp");
    printf("%d\n", strlen(pat));

    first(str, pat);
    second(str, pat);
    third(str, pat);

    return 0;
}
