SELECT *
FROM foo
WHERE bar IN ('hello', 'world')

SELECT * FROM foo
WHERE baz IN (
    select * from bar
    where woz in ('apple', 'steve'))


UPDATE sometable
SET foo = 'bar',
    bar = 'foo'
    /* hello = hello + 1 */
/* WHERE foo = 'baz' */


DELETE FROM [foo bar]
/* WHERE x = 1 */


SELECT hello, world
FROM [foo bar]
/* WHERE hello = 'foobar' */
