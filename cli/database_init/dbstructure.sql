DROP TABLE IF EXISTS types;
DROP TABLE IF EXISTS attack_oses;
DROP TABLE IF EXISTS phases;
DROP TABLE IF EXISTS items;
DROP TABLE IF EXISTS item_types;
DROP TABLE IF EXISTS item_attackos;


CREATE TABLE types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
);

CREATE TABLE attack_oses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    os TEXT 
);

CREATE TABLE phases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    phase TEXT 
);

CREATE TABLE items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    type_id INTEGER,
    description TEXT ,
    usage TEXT,
    source TEXT,
    cve TEXT,
    phase_id INTEGER ,
    FOREIGN KEY (type_id) REFERENCES types (id),
    FOREIGN KEY (phase_id) REFERENCES phases (id)
);

/*
CREATE TABLE item_types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id INTEGER,
    type_id INTEGER,
    FOREIGN KEY(item_id) REFERENCES items(id),
    FOREIGN KEY(type_id) REFERENCES types(id)
);
*/
CREATE TABLE item_attackos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id INTEGER,
    attackos_id INTEGER,
    FOREIGN KEY(item_id) REFERENCES items(id),
    FOREIGN KEY(attackos_id) REFERENCES attack_oses(id)
);

/*
(1, 'command')
(2, 'tool')

(1, 'linux')
(2, 'windows')
(3, 'mac')
(4, 'other')

(1, 'recon')
(2, 'scanning')
(3, 'initial foothold')
(4, 'privesc')
(5, 'maintain access')
(6, 'covering')
(7, 'general')
*/