Lab 2: Web Vulnerabilities
==========================

Instructions
------------
Nile, the online store from Lab 1, has hired you again! “We have fixed all of those logic bugs you found before”, their head engineer claims, “and now the site is completely secure!”. You have your doubts. You agree to look at the site, and immediately find that it is vulnerable to a number of injection attacks. Whoops! Looks like you can show them the error of their ways yet again.

To access the lab, go to csci3403.com and select Lab 5. From that page, you can create a new lab environment, or join a classmate’s lab environment. We suggest you do this lab in a group!

Scope (THIS IS IMPORTANT!):
---------------------------
You have permission to attack the lab server which is hosted on csci3403.com. You have permission to exploit any vulnerabilities with one exception: you are not allowed to intentionally perform denial-of-service attacks or in any way prevent other students from accessing the lab.

Challenges
----------
### SQL Injection: Show Hidden Items (10 points)
The product search is vulnerable to SQL injection. Find a way of displaying unlisted items.
### SQL Injection: Show Credit Cards (20 points)
One of the other database tables contains credit card information. Read one of the user credit card numbers. This requires an SQL UNION attack, and you will need these tips:

Every SELECT statement in a UNION must return the same number of results (called columns), and it will throw an error otherwise. For example, this UNION selects 5 columns on the left side, and however many columns are in the y table on the right side, meaning it will only work if there are exactly 5 columns in the y table:

	SELECT (a,b,c,d,e) FROM x UNION SELECT * FROM y;

If the y table only has two columns, you can add three extra columns which will always return 0 to ensure that both sides return five columns:

	SELECT (a,b,c,d,e) FROM x UNION SELECT *,0,0,0 FROM y;

You may not know how many columns are in a table, or what their names are. In that case, you can always add extra columns one at a time until it succeeds.

The credit cards are stored in a different database table than the products. You can find the name of that database using another SQL UNION attack and this SQLite command which selects the name of every table in the database:

SELECT name FROM sqlite_master WHERE type='table';

### Blind SQL Injection: Log In Without A Password (10 points)
The login page is vulnerable to blind SQL injection. In blind SQL injection, you are not able to see the results of your attack like you could on the product page, but you can still affect the SQL statement. Use this to log in as the user admin without knowing their password.

### Blind SQL Injection: Steal A Password (30 points)
Use blind SQL injection to steal the password for the user admin. While we do not receive data back from the server, we can use what is called a “side channel” attack: an attack which uses a secondary property of a system to read data which is not directly accessible. In this case, we can get information about a database query based solely on how long it takes to execute!

This SQL database has a function called SLEEP which takes an integer, and sleeps that many seconds before returning. (Note: SQLite does not normally have this function, but we have added it for this lab. Other databases, such as MySQL, do implement it). You can use the SLEEP function in a query such as in this example, which would wait 1 second before returning:
	SELECT * FROM users WHERE username='admin' AND SLEEP(1);

You can use the SLEEP function, along with these tips about how SQL operates, to determine what the password for the admin user is:
SQL uses short-circuit evaluation: the AND and OR operators do not evaluate their second argument if it would have no effect on the result. For example, this expression will not call SLEEP(1), because the first argument is always false, thus the entire AND expression is false and there is no reason to evaluate the second argument:

> 1=2 AND SLEEP(1);

Likewise, this expression will not run SLEEP(1) because the first argument to the OR operator is true, thus the entire OR expression is true:

> 1=1 OR SLEEP(1);

In SQL, the % character is a wildcard search. For example, this command will return any username starting with a:

> SELECT username FROM user WHERE username LIKE 'a%';

The admin password consists of five random lowercase characters.
You will likely want to automate this attack with Burp Suite. You can display the time a request took by selecting “Columns” > “Response received” from the menu bar.

Determine how to construct this side channel attack to steal the admin password. Log in using that password to receive credit.

### XSS Cookie Theft (30 points)
The site is vulnerable to XSS: specifically reflected XSS, meaning the attack can be stored in a malicious URL. Find where the site is vulnerable and note how the attack can be triggered simply by visiting a malicious URL.

To demonstrate the impact of this attack, you will steal the session cookie of an instructor by creating a malicious link which, when visited, runs JavaScript code that steals the user’s cookie and sends it to a server you control.

To receive the stolen cookies, you will need to set up a server which is publicly accessible and constantly recording data it receives. You can use the same server as before, student.csci3403.com, which you can log on to over SSH with these credentials:
Username: Your identikey
Password: csci3403! (unless you have changed it already)

A simple way of receiving and recording cookies is by hosting a simple web server using this command (you will need to pick a port greater than 1024 which is not used by another student):

> $ nohup python -m http.server <port number> &

This command runs a simple Python server which can receive web requests. Because we are using nohup, it will not exit if you log out, and it also logs every request it receives to an output file called nohup.out. To make sure it works, visit this URL (the URL doesn’t have to go anywhere):
http://student.csci3403.com:<port number>/<some random gibberish>

Then check the nohup.out file and make sure it logged the request, including the random gibberish you appended to the end. In your attack, you will replace that random gibberish with any important data you want to record.

Once your server is set up, write your XSS attack. It should run JavaScript which reads the cookies of the current user and sends them to your server. Some JavaScript tips:

- The cookies are stored in the document.cookie variable.
- The fetch() function can be used to make a GET request to any URL, for example:

    > fetch("http://example.com")

Test your attack by stealing your own cookies (you will need to be logged in first, and on Firefox, otherwise nothing will be sent). Once your attack is ready, send the malicious link to any of the instructors in this class over Slack. The instructors will let you know when they have clicked the link. If your attack worked, you should be able to read that instructor’s cookie from your logs. Use that cookie to log in as that instructor to receive credit!