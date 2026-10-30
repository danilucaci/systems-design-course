CREATE TABLE IF NOT EXISTS users (
    id uuid PRIMARY KEY,
    email text NOT NULL UNIQUE CHECK (length(email) BETWEEN 3 AND 254)
);
CREATE TABLE IF NOT EXISTS journeys (
    id uuid PRIMARY KEY,
    owner_id uuid NOT NULL REFERENCES users(id),
    name text NOT NULL CHECK (length(btrim(name)) BETWEEN 1 AND 120),
    created_at timestamptz NOT NULL DEFAULT now(),
    version integer NOT NULL DEFAULT 1 CHECK (version > 0),
    UNIQUE (owner_id, id)
);
CREATE TABLE IF NOT EXISTS journey_stops (
    owner_id uuid NOT NULL,
    journey_id uuid NOT NULL,
    position integer NOT NULL CHECK (position >= 0),
    station_id uuid NOT NULL,
    PRIMARY KEY (journey_id, position),
    FOREIGN KEY (owner_id, journey_id) REFERENCES journeys(owner_id, id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS create_requests (
    owner_id uuid NOT NULL,
    operation_key varchar(80) NOT NULL,
    payload_hash bytea NOT NULL,
    journey_id uuid NOT NULL,
    response_snapshot jsonb NOT NULL,
    PRIMARY KEY (owner_id, operation_key),
    FOREIGN KEY (owner_id, journey_id) REFERENCES journeys(owner_id, id)
);
