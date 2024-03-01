# -*- coding: utf-8 -*-
import time
from time_password_checker import check_password

class solution():
    def __init__(self) -> None:
        # DO NOT MODIFY THE EXISTED PROPERTY
        # You can add as many properties as you need
        self.password = "" # This is where your guessed password is store
    
    def example(self):
        # The following shows how to get the time spent
        # You can modify it to test your ideas
        
        # If password is correct, check_password will return Correct
        # If password is wrong, check_password will return Wrong
        
        T1 = time.perf_counter()
        result = check_password(self.password)
        T2 = time.perf_counter()
        
        # You can print the output for debug or test.
        print(result)
        print("time spend: ", T2-T1)
        
    def getPassword(self):
        # Please complete this method
        # It should be the return the correct password in a string
        # GradeScope will import your class, and call this method to get the password you calculated.
        pwLength_max = 11 # maximum password length
        pw_list = [] # password list
        for pw_idx in range(pwLength_max): # loop 11 times, find the correct char at password[pw_idx]
            char_time_pair = [0, 0] # temp list to record [correct_char, process_time]
            for pw_char in range(33,127): # loop all possible chars
                time_list = [] # list to store excution time
                pw_list.append(chr(pw_char)) # append cur_char
                for x in range(10): # sampling 10 time for purpose of removig random noise
                    T1 = time.perf_counter()
                    result = check_password(''.join(pw_list))
                    T2 = time.perf_counter()
                    time_list.append(T2-T1)
                if (result == 'Correct'): # if correct, well done
                    print(pw_list)
                    self.password = ''.join(pw_list)
                    return self.password
                pw_list.pop() # pop out cur_char
                time_list.sort() # sort time_list ascendingly
                time_avg = sum(time_list[:5]) / 5.0 # average one half to remove potential noise
                if (time_avg > char_time_pair[1]):
                    char_time_pair = [chr(pw_char),time_avg]
            pw_list.append(char_time_pair[0])
            print(pw_list)

# Write Up
# Please explain your solution
"""
General idea:
Test one character at a time. Character matches if the responding time is longer.
The first looping to find the matched character for pw[0].
A foor loop and chr() function gives all possible ascii characters.
Append one character to pw_list and send pw_list to check_password(), pop the character out after.
Record the combination of [char, responding_time].
Based on max(responding_time), append the character to pw_list. One character found.
Repeat the loop to find the next character

Deal with Random Noise:
For the same password combination, pw_list, 
I send it to check_password() multiple time and collect all responding_time.
In this case, 10 samples seem to be sufficient. The number can definitely be larger for accuracy.
I first sort() the list that contains these 10 samples,
then choose only the first half of the responding_time for averaging.
This way, it removes those large number that come from randome noise.
"""