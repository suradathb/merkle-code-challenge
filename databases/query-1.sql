-- Query เพื่อแสดงลูกค้าที่ใช้จ่ายมากที่สุด 3 อันดับแรก
SELECT user_id, SUM(usd_amount) AS total_spent
FROM transactions
GROUP BY user_id
ORDER BY total_spent DESC
LIMIT 3;