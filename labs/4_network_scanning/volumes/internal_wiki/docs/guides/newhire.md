# New Hire: Getting Started

## Getting VPN access

Send an email to Alice, the head of IT. She will create an account for you on the VPN, which should give you all the access you need to access our production servers!

## Script Credentials

Please don't use your personal account credentials in any scripts, as that could cause your code to fail if you ever get fired. Instead, please use these service account credentials for any automated jobs:

!!! warning inline end

    These credentials should not be pushed to git or shared outside the company

Username: `dev`  
Password: `{flag1-internal-use-only}`

These should give you access to most of the production machines.

## Data Access

We store all of our customer data in the "sales" database. The normal service credentials cannot read the database for security reasons, only actual employees have that level of access. Any employee can connect using this command:

`psql -h 172.16.10.6 -U [your username] -d sales`

If you forget the table names, can run `\dt` to see a full list of them. Remember to put a semicolon after each database query!