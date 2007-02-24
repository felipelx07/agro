/************ Update: Schemas ***************/
CREATE SCHEMA riego;

set search_path = riego, pg_catalog;

/************ Update: Tables ***************/

/******************** Add Table: aplicacion ************************/
CREATE SEQUENCE aplicacion_codigo_aplicacion_seq INCREMENT 1;

/* Build Table Structure */
CREATE TABLE aplicacion
(
	codigo_aplicacion INTEGER NOT NULL DEFAULT nextval('riego.aplicacion_codigo_aplicacion_seq'::regclass),
	codigo_hilera INTEGER NULL,
	codigo_producto INTEGER NULL,
	dosis FLOAT NOT NULL,
	fecha DATE NOT NULL,
	rut VARCHAR(12) NULL,
	codigo_maquinaria INTEGER NOT NULL,
	codigo_implemento INTEGER NOT NULL
) WITHOUT OIDS;

/******************** Add Table: cuartel ************************/
CREATE SEQUENCE cuartel_codigo_cuartel_seq INCREMENT 1;

/* Build Table Structure */
CREATE TABLE cuartel
(
	codigo_cuartel INTEGER NOT NULL DEFAULT nextval('riego.cuartel_codigo_cuartel_seq'::regclass),
	codigo_sector INTEGER NOT NULL,
	descripcion_cuartel TEXT NOT NULL
) WITHOUT OIDS;

/* Table Items: cuartel */
ALTER TABLE cuartel ADD CONSTRAINT pkcuartel
	PRIMARY KEY (codigo_cuartel);

/******************** Add Table: cultivo ************************/
CREATE SEQUENCE cultivo_codigo_cultivo_seq INCREMENT 1;

/* Build Table Structure */
CREATE TABLE cultivo
(
	codigo_cultivo INTEGER NOT NULL DEFAULT nextval('riego.cultivo_codigo_cultivo_seq'::regclass),
	descripcion_cultivo TEXT NOT NULL
) WITHOUT OIDS;

/* Table Items: cultivo */
ALTER TABLE cultivo ADD CONSTRAINT pkcultivo
	PRIMARY KEY (codigo_cultivo);

/******************** Add Table: ficha ************************/

/* Build Table Structure */
CREATE TABLE ficha
(
	codigo_tipo_ficha INTEGER NOT NULL,
	descripcion_ficha TEXT NOT NULL,
	rut VARCHAR(12) NOT NULL
) WITHOUT OIDS;

/* Table Items: ficha */
ALTER TABLE ficha ADD CONSTRAINT pkficha
	PRIMARY KEY (rut);

/******************** Add Table: hilera ************************/
CREATE SEQUENCE hilera_codigo_hilera_seq INCREMENT 1;

/* Build Table Structure */
CREATE TABLE hilera
(
	codigo_cuartel INTEGER NOT NULL,
	codigo_hilera INTEGER NOT NULL DEFAULT nextval('riego.hilera_codigo_hilera_seq'::regclass),
	codigo_variedad INTEGER NOT NULL,
	descripcion_hilera TEXT NOT NULL,
	superficie DOUBLE PRECISION NOT NULL
) WITHOUT OIDS;

/* Table Items: hilera */
ALTER TABLE hilera ADD CONSTRAINT pkhilera
	PRIMARY KEY (codigo_hilera);

/******************** Add Table: implemento ************************/
CREATE SEQUENCE implemento_codigo_implemento_seq INCREMENT 1;

/* Build Table Structure */
CREATE TABLE implemento
(
	codigo_implemento INTEGER NOT NULL DEFAULT nextval('implemento_codigo_implemento_seq'),
	descripcion_implemento TEXT NOT NULL
);

/* Table Items: implemento */
ALTER TABLE implemento ADD CONSTRAINT pkimplemento
	PRIMARY KEY (codigo_implemento);

/******************** Add Table: labor ************************/
CREATE SEQUENCE labor_codigo_labor_seq INCREMENT 1;

/* Build Table Structure */
CREATE TABLE labor
(
	codigo_labor INTEGER NOT NULL DEFAULT nextval('riego.labor_codigo_labor_seq'::regclass),
	descripcion_labor TEXT NOT NULL
) WITHOUT OIDS;

/* Table Items: labor */
ALTER TABLE labor ADD CONSTRAINT pklabor
	PRIMARY KEY (codigo_labor);

/******************** Add Table: labor_hilera ************************/

/* Build Table Structure */
CREATE TABLE labor_hilera
(
	codigo_hilera INTEGER NOT NULL,
	codigo_labor INTEGER NOT NULL,
	fecha DATE NOT NULL,
	rut VARCHAR(12) NOT NULL
) WITHOUT OIDS;

/* Table Items: labor_hilera */
ALTER TABLE labor_hilera ADD CONSTRAINT pklabor_hilera
	PRIMARY KEY (codigo_labor, codigo_hilera);

/******************** Add Table: maquinaria ************************/
CREATE SEQUENCE maquinaria_codigo_maquinaria_seq INCREMENT 1;

/* Build Table Structure */
CREATE TABLE maquinaria
(
	codigo_maquinaria INTEGER NOT NULL DEFAULT nextval('riego.maquinaria_codigo_maquinaria_seq'::regclass),
	descripcion_maquinaria TEXT NOT NULL
) WITHOUT OIDS;

/* Table Items: maquinaria */
ALTER TABLE maquinaria ADD CONSTRAINT pkmaquinaria
	PRIMARY KEY (codigo_maquinaria);

/******************** Add Table: producto ************************/
CREATE SEQUENCE producto_codigo_producto_seq INCREMENT 1;

/* Build Table Structure */
CREATE TABLE producto
(
	codigo_producto INTEGER NOT NULL DEFAULT nextval('riego.producto_codigo_producto_seq'::regclass),
	codigo_unidad INTEGER NOT NULL,
	descripcion_producto TEXT NOT NULL,
	dosis_propuesta FLOAT NOT NULL,
	codigo_unidad_dosis INTEGER NOT NULL
) WITHOUT OIDS;

/* Table Items: producto */
ALTER TABLE producto ADD CONSTRAINT pkproducto
	PRIMARY KEY (codigo_producto);

/******************** Add Table: sector ************************/
CREATE SEQUENCE sector_codigo_sector_seq INCREMENT 1;

/* Build Table Structure */
CREATE TABLE sector
(
	codigo_cultivo INTEGER NOT NULL,
	codigo_sector INTEGER NOT NULL DEFAULT nextval('riego.sector_codigo_sector_seq'::regclass),
	descripcion_sector TEXT NOT NULL
) WITHOUT OIDS;

/* Table Items: sector */
ALTER TABLE sector ADD CONSTRAINT pksector
	PRIMARY KEY (codigo_sector);

/******************** Add Table: tipo_ficha ************************/
CREATE SEQUENCE tipo_ficha_codigo_tipo_ficha_seq INCREMENT 1;

/* Build Table Structure */
CREATE TABLE tipo_ficha
(
	codigo_tipo_ficha INTEGER NOT NULL DEFAULT nextval('riego.tipo_ficha_codigo_tipo_ficha_seq'::regclass),
	descripcion_tipo_ficha TEXT NOT NULL
) WITHOUT OIDS;

/* Table Items: tipo_ficha */
ALTER TABLE tipo_ficha ADD CONSTRAINT pktipo_ficha
	PRIMARY KEY (codigo_tipo_ficha);

/******************** Add Table: unidad ************************/
CREATE SEQUENCE unidad_codigo_unidad_seq INCREMENT 1;

/* Build Table Structure */
CREATE TABLE unidad
(
	codigo_unidad INTEGER NOT NULL DEFAULT nextval('riego.unidad_codigo_unidad_seq'::regclass),
	descripcion_unidad TEXT NOT NULL
) WITHOUT OIDS;

/* Table Items: unidad */
ALTER TABLE unidad ADD CONSTRAINT pkunidad
	PRIMARY KEY (codigo_unidad);

/******************** Add Table: unidad_dosis ************************/
CREATE SEQUENCE unidad_dosis_codigo_unidad_dosis_seq INCREMENT 1;

/* Build Table Structure */
CREATE TABLE unidad_dosis
(
	codigo_unidad_dosis INTEGER NOT NULL DEFAULT nextval('unidad_dosis_codigo_unidad_dosis_seq'),
	descripcion_unidad_dosis TEXT NOT NULL
);

/* Table Items: unidad_dosis */
ALTER TABLE unidad_dosis ADD CONSTRAINT pkunidad_dosis
	PRIMARY KEY (codigo_unidad_dosis);

/******************** Add Table: variedad ************************/
CREATE SEQUENCE variedad_codigo_variedad_seq INCREMENT 1;

/* Build Table Structure */
CREATE TABLE variedad
(
	codigo_variedad INTEGER NOT NULL DEFAULT nextval('riego.variedad_codigo_variedad_seq'::regclass),
	descripcion_variedad TEXT NOT NULL
) WITHOUT OIDS;

/* Table Items: variedad */
ALTER TABLE variedad ADD CONSTRAINT pkvariedad
	PRIMARY KEY (codigo_variedad);


/************ Add Foreign Keys to Database ***************/

/************ Foreign Key: fk_aplicacion_ficha ***************/
ALTER TABLE aplicacion ADD CONSTRAINT fk_aplicacion_ficha
	FOREIGN KEY (rut) REFERENCES ficha (rut) ON DELETE NO ACTION;

/************ Foreign Key: fk_aplicacion_hilera ***************/
ALTER TABLE aplicacion ADD CONSTRAINT fk_aplicacion_hilera
	FOREIGN KEY (codigo_hilera) REFERENCES hilera (codigo_hilera) ON DELETE NO ACTION;

/************ Foreign Key: fk_aplicacion_implemento ***************/
ALTER TABLE aplicacion ADD CONSTRAINT fk_aplicacion_implemento
	FOREIGN KEY (codigo_implemento) REFERENCES implemento (codigo_implemento) ON DELETE NO ACTION;

/************ Foreign Key: fk_aplicacion_maquinaria ***************/
ALTER TABLE aplicacion ADD CONSTRAINT fk_aplicacion_maquinaria
	FOREIGN KEY (codigo_maquinaria) REFERENCES maquinaria (codigo_maquinaria) ON DELETE NO ACTION;

/************ Foreign Key: fk_aplicacion_producto ***************/
ALTER TABLE aplicacion ADD CONSTRAINT fk_aplicacion_producto
	FOREIGN KEY (codigo_producto) REFERENCES producto (codigo_producto) ON DELETE NO ACTION;

/************ Foreign Key: fk_cuartel_sector ***************/
ALTER TABLE cuartel ADD CONSTRAINT fk_cuartel_sector
	FOREIGN KEY (codigo_sector) REFERENCES sector (codigo_sector) ON DELETE NO ACTION;

/************ Foreign Key: fk_ficha_tipo_ficha ***************/
ALTER TABLE ficha ADD CONSTRAINT fk_ficha_tipo_ficha
	FOREIGN KEY (codigo_tipo_ficha) REFERENCES tipo_ficha (codigo_tipo_ficha) ON DELETE NO ACTION;

/************ Foreign Key: fk_hilera_cuartel ***************/
ALTER TABLE hilera ADD CONSTRAINT fk_hilera_cuartel
	FOREIGN KEY (codigo_cuartel) REFERENCES cuartel (codigo_cuartel) ON DELETE NO ACTION;

/************ Foreign Key: fk_hilera_variedad ***************/
ALTER TABLE hilera ADD CONSTRAINT fk_hilera_variedad
	FOREIGN KEY (codigo_variedad) REFERENCES variedad (codigo_variedad) ON DELETE NO ACTION;

/************ Foreign Key: fk_labor_hilera_ficha ***************/
ALTER TABLE labor_hilera ADD CONSTRAINT fk_labor_hilera_ficha
	FOREIGN KEY (rut) REFERENCES ficha (rut) ON DELETE NO ACTION;

/************ Foreign Key: fk_labor_hilera_hilera ***************/
ALTER TABLE labor_hilera ADD CONSTRAINT fk_labor_hilera_hilera
	FOREIGN KEY (codigo_hilera) REFERENCES hilera (codigo_hilera) ON DELETE NO ACTION;

/************ Foreign Key: fk_labor_hilera_labor ***************/
ALTER TABLE labor_hilera ADD CONSTRAINT fk_labor_hilera_labor
	FOREIGN KEY (codigo_labor) REFERENCES labor (codigo_labor) ON DELETE NO ACTION;

/************ Foreign Key: fk_producto_unidad ***************/
ALTER TABLE producto ADD CONSTRAINT fk_producto_unidad
	FOREIGN KEY (codigo_unidad) REFERENCES unidad (codigo_unidad) ON DELETE NO ACTION;

/************ Foreign Key: fk_producto_unidad_dosis ***************/
ALTER TABLE producto ADD CONSTRAINT fk_producto_unidad_dosis
	FOREIGN KEY (codigo_unidad_dosis) REFERENCES unidad_dosis (codigo_unidad_dosis) ON DELETE NO ACTION;

/************ Foreign Key: fk_sector_cultivo ***************/
ALTER TABLE sector ADD CONSTRAINT fk_sector_cultivo
	FOREIGN KEY (codigo_cultivo) REFERENCES cultivo (codigo_cultivo) ON DELETE NO ACTION;
