SELECT 
    u.id, 
    u.email, 
    COUNT(l.id) AS link_count
FROM 
    users_customuser AS u
LEFT JOIN 
    links_link AS l ON u.id = l.user_id
GROUP BY 
    u.id
ORDER BY 
    link_count DESC, 
    u.created_at ASC
LIMIT 10;
