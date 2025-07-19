-- Active: 1718634278776@@127.0.0.1@5432@app_db@public

DROP PROCEDURE IF EXISTS city_reports;


CREATE OR REPLACE PROCEDURE city_reports (p_city VARCHAR, p_month VARCHAR, p_year NUMERIC, p_total DOUBLE PRECISION)
LANGUAGE plpgsql
AS $$
DECLARE
    v_id INTEGER;
    v_count INTEGER;
    v_total INTEGER;
BEGIN

    SELECT id, count, total
    INTO v_id, v_count, v_total
    FROM city_monthly_reports
    WHERE city = p_city AND month = p_month AND year = p_year
    ORDER BY year, month DESC
    LIMIT 1;

    IF v_id IS NULL THEN
        INSERT INTO city_monthly_reports (id, city, month, year, count, total)
        VALUES (DEFAULT, p_city, p_month, p_year, 1, p_total);
    ELSE
        UPDATE city_monthly_reports
        SET count = v_count+1, total=v_total+p_total
        WHERE id = v_id;
    END IF;
END;
$$;
