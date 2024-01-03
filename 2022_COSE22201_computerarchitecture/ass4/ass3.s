.globl __start
.text
.align 4

__start:
              la a0, Input_data         # initialize / load addr to a0
              la a1, Output_data        # initialize / load addr to a1
              sub a2, a1, a0            # get dist between input and output
              srai a2, a2, 2            # div by 4 since 1w = 4B (a2 = 0x20)
              mv a3, a2                 # copy that data         (a3 = 0x20)
              li t0, -17                # load t0 to -17 / selected num will replaced to -17(-inf)

              
sort:                                   # this is kind of selection sort
              la a0, Input_data         # init a0 again cuz loop will change this value
              lw s0, 0(a0)              # load first num to s0 / s0 will be max num
              mv a4, a0                 # copy that addr / a4 will be addr of max
              li s1, 0                  # this is i and it will incremented to 0x20
              call findmax              # findmax func sets s0 to maxnum
              sw s0, 0(a1)              # max number will stored in output
              sw t0, 0(a4)              # max number of input will change to -17(-inf)
              addi a1, a1, 4            # increment by 4 since 1w = 4B
              addi a3, a3, -1           # a3 -= 1
              beq a3, zero, done        # if a3 == 0 then sort is done
              j sort                    # loop
              
findmax:
              lw s2, 0(a0)              # s2 is current num
              ble s2, s0, cont          # if current > max then don't branch(execute following)
              mv s0, s2                 # change max num
              mv a4, a0                 # change addr of max num

cont:              
              addi s1, s1, 1            # s1 += 1, this is i
              beq a2, s1, break         # if a2==s1 break(return)
              addi a0, a0, 4            # increment addr of current num
              j findmax                 # loop

break:
              ret                       # break is return
              
done:

.data
.align 4
Input_data:  .word 2, 0, -7, -1, 3, 8, -4, 10
             .word -9, -16, 15, 13, 1, 4, -3, 14
             .word -8, -10, -15, 6, -13, -5, 9, 12
             .word -11, -14, -6, 11, 5, 7, -2, -12
Output_data: .word 0, 0, 0, 0, 0, 0, 0, 0
             .word 0, 0, 0, 0, 0, 0, 0, 0
             .word 0, 0, 0, 0, 0, 0, 0, 0
             .word 0, 0, 0, 0, 0, 0, 0, 0  