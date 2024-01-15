Lab 1: Application Security
===========================

Instructions
------------
The internet is going crazy over the newest social media, TweetBook! Their user numbers are skyrocketing, young gen alphas are using it to post incriminating videos of themselves, and every other social media is scrambling to blatantly copy all of its features. But as a security researcher, you have heard rumors that the site may not be as secure as it claims. You have taken it upon yourself to (responsibly and legally) test their security and see what you can find.

To access the lab, go to csci3403.com and select Lab 4. From that page, you can create a new lab environment, or join an existing lab environment if you would prefer to work with others. We suggest you do this lab in a group! While you are collaborating, we ask that you remain respectful of others and keep your inputs university-appropriate.

Scope (THIS IS IMPORTANT!):
---------------------------
You have permission to attack the lab server which is hosted on csci3403.com. You have permission to exploit any vulnerabilities with one exception: you are not allowed to intentionally perform denial-of-service attacks or in any way prevent other students from accessing the lab.

Challenges
----------
To complete this lab, you will need to exploit a number of vulnerabilities. You are given the impact of each vulnerability, and it is your job to discover how to exploit them. This lab covers the following skills (additional vulnerabilities may exist in the site, but these are not worth points):

- Modify client-side code and cookies
- Read and modify network requests
- Perform CSRF attacks

### Bypass Length Limits (10 points)
Make a post longer than 64 characters.

### Reset User Passwords (20 points)
Reset the password for one of the instructor’s accounts.
### Steal User Passwords (20 points)
Steal the password for one of the instructor’s accounts, and use it to log in. You will need to use the account’s original password, this will not work if you use a password which has been reset.
### Access an Account Without a Password (20 points)
Access an instructor’s account without ever using their password.
### CSRF Attack (30 points, 10 points possible extra credit)
[This is a group exercise: Only one person in your lab environment needs to execute it]

Set up your own malicious website which causes anyone who visits it to make a post on TweetBook (this post can say anything at all). The attack should trigger automatically when the victim visits the malicious URL without requiring any additional input.

To get credit for this challenge, you will need to execute this attack against one of the instructors! This means your malicious site will need to be publicly accessible. We have set up a public server at student.csci3403.com which you can log on to with these credentials:

Username: Your identikey
Password: csci3403! (we recommend you change this to something more secure)

You can host your website with this command (you will need to pick a port number greater than 1024 which does not conflict with another student):

$ python -m http.server <port number>

Once you have set up your malicious site to be publicly accessible, send a link to any of the instructors in this class. Make sure to test these links before sending them to an instructor! They will click any links you send, and if the attack executes successfully you will get credit.

### Extra credit (10 points): Phish the instructors!
The instructors will click any links you send, even if they know it is part of this lab. But if you are able to trick them into clicking it without knowing that it will trigger an attack, you will get 10 points of extra credit. The instructors will be on the lookout, so be creative!