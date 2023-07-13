DROP TABLE IF EXISTS brukere;
DROP TABLE IF EXISTS innlegg;
DROP TABLE IF EXISTS kommentar;

CREATE TABLE brukere (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	brukernavn VARCHAR(20) UNIQUE NOT NULL,
	passord VARCHAR(50) NOT NULL,
	er_admin BOOLEAN DEFAULT 0
);

CREATE TABLE innlegg (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	tittel VARCHAR(20) NOT NULL,
	innhold VARCHAR(512),
	dato_postet TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	bruker_id INT NOT NULL,
	FOREIGN KEY (bruker_id) REFERENCES brukere(id)

);

CREATE TABLE kommentar (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	innhold VARCHAR(100) NOT NULL,
	dato_postet TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	innlegg_id INT NOT NULL,
	bruker_id INT NOT NULL,
	FOREIGN KEY (innlegg_id) REFERENCES innlegg(id),
	FOREIGN KEY (bruker_id) REFERENCES burkere(id)
);

-- INSERT INTO brukere (brukernavn,passord,er_admin) VALUES 
-- 	("bruker1","passord",0),
-- 	("bruker2","passord",1);