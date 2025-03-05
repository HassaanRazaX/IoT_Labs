# LAB3 - MicroPython Home Tasks

## Home Tasks

###  Task 1: Displaying Temperature & Humidity on OLED
###  Task 1.1
In this task, I connected the DHT11 sensor with the ESP and showed temperature and humidity readings on the OLED using Wokwi. It was cool seeing live data pop up on the small screen. I just had to keep refreshing the readings every second, and sometimes it took a sec to load, but it worked fine overall.

###  Task 1.2: Try adding emojis
In this task I tried to add emojis but OLED does not support the emojis to display even though i tried to use a framebuf library to show emoji as bitmap but it did'nt work.
###  Task 1.3: Try adding emojis
I blowed towards DHT11 sensor and i observed the immidiate rise in temperature and humidity displayed on OLED.

---

### Task 2: Running the Code Without Interrupt 

In this task I run the code by disabling interupt so ISR do not run .ISR handles the button press, whenever we press button it toggles the power of OLED. As a result of disabling ISR , screen of oled is continuously turned on and have no any effect.  
---

### Task 3: Understanding Debounce Issue  

#### What is a debounce issue and why we get rid of it?  
Okay, so when we press a button, we expect it to turn ON or OFF instantly, right? But in reality, the button doesn’t work that smoothly. It kind of "bounces" a few times before settling. This bouncing means the microcontroller might think we pressed the button multiple times even though we only pressed it once. This can mess up our program.  

To fix this, we use a debounce technique, which helps the microcontroller ignore those extra unwanted signals and only count a single button press. Without it, our button might act weird, like turning ON and OFF super fast or not responding properly.  

---

#### In which applications/domains can the debounce issue be threatening if not resolved in the system?  
Debounce problems are mostly annoying in simple projects, but in serious systems like medical devices, industrial machines, and security systems, it can be a big problem. Imagine a hospital machine that gives medicine and mistakenly registers multiple button presses because of bouncing—yikes! Or a factory machine that starts and stops unpredictably. That’s why we must take debounce seriously in important applications.  

---

#### Why does debounce occur? Is it a compiler error, logical error, or is the microcontroller cheap?  
Debounce happens because of how mechanical buttons work, not because of the compiler or cheap microcontrollers. When we press a button, its metal contacts physically touch, but they don’t make a smooth connection immediately—they vibrate a bit, creating tiny, quick ON-OFF signals before settling. This isn’t a logical or compiler issue; it’s just how buttons behave naturally. Even expensive microcontrollers will have this issue unless we handle it in code or hardware.  

---

### Task 4: Why Do We Use Interrupts  

#### Why do we use interrupts?  
Interrupts are like an urgent notification for the microcontroller. Instead of checking something over and over in a loop (which wastes time), the microcontroller can do other tasks and only respond when needed. For example, instead of constantly checking if a button is pressed, we can use an interrupt so the microcontroller only reacts when the button is actually pressed. This makes the system efficient and responsive.  

---

#### How does an interrupt lower the processing cost of the microcontroller?  
Without interrupts, the microcontroller would keep running loops to check if an event happened (like checking if a button was pressed). This wastes processing power. Interrupts let the microcontroller chill and do other things until something important happens. When an interrupt occurs, it quickly stops what it’s doing, handles the important task, and then goes back to work. This saves energy and allows the microcontroller to handle multiple tasks smoothly.  
