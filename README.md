# db_upgrade
A python script that upgrades a **MySQL DB** by running scripts against it.

This script assumes that you have a **MySQL DB** running on the **localhost**. For simplicity’s sake I have created a **test DB** without a password. You will obviously have to change this for Production use cases.

This script looks for numbered files ending in `.sql` within the **’scripts’** directory. The naming convention it assumes is of a **‘number’** followed by a name, for example: `003createtemptable.sql`.

It reads the current version from the `version` table in the DB and if any of the scripts have a **higher** version number, it executes the SQL in those scripts, **in numbered order**, against your database.

After it finishes doing the upgrades, it updates the `version` table with the new version number. This is to prevent the same updates from being run twice. 

Here’s some output from an example run:

```
kj@myvm:~/python$ ./do_upgrade.py
Max version: 045
Current version: 002
Upgrades to be applied:
['003', '004', '005', '045']

Applying upgrade 003.createtemptable.sql:
CREATE TABLE temp (id int not null auto_increment, name varchar(10) not null, primary key (id))

Applying upgrade 004.inserttemprow.sql:
INSERT INTO temp VALUES (0, 'Khusro')
INSERT INTO temp VALUES (0, 'John')
INSERT INTO temp VALUES (0, 'Jane')
INSERT INTO temp VALUES (0, 'Alice')

Applying upgrade 005updatetemprow.sql:
UPDATE temp SET name = 'John' WHERE name = 'Khusro'

Applying upgrade 045.createusertable.sql:
CREATE TABLE user (id int not null auto_increment, username varchar(10) not null, primary key (id))
Updating DB Version to: 045
```