# -*- coding: utf-8 -*-
import subprocess

class solution:
    def __init__(self) -> None:
        # DO NOT MODIFY THE EXITED PROPERTIES
        # You can add as many properties as you need
        self.mem_ctl_exe = "./mem_ctl.exe"                      # This is the path of mem_ctl.exe file
        self.pwd_checker_exe = "./mem_password_checker.exe"     # This is the path of password_checker.exe file
        self.password = ""                                      # This is where your guessed password is store
        
    def setProtectMem(self, start_index, end_index):
        # DO NOT MODIFY THIS METHOD
        
        # This method used to set a range of memory can not be accessed starting from start_index, ending with end_index (included).
        # After set [start_index, end_index] as can not be accessed, any read or write operations will
        # If this operation successfully executed, this method will return some output from the mem_ctl.exe
        # Otherwise, this method will return -1
        if(start_index <= end_index and start_index >= 0 and start_index < 1024 and end_index >=0 and end_index < 1024):
            p1 = subprocess.Popen([self.mem_ctl_exe, str(start_index), str(end_index)],stdout=subprocess.PIPE)
            mem_ctl_exe_result = p1.communicate()[0].decode()
            return mem_ctl_exe_result
        else:
            return -1

    def checkPassword(self, password):
        # DO NOT MODIFY THIS METHOD
        
        # This method will pass your password to mem_password_checker.exe to verify the correctness
        # The return value is a string which is the output of mem_password_checker.exe
        # If password is correct, this method will return Correct
        # If password is wrong, this method will return Wrong
        # If mem_password_checker accessed an can not be accessed memory, this method will return SEG ERROR
        
        p2 = subprocess.Popen([self.pwd_checker_exe, password], stdout=subprocess.PIPE)
        pwd_checker_exe_result = p2.communicate()[0].decode()
        return pwd_checker_exe_result
    
    def example(self):
        # The following shows how to call a executable file in python and capture its output
        # You can modify it to test your ideas
        
        mem_ctl_exe_result = self.setProtectMem(100,1000)
        # You can print the output for debug or test.
        print(mem_ctl_exe_result)
        print('haha')

        # After mem_ctl.exe executed, the memory in range [start_index, end_index] will be set to can not be accessed.
        # That means, password_check.exe will not accessible this section of memory.
        # Any read or write from password_check.exe to this range will cause an "SEG ERROR"

    
        pwd_checker_exe_result = self.checkPassword("guess")
        # You can print the output for debug or test.
        print(pwd_checker_exe_result)


        # For password_checker.exe, the password you input will be stored from the beginning of the memory.
        # Take the above parameters as input, the memory structure is shown below:

        # index:        0--------------------100----------------------------------1000----------1023
        # access type:  |-----accessible------|---------cannot be accessed----------|--accessible--|
        # value:        guess\0#####################################################################

        print(self.password)
    
    def getPassword(self):
        # Please complete this method
        # It should be the return the correct password in a string
        # You should modify the start_index, end_index and password appropriately to achieve the attack
        # GradeScope will import your class, and call this method to get the password you calculated.
        blocker_idx = 1 # initialize protectMen index
        pwLength_max = 20 # maximum password length
        pw_list = [] # password list
        for pw_idx in range(pwLength_max): 
            self.setProtectMem(blocker_idx,1023) # Men[blocker_idx,1023] is now protected from accessing
            for c in range(33,127): # loop all ascii characters from 33 ro 126
                pw_list.append(chr(c)) # append the current chracter to the list
                if (self.checkPassword(''.join(pw_list))=='SEG ERROR'): # the cur_char correct, require more chars for password
                    blocker_idx+=1 # increse blocker index to test next_char
                    break
                if (self.checkPassword(''.join(pw_list))=='Correct'): # final answer to the password
                    self.password = ''.join(pw_list) 
                    return self.password # return the password as a string
                pw_list.pop() # fail the previous two if statement, pop out the most recent character

# Write Up
# Please explain your solution
"""
The general idea is to test one character at a time. Determine the correcctness depends on return messages.
The first looping, I block Men[block_idx=1, 1023] and test individual ascii char on Men[0].
A for_loop in range(33,127) and a chr() conversion can test all possible char on Men[0].
Wrong, SEG ERROR, and Correct are three possible return messages.
I do no need to worry about 'Wrong', because all char will be test until the one matched.
if 'SEG ERROR', meaning that cur_char is matched, but pw_length is more than this, we increase block_idx to test the next_char, go to the next loop
if 'Correct', meaning that cur_char is matched, and pw_length is matched, all done.

Notes on pw_list variable.
append() and pop() enable the modification to the last item of the list.
append() cur_char, if the cur_char matched, it never goes to pop() and stay in pw_list, otherwise pop().
"""