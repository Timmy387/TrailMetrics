SELECT * FROM files;

DROP TABLE trails;

DROP TABLE trail_users;

DROP TABLE files;


SELECT trail_name, strftime('%Y', day), count(*)
FROM trail_users
WHERE trail_name = 'Saddlemire'
GROUP BY trail_name, strftime('%Y', day);


SELECT trail_name, strftime('%Y', day)
FROM trail_users
GROUP BY trail_name
UNION
SELECT trail_name, 0
FROM trails
WHERE trail_name NOT IN (SELECT trail_name
                         FROM trail_users
                         WHERE day = '2018-05-11'
                         GROUP BY trail_name);


SELECT trail_name, strftime('%m', day), count(*)
FROM trail_users
WHERE trail_name = 'Saddlemire' AND strftime('%Y', day) = '2018'
GROUP BY trail_name, strftime('%m', day);