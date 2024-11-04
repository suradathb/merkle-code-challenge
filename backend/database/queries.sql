-- Query เพื่อแสดงลูกค้าที่ใช้จ่ายมากที่สุด 3 อันดับแรก
SELECT user_id, SUM(usd_amount) AS total_spent
FROM transactions
GROUP BY user_id
ORDER BY total_spent DESC
LIMIT 3;

-- Query เพื่อหาจำนวนผู้ใช้ที่ใช้จ่ายมากกว่า $1,000 แต่ไม่เกิน $2,000
SELECT COUNT(*)
FROM (
    SELECT user_id, SUM(usd_amount) AS total_spent
    FROM transactions
    GROUP BY user_id
    HAVING total_spent > 1000 AND total_spent < 2000
) AS subquery;

-- Query เพื่อแสดงประเทศที่มีการใช้จ่ายเฉลี่ยต่อผู้ใช้น้อยกว่า $500
SELECT country
FROM users
JOIN (
    SELECT user_id, AVG(usd_amount) AS avg_spent
    FROM transactions
    GROUP BY user_id
) AS user_spending ON users.id = user_spending.user_id
GROUP BY country
HAVING AVG(user_spending.avg_spent) < 500;
