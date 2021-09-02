
CREATE TABLE image_urls (
    id SERIAL PRIMARY KEY,
    search_query VARCHAR(50),
    image_url VARCHAR(300),
    downloaded BOOLEAN DEFAULT FALSE
);