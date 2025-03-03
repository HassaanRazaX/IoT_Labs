# LAB3 - MicroPython Home Tasks

## Home Tasks

###  Task 1: Displaying Temperature & Humidity on OLED
###  Task 1.1
In this task, I connected the DHT22 sensor with the ESP and showed temperature and humidity readings on the OLED using Wokwi. It was cool seeing live data pop up on the small screen. I just had to keep refreshing the readings every second, and sometimes it took a sec to load, but it worked fine overall.

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

---

### Task 4: Interrupt and Debounce on ESP32
This task was different. I uploaded the code directly to the ESP32, where I used interrupts and debounce concepts. Pressing the button turned the OLED on and off, but without debounce, it kept flickering. Adding debounce with a timer fixed that. It was fun seeing how a small press could control the screen. Learned how interrupts react instantly, which was pretty cool.

---

> Overall, Lab3 was fun and practical. Got to mess around with sensors, displays, and buttons. Some parts were confusing at first but seeing things work in real-time felt rewarding.

