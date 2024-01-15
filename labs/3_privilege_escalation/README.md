Lab 3: Privilege Escalation
===========================

Instructions
------------
The online shopping platform from Lab 1, Nile, has reached out to you again. They maintain a number of Linux servers with multiple users, including one guest account which is accessible by a wide range of people. They want you to log on to this guest account and make sure that it is properly secured. Using your knowledge of Linux permissions, you will exploit vulnerabilities in this account to gain additional privileges and access data you should not be able to.

To access the lab, go to csci3403.com and select Lab 2. From that page, you can create a new lab environment, or join an existing lab environment if you would prefer to work in a group.

Scope (Important)
-----------------
You have permission to attack the lab server which is hosted on csci3403.com. You have permission to exploit any vulnerabilities with one exception: you are not allowed to intentionally perform denial-of-service attacks or in any way prevent other students from accessing the lab.

### Level 1 (20 points)
You have been given access to the guest account. This account is running a restricted shell, meaning many commands are not available:
- Normally, programs on Linux are stored in the directory /usr/bin, and if you look in that directory you will see all of the standard Linux commands. However, this restricted shell can only run programs in the directory /usr/rbin, which only includes ls, mv, and cp.
- The restricted shell disables many actions- the full list is here, but the important ones are that you cannot change your directory or run programs outside of /usr/rbin.

Given these restrictions and the limited commands you can run, find a way to run an actual shell which is not restricted. Prove that you have done so by reading the file level1.txt in your home directory. You will submit the contents of that file to Canvas.

### Level 2 (20 points)
There is also a file called level2.txt in your home directory, but even if you were in an unrestricted shell, you still do not have permission to read it. Read it anyway.

### Level 3 (20 points)
The level3.txt is in the home directory of the alice user (/home/alice). You do not have permission to read this particular file, but you can read some other files in her directory. These files can sometimes contain passwords or other important information, so see if there is anything in there which you can use.

### Level 4 (20 points)
The level4.txt is in the home directory of the bob user (/home/bob). You have permission to run a command as bob, which you can see by running sudo -l.

### Level 5 (20 points)
The level5.txt is in the home directory of the carol user (/home/carol). You have permission to run a command as carol, which you can see by running sudo -l. This command appears to be secure as it does not seem to allow you to run a shell at first glance. However, some of the command-line options can be used to trigger unexpected behavior.

### Extra credit (15 points)
There is an extra credit file in /root/extra_credit.txt which is only accessible by the root user. However, the root user has set up a cron job: a scheduled task which runs every minute. These jobs can be found in the directory /etc/cron.d/, and the configuration file there indicates that cron runs the file /usr/share/backup-script/backup.sh every minute as the root user. You don’t have permission to edit that backup script, but you have write permission to the directory it is in: this allows you to create or destroy new files in that directory. Use this permissions oversight to get root access and read the extra credit file.

_Hint: You do not have access to the output of this cron job, so your attack will have to work without user interaction. You can use the `date` command to see the server time: the cron job will run every minute on the minute._