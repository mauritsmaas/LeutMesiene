DROP TABLE IF EXISTS types;
DROP TABLE IF EXISTS attack_oses;
DROP TABLE IF EXISTS phases;
DROP TABLE IF EXISTS items;
DROP TABLE IF EXISTS item_types;
DROP TABLE IF EXISTS item_attackos;

CREATE TABLE types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE attack_oses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    os TEXT NOT NULL
);

CREATE TABLE phases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    phase TEXT NOT NULL
);

CREATE TABLE items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type_id INTEGER NOT NULL
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    usage TEXT,
    source TEXT NOT NULL,
    cve TEXT,
    phase_id INTEGER NOT NULL,
    FOREIGN KEY (type_id) REFERENCES type (id),
    FOREIGN KEY (phase_id) REFERENCES phases (id)
);

CREATE TABLE item_types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id INTEGER,
    type_id INTEGER,
    FOREIGN KEY(item_id) REFERENCES items(id),
    FOREIGN KEY(type_id) REFERENCES types(id)
);

CREATE TABLE item_attackos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id INTEGER,
    attackos_id INTEGER,
    FOREIGN KEY(item_id) REFERENCES items(id),
    FOREIGN KEY(attackos_id) REFERENCES attack_oses(id)
);
