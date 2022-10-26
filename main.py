class CMPE443:
    "This is the doc"

    def __init__(self) -> None:
        self.GPIO_PORTS = ["A", "B", "C", "D", "E", "F", "G", "H"]
        self.valid_pins = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        self._dict_pheripheral_clock_en = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7}
        self._dict_address_gpio_moders = {"A": 0x42020000, "B": 0x42020400, "C": 0x42020800, "D": 0x42020C00, "E": 0x42021000, "F": 0x42021400, "G": 0x42021800, "H": 0x42021C00}
        self.moders=[]
        self.odrs=[]
        self.defines=[]
        self.globals=[]
        self.main=[]
        self.bus=""
    
    def _enable_bus(self,port):
        print("Register of the enabler bus is RCC_AHB2ENR")
        RCC_AHB2ENR = "0x4002104C"
        self.bus="RCC_AHB2ENR"
        strr=f"#define RCC_AHB2ENR *((volatile uint32_t *) {RCC_AHB2ENR})"
        if strr not in self.defines:
            self.defines.append(strr)
        self.main.append(f"{self.bus} |= (1<<{str(self._dict_pheripheral_clock_en[port])});")
        self.main.append("for(index=0;index<wait_millisecond*666;index++);")
        self.main.append("wait_counter = wait_counter + 1;")

    def _disable_bus(self,port):
        self.main.append(f"{self.bus} &= ~(1<<{str(self._dict_pheripheral_clock_en[port])});")
    
    def _set_moder(self,port,pin,mode):
        print("Input mode=00, output mode=01 , alternate function mode=10")
        GPIOx_MODER=str(hex(self._dict_address_gpio_moders[port]))
        self.moders.append({f"GPIO{port}":GPIOx_MODER})
        strr=f"#define GPIO{port}_MODER *((volatile uint32_t *) {str(GPIOx_MODER)})"
        if strr not in self.defines:
            self.defines.append(strr)
        number = int(pin)*2+1 
        function_mode=""
        function_mode1=""
        if mode == "01":
            function_mode = f"GPIO{port}_MODER &= ~(1 << {str(number)});"         # to do 0
            function_mode1 = f"GPIO{port}_MODER |= (1 << {str(number-1)});" # to do 1
        if mode == "11":
            function_mode = f"GPIO{port}_MODER |= (1 << {str(number-1)});"
            function_mode1 = f"GPIO{port}_MODER |= (1 << {str(number)});"
        if mode == "00":
            function_mode = f"GPIO{port}_MODER &= ~(1 << {str(number)});"
            function_mode1 = f"GPIO{port}_MODER &= ~(1 << {str(number-1)});"
        if mode == "10":
            function_mode = f"GPIO{port}_MODER |= (1 << {str(number)});"
            function_mode1 = f"GPIO{port}_MODER &= ~(1 << {str(number-1)});"
        self.main.append(function_mode)
        self.main.append(function_mode1)

    def _set_odr(self,port,pin,open_close:int):
        GPIOx_ODR = str(hex(self._dict_address_gpio_moders[port] + 0x14))  
        self.odrs.append({f"GPIO{port}":GPIOx_ODR})
        strr=f"#define GPIO{port}_ODR *((volatile uint32_t *) {str(GPIOx_ODR)})"
        if strr not in self.defines:
            self.defines.append(strr)
        if open_close == 1:
            self.main.append(f"GPIO{port}_ODR |= (1 << {str(pin)});")
        if open_close == 0:
            self.main.append(f"GPIO{port}_ODR &= ~(1 << {str(pin)});")
    
    def _set_idr(self,port,pin,open_close:int):
        GPIOx_IDR = str(hex(self._dict_address_gpio_moders[port] + 0x10))  
        self.odrs.append({f"GPIO{port}":GPIOx_IDR})
        strr=f"#define GPIO{port}_IDR *((volatile uint32_t *) {str(GPIOx_IDR)})"
        if strr not in self.defines:
            self.defines.append(strr)
        if open_close == 1:
            self.main.append(f"GPIO{port}_IDR |= (1 << {str(pin)});")
        if open_close == 0:
            self.main.append(f"GPIO{port}_IDR &= ~(1 << {str(pin)});")

    def blink_pin(self,port: str = "PA", pin: int = 0):
        if pin not in self.valid_pins:
            raise("Invalid pin")
        if port not in self.GPIO_PORTS:
            raise("Invalid port")
        if port in self.GPIO_PORTS:
            self.defines.append("#include <stdint.h>")
            self.globals.append("uint32_t wait_millisecond = 1000;")
            self.globals.append("uint32_t wait_counter = 0;")
            self.main.append("int main(void)  {")
            self.main.append("//This is the blinking led code.")
            self.main.append("volatile int index;")
            self._enable_bus(port)
            self._set_moder(port,pin,"01")
            self._set_odr(port,pin,1)
            #self.GPIOx_IDR = str(hex(self._dict_address_gpio_moders[port] + 0x10))
            self.main.append("while(1) {")
            self._set_odr(port,pin,1)
            self.main.append("for(index=0;index<wait_millisecond*666;index++);")
            self._set_odr(port,pin,0)
            self.main.append("for(index=0;index<wait_millisecond*666;index++);")
            self.main.append("}")
            self.main.append("return 0;")
            self.main.append("}")
            self.write()
    
    def shine_when_pressed(self,o_port,o_pin,i_port,i_pin):
        if o_port in self.GPIO_PORTS and i_port in self.GPIO_PORTS and i_pin in self.valid_pins and o_pin in self.valid_pins:
            self.defines.append("#include <stdint.h>")
            self.globals.append("uint32_t wait_millisecond = 1000;")
            self.globals.append("uint32_t wait_counter = 0;")
            self.main.append("int main(void)  {")
            
            self.main.append("volatile int index;")
            self._enable_bus(o_port)
            self._enable_bus(i_port)
            self._set_moder(i_port,i_pin,"00")
            self._set_moder(o_port,o_pin,"01")
            self._set_odr(o_port,o_pin,-1)
            self._set_idr(i_port,i_pin,-1)   
            self.main.append("while(1) {")
            self.main.append(f"if(GPIO{i_port}_IDR>>{str(i_pin)}== 1) {'{'}")
            self.main.append("//When pressed")
            self._set_odr(o_port,o_pin,1)
            self.main.append("}else{") 
            self.main.append("//When not pressed")
            self._set_odr(o_port,o_pin,0)
            self.main.append("}")
            self.main.append("}")
            self.main.append("return 0;")
            self.main.append("}")

            self.write()

    def write(self):
        with open("main.c", "w") as f:
            for i in self.defines:
                f.write(i)
                f.write("\n")
            for i in self.globals:
                f.write(i)
                f.write("\n")
            for i in range(len(self.main)):
                if i==0:
                    f.write(self.main[i]+"\n")
                elif i==len(self.main)-1:
                    f.write(self.main[i])
                else:
                    f.write("\t"+self.main[i]+"\n")

if __name__ == "__main__":
    # RED   LED    PA9
    # GREEN LED    PC7
    # BLUE  LED    PB7
    # USER  BUTTON PC13

    cmpe443 = CMPE443()
    cmpe443.shine_when_pressed("A", 9, "C", 13)
