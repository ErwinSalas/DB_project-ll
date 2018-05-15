--nodeI SQL QUERY
CREATE TABLE usuarios(
	idUsuario integer not null,
	email varchar(50) check (email similar to ('[A-z]%@[A-z]%.[A-z]%')),
	psswrd varchar(10),
	CONSTRAINT PK_idUsuario PRIMARY KEY(idUsuario)
);
CREATE TABLE servicios(
	idServicio integer not null,
	nombre varchar(20),
	idSede integer,
	costo integer,
	img bytea,  
	CONSTRAINT PK_idServicio_servicios PRIMARY KEY(idServicio)
);
CREATE TABLE servicios_reservas(
	idServicio integer,
	idReserva integer,
	cantidadPersonas integer, --new
	CONSTRAINT PK_idServicio_idReserva PRIMARY KEY(idReserva, idServicio),
	CONSTRAINT FK_idServicio_servicios FOREIGN KEY(idServicio) REFERENCES servicios
);
--drop table usuarios
--drop table servicios_reservas
--drop table servicios
CREATE EXTENSION dblink;
--------------------------------------------DATA NODE 1---------------------------------------
--IMPORTS BINARY FILE FOR bytea TYPE
CREATE OR REPLACE FUNCTION bytea_import(p_path TEXT, p_result OUT bytea) 
LANGUAGE plpgsql AS 
$$
DECLARE
  l_oid oid;
BEGIN
  SELECT lo_import(p_path) INTO l_oid;
  SELECT lo_get(l_oid) INTO p_result;
  PERFORM lo_unlink(l_oid);
END;$$;
----------------------------------------------------------------------------------------------
--INSERTS USERS INTO nodeI & centralDB
CREATE OR REPLACE FUNCTION newUser(idUsuario int, email varchar(50), psswrd varchar(10), nombre varchar(15), apellido1 varchar(15), apellido2 varchar(15))
RETURNS RECORD
AS
$$
	INSERT INTO usuarios VALUES (idUsuario, email, psswrd);
	--INSERT centralDB
	SELECT dblink('host=localhost user=postgres password=aniram dbname=centralDB', 
		    FORMAT('INSERT INTO usuarios VALUES 
		    (%s,''%s'',''%s'',''%s'')',idUsuario,nombre,apellido1,
			apellido2)); 
$$
LANGUAGE SQL;
----------------------------------SERVICES FOR nodeI (idSede: 2)----------------------------------
INSERT INTO servicios(idServicio, nombre, idSede, costo, img) values(6, 'Hospedaje', 2, 15000, (SELECT bytea_import('C:\Users\CHRISTIAN\Documents\TEC\2018 I SEM\BASES DE DATOS II\postgresql.png')));
INSERT INTO servicios(idServicio, nombre, idSede, costo, img) values(7, 'Alimentacion', 2, 15000, (SELECT bytea_import('C:\Users\CHRISTIAN\Documents\TEC\2018 I SEM\BASES DE DATOS II\postgresql.png')));
INSERT INTO servicios(idServicio, nombre, idSede, costo, img) values(8, 'Cabalgata', 2, 25000, (SELECT bytea_import('C:\Users\CHRISTIAN\Documents\TEC\2018 I SEM\BASES DE DATOS II\postgresql.png')));
INSERT INTO servicios(idServicio, nombre, idSede, costo, img) values(9, 'Rafting', 2, 25000, (SELECT bytea_import('C:\Users\CHRISTIAN\Documents\TEC\2018 I SEM\BASES DE DATOS II\postgresql.png')));
INSERT INTO servicios(idServicio, nombre, idSede, costo, img) values(0, 'Tour_Guiado', 2, 10000, (SELECT bytea_import('C:\Users\CHRISTIAN\Documents\TEC\2018 I SEM\BASES DE DATOS II\postgresql.png')));

----------------------------------USERS FOR nodeI (idSede: 2)-------------------------------------

select newUser(6, 'xxx@xxx.com','123a','USR6','A1','A2');
select newUser(7, 'xxx@xxx.com','123b','USR7','A1','A2');
select newUser(8, 'xxx@xxx.com','123c','USR8','A1','A2');
select newUser(9, 'xxx@xxx.com','123d','USR9','A1','A2');
select newUser(0, 'xxx@xxx.com','123e','USR0','A1','A2');

---------------------------------------------------------------------------------------------------