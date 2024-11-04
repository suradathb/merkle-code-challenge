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
