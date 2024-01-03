# 1 "SevenSeg.c"
# 1 "<built-in>"
# 1 "<command-line>"
# 1 "SevenSeg.c"
# 1 "SevenSeg.h" 1
# 2 "SevenSeg.c" 2



int SevenSeg()
{
    unsigned int *seg0_addr = (unsigned int *)0xFFFF2000 + 3;
    unsigned int *seg1_addr = (unsigned int *)0xFFFF2000 + 4;
    unsigned int *Output_data = (unsigned int *)0x00000080;
    int i;
    int result = -16;
    char flag = 1;

    for (i = 0; i < 32; i++)
    {
        if (*Output_data != result)
            flag = 0;
        Output_data--;
        result++;
    }

    if (flag)
        *seg0_addr = 0x79;
    else
        *seg1_addr = 0x24;

    while (1)
        ;

    return 0;
}
