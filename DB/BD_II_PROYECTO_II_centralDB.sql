create database centralDB;
use postgres
CREATE TABLE usuarios(
	idUsuario integer not null,
	nombre varchar(15),
	apellido1 varchar(15),
	apellido2 varchar(15),
	CONSTRAINT PK_idUsuario_usuarios PRIMARY KEY(idUsuario)
)
CREATE TABLE sedes( --cada "nodo-sede" tiene servicios diferentes, se encuentran reg en en el servidor central
	idSede integer not null,
	nombre varchar(15),
	ubicacion varchar(15),
	CONSTRAINT PK_idSede_sedes PRIMARY KEY(idSede)
)
--drop table reservas
CREATE TABLE reservas(
	idReserva integer not null,
	idSede integer,
	idUsuario integer,
	montoTotal integer, --calculo sobre consulta distribuida
	fecha date,
	CONSTRAINT PK_idReservas_reservas PRIMARY KEY(idReserva),
	CONSTRAINT FK_idSede_sedes FOREIGN KEY(idSede) REFERENCES sedes,
	CONSTRAINT FK_idUsuario_usuarios FOREIGN KEY(idUsuario) REFERENCES usuarios
)
CREATE EXTENSION dblink;
----------------------------------------------------------------------------------------------
--------------------------------------DATA CENTRAL SERVER-------------------------------------
----------------------------------------------------------------------------------------------
--FUNCTIONS:

--drop function insReservacion(integer, integer, integer, date, integer, integer);
--INSERTS RESERVATIONS INTO centralDB & nodeI 
CREATE OR REPLACE FUNCTION insReservacion(
	p_idReserva int, 
	p_idUsuario int, 
	p_idSede int, --pueden variar las sedes entonces genérico
	p_fecha date, 
	p_idServicio int, 
	p_cantidad int)RETURNS VOID
AS
$$
DECLARE
	p_montoTotal int; 
	costo int;

BEGIN
	--hacer cases para todas las sedes cuando se tengan las bd
	CASE p_idSede
	--if sede = x : dbname=?--
		WHEN 2 THEN --nodoII
			costo = (SELECT s.costo FROM (SELECT * FROM dblink('host=localhost user=postgres password=aniram dbname=nodeII',
					FORMAT('SELECT costo FROM servicios where idServicio = %s', p_idServicio))AS servicios(costo int))AS s);
			p_montoTotal=costo*p_cantidad;
			INSERT INTO reservas(idReserva, idSede, idUsuario, montoTotal, fecha) VALUES (p_idReserva, p_idSede, p_idUsuario, p_montoTotal, p_fecha);
			PERFORM dblink('host=localhost user=postgres password=aniram dbname=nodeII', --aquí va la sede
				    FORMAT('INSERT INTO servicios_reservas VALUES 
				    (%s,%s,%s)',p_idServicio,p_idReserva,p_cantidad));
		WHEN 3 THEN --nodoIII
			costo = (SELECT s.costo FROM (SELECT * FROM dblink('host=localhost user=postgres password=aniram dbname=nodeIII',
					FORMAT('SELECT costo FROM servicios where idServicio = %s', p_idServicio))AS servicios(costo int))AS s);
			p_montoTotal=costo*p_cantidad;
			INSERT INTO reservas(idReserva, idSede, idUsuario, montoTotal, fecha) VALUES (p_idReserva, p_idSede, p_idUsuario, p_montoTotal, p_fecha);
			PERFORM dblink('host=localhost user=postgres password=aniram dbname=nodeIII', --aquí va la sede
				    FORMAT('INSERT INTO servicios_reservas VALUES 
				    (%s,%s,%s)',p_idServicio,p_idReserva,p_cantidad));
		--WHEN X THEN -- INSERT INTO DATABASE REQUIRED.
	END CASE; 
	
END;
$$
LANGUAGE PLPGSQL;
---------------------------------------LOCATIONS REGISTER centralBD---------------------------
INSERT INTO sedes(idSede, nombre, ubicacion) values(1, 'C.TURISTICO A', 'SAN_JOSE');
INSERT INTO sedes(idSede, nombre, ubicacion) values(2, 'C.TURISTICO B', 'ALAJUELA');
INSERT INTO sedes(idSede, nombre, ubicacion) values(3, 'C.TURISTICO C', 'CARTAGO');
INSERT INTO sedes(idSede, nombre, ubicacion) values(4, 'C.TURISTICO D', 'HEREDIA');
INSERT INTO sedes(idSede, nombre, ubicacion) values(5, 'C.TURISTICO E', 'GUANACASTE');
INSERT INTO sedes(idSede, nombre, ubicacion) values(6, 'C.TURISTICO F', 'PUNTARENAS');
INSERT INTO sedes(idSede, nombre, ubicacion) values(7, 'C.TURISTICO G', 'LIMON');
--------------------------------------RESERVATIONS centralBD----------------------------------
--SELECT * from usuarios
--SELECT * from reservas
--delete from reservas where idReserva= 1
SELECT insReservacion(1, 1, 2, '3-1-2018', 1, 2); --RESERVACION 1, USUARIO 1 (CHRISTIAN), SEDE 2 (ALAJUELA), FECHA, SERVICIO, CANTIDAD

--------------------------------------QUERIES centralBD----------------------------------------
/*
demanda de servicios d c/sede orden desc
sedes con mayor cantidad de reservas
ingresos de cada sede en un tiempo x

*/
