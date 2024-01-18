-- Selects band_name and calculates the lifespan in 
-- years for Glam rock bands

SELECT
    band_name,
    -- Uses DATEDIFF to calculate the difference in days between the end year 
    -- (or 2022 if the band is still active) and the formed year
    -- If the band has a split year, it uses the split year; otherwise, it uses the end of 2022
    ROUND(DATEDIFF(IFNULL(split, '2022-01-01'), CONCAT(formed, '-01-01')) / 365, 2) AS lifespan
FROM
    metal_bands
WHERE
    style LIKE '%Glam rock%'
-- Orders the result set by the calculated lifespan in descending order
ORDER BY
    lifespan DESC;

