/************ Update: Tables ***************/
set search_path = riego, pg_catalog;
/******************** Add Table: estado_fenologico ************************/
CREATE SEQUENCE estado_fenologico_codigo_estado_fenologico_seq INCREMENT 1;

/* Build Table Structure */
CREATE TABLE estado_fenologico
(
	codigo_estado_fenologico INTEGER NOT NULL DEFAULT nextval('estado_fenologico_codigo_estado_fenologico_seq'),
	descripcion_estado_fenologico TEXT NOT NULL
);

/* Table Items: estado_fenologico */
ALTER TABLE estado_fenologico ADD CONSTRAINT pkestado_fenologico
	PRIMARY KEY (codigo_estado_fenologico);

/******************** Add Table: registro_estado_fenologico ************************/
CREATE SEQUENCE registro_estado_fenologico_codigo_registro_estado_fenologico_seq INCREMENT 1;

/* Build Table Structure */
CREATE TABLE registro_estado_fenologico
(
	codigo_estado_fenologico INTEGER NOT NULL,
	codigo_registro_estado_fenologico INTEGER NOT NULL DEFAULT nextval('registro_estado_fenologico_codigo_registro_estado_fenologico_seq'),
	fecha DATE NOT NULL,
	codigo_cultivo INTEGER NOT NULL,
	codigo_temporada INTEGER NOT NULL
);

/* Table Items: registro_estado_fenologico */
ALTER TABLE registro_estado_fenologico ADD CONSTRAINT pkregistro_estado_fenologico
	PRIMARY KEY (codigo_registro_estado_fenologico);


/************ Add Foreign Keys to Database ***************/

/************ Foreign Key: fk_registro_estado_fenologico_estado_fenologico ***************/
ALTER TABLE registro_estado_fenologico ADD CONSTRAINT fk_registro_estado_fenologico_estado_fenologico
	FOREIGN KEY (codigo_estado_fenologico) REFERENCES estado_fenologico (codigo_estado_fenologico) ON DELETE NO ACTION;
