-- A sql script that ranks bands from country of origin 
-- ordered by nun unique fans
SELECT origin, SUM(fans) AS nb_fans
FROM metal_bands
GROUP BY origin
ORDER BY nb_fans DESC;

