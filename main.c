#include <stdint.h>
#define RCC_AHB2ENR *((volatile uint32_t *) 0x4002104C)
#define GPIOC_MODER *((volatile uint32_t *) 0x42020800)
#define GPIOA_MODER *((volatile uint32_t *) 0x42020000)
#define GPIOA_ODR *((volatile uint32_t *) 0x42020014)
#define GPIOC_IDR *((volatile uint32_t *) 0x42020810)
uint32_t wait_millisecond = 1000;
uint32_t wait_counter = 0;
int main(void)  {
	volatile int index;
	RCC_AHB2ENR |= (1<<0);
	for(index=0;index<wait_millisecond*666;index++);
	wait_counter = wait_counter + 1;
	RCC_AHB2ENR |= (1<<2);
	for(index=0;index<wait_millisecond*666;index++);
	wait_counter = wait_counter + 1;
	GPIOC_MODER &= ~(1 << 27);
	GPIOC_MODER &= ~(1 << 26);
	GPIOA_MODER &= ~(1 << 19);
	GPIOA_MODER |= (1 << 18);
	while(1) {
	if(GPIOC_IDR>>13== 1) {
	//When pressed
	GPIOA_ODR |= (1 << 9);
	}else{
	//When not pressed
	GPIOA_ODR &= ~(1 << 9);
	}
	}
	return 0;
}