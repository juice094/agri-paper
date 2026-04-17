-- Agri-Paper: agri_observations schema for devbase registry
-- Version: 0.2.0 (2026-04-17)
-- Changes from v0.1.0: added observed_at, lat, lon; severity CHECK constraint; composite index

CREATE TABLE IF NOT EXISTS agri_observations (
    id TEXT PRIMARY KEY,
    repo_id TEXT,
    crop TEXT NOT NULL,
    disease TEXT,
    symptoms TEXT,
    treatment TEXT,
    region TEXT,
    severity TEXT CHECK (severity IN ('mild', 'moderate', 'severe', 'critical')),
    confidence REAL CHECK (confidence >= 0.0 AND confidence <= 1.0),
    source TEXT,
    -- Added per devbase review (2026-04-17)
    observed_at TEXT,           -- ISO-8601 timestamp of field observation
    lat REAL,                   -- Latitude for spatial queries
    lon REAL,                   -- Longitude for spatial queries
    FOREIGN KEY (repo_id) REFERENCES repos(id) ON DELETE CASCADE
);

-- Index strategy proposed by devbase + agri-paper joint review
CREATE INDEX IF NOT EXISTS idx_agri_crop ON agri_observations(crop);
CREATE INDEX IF NOT EXISTS idx_agri_disease ON agri_observations(disease);
CREATE INDEX IF NOT EXISTS idx_agri_region ON agri_observations(region);
CREATE INDEX IF NOT EXISTS idx_agri_crop_region ON agri_observations(crop, region);  -- Most frequent query pattern
CREATE INDEX IF NOT EXISTS idx_agri_source ON agri_observations(source);
