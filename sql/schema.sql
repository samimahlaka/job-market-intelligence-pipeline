CREATE TABLE dim_company(
    company_id SERIAL PRIMARY KEY,
    company_name VARCHAR(255) UNIQUE
    );

CREATE TABLE dim_location(
    location_id SERIAL PRIMARY KEY,
    city VARCHAR(255) NOT NULL,
    state VARCHAR(255) NOT NULL,
    country VARCHAR(255) NOT NULL,
);

CREATE TABLE dim_skill (
    skill_id SERIAL PRIMARY KEY,
    skill_name VARCHAR(100) UNIQUE
);

CREATE TABLE fact_jobs (
    job_id BIGINT PRIMARY KEY,
    job_title VARCHAR(255),
    company_id INT,
    location_id INT,
    posted_date DATE,
    remote_flag BOOLEAN,

    FOREIGN KEY (company_id)
        REFERENCES dim_company(company_id),

    FOREIGN KEY (location_id)
        REFERENCES dim_location(location_id)
);

CREATE TABLE bridge_job_skill (
    job_id BIGINT,
    skill_id INT,

    PRIMARY KEY (job_id, skill_id),

    FOREIGN KEY (job_id)
        REFERENCES fact_jobs(job_id),

    FOREIGN KEY (skill_id)
        REFERENCES dim_skill(skill_id)
);
