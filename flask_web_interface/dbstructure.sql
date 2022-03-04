DROP TABLE IF EXISTS types;
DROP TABLE IF EXISTS attack_oses;
DROP TABLE IF EXISTS phases;
DROP TABLE IF EXISTS items;
DROP TABLE IF EXISTS item_assignees;

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
    FOREIGN KEY (type_id) REFERENCES type (id),
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    usage TEXT,
    source TEXT NOT NULL,
    cve TEXT,
    FOREIGN KEY (os_id) REFERENCES attack_oses (id),
    FOREIGN KEY (phase_id) REFERENCES phases (id)
);

CREATE TABLE assignees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE item_assignees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id INTEGER,
    assignee_id INTEGER,
    FOREIGN KEY(item_id) REFERENCES items(id),
    FOREIGN KEY(assignee_id) REFERENCES assignees(id)
);
