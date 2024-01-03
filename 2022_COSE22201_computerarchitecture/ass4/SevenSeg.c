#include "SevenSeg.h"
#define OUTPUT 0x00000080

int SevenSeg()
{
    unsigned int *seg0_addr = (unsigned int *)SevenSeg0;
    unsigned int *seg1_addr = (unsigned int *)SevenSeg1;
    unsigned int *Output_data = (unsigned int *)OUTPUT;
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
        *seg0_addr = SEG_1;
    else
        *seg1_addr = SEG_2;

    while (1)
        ;

    return 0;
}
