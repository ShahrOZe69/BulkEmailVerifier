# BulkEmailVerifier
Can be used to verify 1000's of emails

# Instructions
Enter filename for example emails.txt

file should contains email in the format
          abc@efg.com
When running the program make sure that the result file (if it already exists) is closed otherwise it will give a permission denied error.. because the program can't write to a file which is already opened          
Use 500 threads

Set Proxy pool reset value to 100

The program will show progress as 1900/30000 

It verifies by first searching the MX record..if MX record exists it verifies it using xxxxxxx.xxx (site name hidden for Security-Purposes.. but you get the idea! :) )

It verified 5000 emails in an hour



