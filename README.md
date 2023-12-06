# 👃🏼SSHniffer V 1.0👃🏼
*This tool is intended for security professionals and is intended to be 
used with proper concent.* 


## What is this tool?
A post-compromise agent to be deployed on rooted linux machines designed 
to quietly listen for SSH connections. When a domain user/service connects 
to the linux device with a password, the agent will log the sshd process 
data by using strace. (Note: this *does not* work when a user 
authenticates via pem key). The agent also periodically attempts to 
connect back to a hard coded IP and port to send the contents of the sshd 
process data which includes a user name and password. From your attacking 
machine, simply open up a NetCat port that you have the agent configured 
to connect back to and the agent will pipe it over to you.

## How to use this tool?
This is a very simple to use program. Simply download the python script and 
modify it to send data back to your IP and Port. Once configured, place 
the shell script on the compromised linux device, and execute "python3 SSHniffer.py" with root context. This tool will continously run in the 
background and send data once you open up the configured listening port on 
your attacking machine. 

## Expected updates:
- Rust version
- Bash one-liner
- Continous streaming:
    - Currently you need to break the socket and reconnect for updated data
- Eaiser readable format:
    - At the moment, the data is very messy and not very 
predicatable. Currently working on a way to grep out user and password 
data only.
- Better status updates:
    - Have the program be informed when it recieves an SSH connection and possibly display user:pass to terminal. (Need to find a reliable way to grep first.)

## Demo:
https://github.com/JitBox/SSHniffer/assets/64562427/a60a6a04-feee-4697-a323-e549c39c49d4

