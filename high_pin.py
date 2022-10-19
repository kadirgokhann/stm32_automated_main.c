class CMPE443:
    "This is the doc"

    def __init__(self, port: str = "PA", pin: int = 0, mode: str = "01") -> None:
        self.GPIO_PORTS = ["PA", "PB", "PC", "PD", "PE", "PF", "PG", "PH"]
        self.valid_pins = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        self._dict_pheripheral_clock_en = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7}
        self._dict_address_gpio_moders = {"A": 0x42020000, "B": 0x42020400, "C": 0x42020800, "D": 0x42020C00, "E": 0x42021000, "F": 0x42021400, "G": 0x42021800, "H": 0x42021C00}
        if pin not in self.valid_pins:
            print("Invalid pin")
            exit(1)
        if port in self.GPIO_PORTS:
            self.bus = "RCC_AHB2ENR"
            self.add_of_bus = "0x4002104C"
            self.GPIOx_MODER = str(hex(self._dict_address_gpio_moders[port[1]]))
            self.GPIOx_ODR = str(hex(self._dict_address_gpio_moders[port[1]] + 0x14))
            if mode == "01":
                number = int(pin)*2+1
                self._function_mode = f"GPIOx_MODER &= ~(1 << {str(number)});"
            if mode == "11":
                self._function_mode = ""
            if mode == "00":
                self._function_mode = f"GPIOx_MODER &= ~(1 << {str(number)});"
                self._function_mode = f"GPIOx_MODER &= ~(1 << {str(number-1)});"
            if mode == "10":
                self._function_mode = f"GPIOx_MODER &= ~(1 << {str(number-1)});"
            self.code = f'''
#define {self.bus} *((volatile uint32_t *) {self.add_of_bus})
#define GPIOx_MODER *((volatile uint32_t *) {str(self.GPIOx_MODER)})
#define GPIOx_ODR *((volatile uint32_t *) {str(self.GPIOx_ODR)})
#include <stdint.h>
uint32_t wait_millisecond = 1000;
uint32_t wait_counter = 0;
int main(void)  {"{"}
    volatile int index;
    {self.bus} |= {"(1<<"+str(self._dict_pheripheral_clock_en[port[1]])+")"};
    for(index=0;index<wait_millisecond*666;index++);
    wait_counter = wait_counter + 1;
    {self._function_mode}
    GPIOx_ODR |= (1 << {str(pin)});
    for(index=0;index<wait_millisecond*666;index++);
    wait_counter = wait_counter + 1;
    GPIOx_ODR &= ~(1 << {str(pin)});
    for(index=0;index<wait_millisecond*666;index++);
    wait_counter = wait_counter + 1;
    return 0;
{"}"}
                    '''
        else:
            print("Invalid port or not added port.")
            exit(1)

    def write(self):
        with open("main.c", "w") as f:
            f.write(self.code)


if __name__ == "__main__":
    cmpe443 = CMPE443("PE", 14, "01")
    cmpe443.write()
