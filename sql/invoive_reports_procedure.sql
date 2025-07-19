-- Active: 1718634278776@@127.0.0.1@5432@app_db@public
DROP PROCEDURE IF EXISTS invoice_reports;

CREATE OR REPLACE PROCEDURE invoice_reports (
    p_month VARCHAR,
    p_year INTEGER,
    p_total DOUBLE PRECISION
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_id INTEGER;
    v_count INTEGER;
    v_total INTEGER;
BEGIN
    SELECT id, count, total
    INTO v_id, v_count, v_total
    FROM invoice_monthly_reports
    WHERE month = p_month AND year = p_year
    ORDER BY year, month DESC
    LIMIT 1;

    IF v_id IS NULL THEN
        INSERT INTO invoice_monthly_reports (id, month, year, count, total)
        VALUES (DEFAULT, p_month, p_year, 1, p_total);
    ELSE
        UPDATE invoice_monthly_reports
        SET count = v_count+1, total=v_total+p_total
        WHERE id = v_id;
    END IF;
END;
$$;
