USE ecshop;
DESC ecs_admin_user;
SELECT * FROM ecs_admin_user;

SELECT * FROM ecs_users;
UPDATE ecs_users
SET user_money = 100000
WHERE user_id = 1;