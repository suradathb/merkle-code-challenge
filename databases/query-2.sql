-- Query เพื่อหาจำนวนผู้ใช้ที่ใช้จ่ายมากกว่า $1,000 แต่ไม่เกิน $2,000
SELECT COUNT(*)
FROM (
    SELECT user_id, SUM(usd_amount) AS total_spent
    FROM transactions
    GROUP BY user_id
    HAVING total_spent > 1000 AND total_spent < 2000
) AS subquery;