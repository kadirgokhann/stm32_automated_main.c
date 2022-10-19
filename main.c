
#define RCC_AHB2ENR *((volatile uint32_t *) 0x4002104C)
#define GPIOx_MODER *((volatile uint32_t *) 0x42021000)
#define GPIOx_ODR *((volatile uint32_t *) 0x42021014)
#include <stdint.h>
uint32_t wait_millisecond = 1000;
uint32_t wait_counter = 0;
int main(void)  {
    volatile int index;
    RCC_AHB2ENR |= (1<<4);
    for(index=0;index<wait_millisecond*666;index++);
    wait_counter = wait_counter + 1;
    GPIOx_MODER &= ~(1 << 29);
    GPIOx_ODR |= (1 << 14);
    for(index=0;index<wait_millisecond*666;index++);
    wait_counter = wait_counter + 1;
    GPIOx_ODR &= ~(1 << 14);
    for(index=0;index<wait_millisecond*666;index++);
    wait_counter = wait_counter + 1;
    return 0;
}
                    