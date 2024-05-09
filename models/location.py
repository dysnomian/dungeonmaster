from db import conn

cursor = conn.cursor()

# Create locations table
create_locations_table = """
CREATE TABLE IF NOT EXISTS Locations (
    id SERIAL PRIMARY KEY NOT NULL,
    starting_location_id INTEGER REFERENCES Locations(id) ON DELETE CASCADE,
    parent_id INTEGER REFERENCES Locations(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL UNIQUE,
    category VARCHAR(100),
    interior_description TEXT,
    exterior_description TEXT,
    notes TEXT
"""
cursor.execute(create_locations_table)
curso