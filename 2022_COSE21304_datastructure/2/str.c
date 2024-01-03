#include <stdio.h>
#include <string.h>
#define MAX 100

void insertion(char *s1, char *s2, int pos)
{
    char temp[MAX];         // 임시변수
    strncpy(temp, s1, pos); // pos 위치까지의 문자열 복사
    strcat(temp, s2);       // 삽입할 문자열 복사
    strcat(temp, s1 + pos); // pos 뒤의 문자열 복사

    strcpy(s1, temp); // s1으로 문자열 옮김
}

int main(int argc, char const *argv[])
{
    // char string1[MAX], string2[MAX];
    // char *s1 = string1, *s2 = string2;
    // strcpy(string1, "amobile");
    // strcpy(string2, "uto");
    char s1[MAX] = "amobile";
    char s2[MAX] = "uto";

    insertion(s1, s2, 1);
    printf("%s", s1);
    return 0;
}
