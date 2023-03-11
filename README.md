# bufferoverflow-usingRop-gadgets

The first step would be to compile the binary using gcc and run it using GDB.
When we run “info functions” command ,we see that there are three interesting functions apart from the built in binary functions that are available,one is the main function,the “ultimateQuestion” function and the loop function.
The main function just calls the loop function and in this function we get to see a bunch of junk values being pushed on to the stack.

![image](https://user-images.githubusercontent.com/114467712/224474600-746852f9-d9a7-429f-b51c-33f9ad04babe.png)
 
Then the loop function calls the ultimateQuestion function and then the process continues.
We see in the ultimateQuestion that the buffer is being set up as shown in the screenshot.When converted to the binary value,the buffer length is about 438 bytes long.This is excluding the PIE artifacts ,ebp and the eip.

![image](https://user-images.githubusercontent.com/114467712/224474605-48cf7add-3b39-4b4b-924a-4c53e8b7cfb3.png)
 
So I decided to put ‘A’s in the payoad to check the size of the buffer.I started from 448,to see big the payload needs to be overflow the return pointer.I set a breakpoint at ultimateQuestion+42 and ran > r < <(python3 -c "print('A'* 449)").The return pointer didn’t overrun. Then I increased by another 4 and this time I knew the total I had to over flow was 452 bytes long to overflow the return pointer. 

![image](https://user-images.githubusercontent.com/114467712/224474611-0ec9009e-769b-4bf5-b35e-20d1f559af75.png)
 
This created a seg fault.
I knew where the pointer to the buffer was,so I had to use rop gadgets that would land on the stack which later points to the buffer.This was the task.
I had to find ROP gadgets that would pop 7 junk values off the stack and make land on the address that I wanted.

![image](https://user-images.githubusercontent.com/114467712/224474615-bdf96c43-ade4-42c9-a8f5-f25d3b0e4d62.png)
 
This was where I needed to land ,inbetween there where 7 junk values that I had to get rid off.
The rop gadgets used in payload is:

![image](https://user-images.githubusercontent.com/114467712/224474621-a4f6ecf4-f3ef-4803-a89a-f2c2827323bf.png)

 

•	The first one pops 4 times and then returns
•	The second one pops twice and returns, which in turn points to our buffer on the stack.
So it was clear the payload that I was supposed to use.
-448 bytes of NOPS and shellcode
-pointer to the first rop gadget(pops 4 times)
-16* ‘\x90’(to compensate the 4 pops each of 4 bytes)
-secound rop gadget.
Ran my payload in pwn-debug to check if the payload worked.

![image](https://user-images.githubusercontent.com/114467712/224474635-a2e4cc5b-7103-4a8d-96a9-6c3c10fd9816.png)
 
As you can see it did work.Next was to use pwntools and python3 to run the payload outside of GDB.I used the same structure of the payload to get the shell.The shellcode that I used in the payload was from shellstorm.com.
The problem wasn’t over yet.I still had to check for bad characters in the particular binary.So I ran the entire hexdecimal values from ‘\00’ to \xff’ to filter out the bad characters and I got a couple of them.
This made me use a payload that didn’t have any of these characters in them.This was hectic.I wanted to everything manually and didn’t want to rely on automating and using tools like msfvenom to build my payload.
So I ran the payload and successfully got a shell.

![image](https://user-images.githubusercontent.com/114467712/224474637-fddae0df-d885-4cf9-94b0-657a3d1b0164.png)
 
 
![image](https://user-images.githubusercontent.com/114467712/224474645-00e39401-4a3f-4699-a00f-db117332281d.png)

The above two screenshot shows obtaining a shell when ran outside GDB. 

The final POC:

![image](https://user-images.githubusercontent.com/114467712/224474649-fddae0cb-6ae8-489f-817b-02e0f79d4518.png)
![image](https://user-images.githubusercontent.com/114467712/224474654-87a1c6e4-79c7-4587-96e9-18db063769de.png)

 
 
My shellcode was 136 bytes long and the one I used to test on pwn-debug was 40 bytes long without any bad characters.
