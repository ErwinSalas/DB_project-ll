--centralDB SQL SCRIPT
CREATE TABLE usuarios(
	idUsuario integer not null,
	nombre varchar(15),
	apellido1 varchar(15),
	apellido2 varchar(15),
	CONSTRAINT PK_idUsuario_usuarios PRIMARY KEY(idUsuario)
);
CREATE TABLE sedes( --cada "nodo-sede" tiene servicios diferentes, se encuentran reg en en el servidor central
	idSede integer not null,
	nombre varchar(15),
	ubicacion varchar(15),
	CONSTRAINT PK_idSede_sedes PRIMARY KEY(idSede)
);

CREATE TABLE reservas(
	idReserva serial,
	idSede integer,
	idUsuario integer,
	montoTotal integer,
	fecha date, --idx
	CONSTRAINT PK_idReservas_reservas PRIMARY KEY(idReserva),
	CONSTRAINT FK_idSede_sedes FOREIGN KEY(idSede) REFERENCES sedes,
	CONSTRAINT FK_idUsuario_usuarios FOREIGN KEY(idUsuario) REFERENCES usuarios
);
CREATE EXTENSION dblink;
----------------------------------------------------------------------------------------------
--------------------------------------DATA CENTRAL SERVER-------------------------------------
----------------------------------------------------------------------------------------------
--FUNCTIONS:
--INSERTS 'N' RANDOM RESERVATIONS INTO centralDB & nodeI

CREATE OR REPLACE FUNCTION insReservacionN(i int)RETURNS VOID
AS
$$
DECLARE
	p_idUsuario int;
	p_idSede int; --pueden variar las sedes entonces genérico
	p_montoTotal int;
	p_fecha date;
	p_costo int;
	p_idServicio int;
	p_cantidad int;
	currentID int;
BEGIN
	WHILE (i>1) LOOP
		p_idUsuario = (select(floor(random() * (select count(*) from usuarios) + 1)::int));
		p_idSede = 2; --x el momento solo el nodo 2 está habilitado
		p_costo = (select( floor ( random() * 1000 + 35)::int));
		p_fecha = cast((now() + '1 year'::interval * random()) as date);
		p_idServicio = (select ( floor( random() * (select * from dblink ('host=localhost user=postgres password=aniram dbname=nodeII',
				'select count(*) from servicios') as cant_reg(cant int))+1)::int));
		p_cantidad = (select ( floor (random()* 6 + 2)::int));
		currentID = cast((SELECT currval('reservas_idReserva_seq')) as integer)+1;
		p_montoTotal = p_costo * p_cantidad;
		INSERT INTO reservas(idSede, idUsuario, montoTotal, fecha) VALUES (p_idSede, p_idUsuario, p_montoTotal, p_fecha);
		PERFORM dblink('host=localhost user=postgres password=aniram dbname=nodeII', --aquí va la sede
			FORMAT('INSERT INTO servicios_reservas VALUES (%s,%s,%s,%s)',
			p_idServicio,currentID,p_cantidad, p_costo));
		i = i-1;
	END LOOP;
END;
$$
LANGUAGE PLPGSQL;
---------------------------------------------OPERACIONES ESPECIFICAS----------------------------------

---------------------------------------------insert----------------------------------
CREATE OR REPLACE FUNCTION insReservacion(
	--p_idReserva int, --SERIAL
	p_idUsuario int,
	p_idSede int, --pueden variar las sedes entonces genérico
	p_costo int,
	p_idServicio int,
	p_cantidad int)RETURNS VOID
AS
$$
DECLARE
	p_montoTotal int;
	currentID int;
	p_fecha date;

BEGIN
	--hacer cases para todas las sedes cuando se tengan las bd
	CASE p_idSede
	--if sede = x : dbname=?--
		WHEN 2 THEN --nodoII
			--consulta dist
			p_montoTotal=p_costo*p_cantidad;
			p_fecha = cast((now() + '1 year'::interval * random()) as date);
			currentID = cast((SELECT currval('reservas_idReserva_seq')) as integer)+1;--para saber por cuál índice va la tabla (SERIAL TYPE)
			INSERT INTO reservas(idSede, idUsuario, montoTotal, fecha) VALUES (p_idSede, p_idUsuario, p_montoTotal, p_fecha);

			PERFORM dblink('host=localhost user=postgres password=postgres dbname=nodeII', --aquí va la sede
				    FORMAT('INSERT INTO servicios_reservas VALUES
				    (%s,%s,%s,%s)',p_idServicio,currentID,p_cantidad, p_costo));
		WHEN 3 THEN --nodoIII

			p_montoTotal=p_costo*p_cantidad;
			p_fecha = cast((now() + '1 year'::interval * random()) as date); --inserta de la fecha de hoy en adelante
			currentID = cast((SELECT currval('reservas_idReserva_seq')) as integer)+1;
			PERFORM dblink('host=localhost user=postgres password=postgres dbname=nodeIII', --aquí va la sede
				    FORMAT('INSERT INTO servicios_reservas VALUES
				    (%s,%s,%s,%s)',p_idServicio,currentID,p_cantidad, p_costo));
			INSERT INTO reservas(idSede, idUsuario, montoTotal, fecha) VALUES (p_idSede, p_idUsuario, p_montoTotal, p_fecha);
		--WHEN X THEN -- INSERT INTO DATABASE REQUIRED.
	END CASE;

END;
$$
LANGUAGE PLPGSQL;
---------------------------------------------delete----------------------------------
CREATE OR REPLACE FUNCTION delReservacion(
	--p_idReserva int, --SERIAL
	p_idReservacion int
	)RETURNS VOID
AS
$$
BEGIN
	--hacer cases para todas las sedes cuando se tengan las bd
	delete from reservas r where r.idReserva=p_idReservacion;
	PERFORM dblink('host=localhost user=postgres password=postgres dbname=nodeII', --aquí va la sede
				    FORMAT('DELETE from servicios_reservas sr where sr.idReserva = %s'
				    ,p_idReservacion));

END;
$$
LANGUAGE PLPGSQL;
---------------------------------------------update----------------------------------
CREATE OR REPLACE FUNCTION updReservacion( --hacer cases para todas las sedes
	p_idReserva int,
	p_idServicio int,
	p_cantidad int
	)RETURNS VOID
AS
$$
DECLARE
	p_costo int;
	p_fecha date;
	--p_idSede int; indica a cual servidor conectarse
BEGIN
	--p_idSede = (select idSede from reservas where idReserva = p_idReserva);
	--case p_idSede
	--when 2: conectarse a 'n' sede para su modificacion
	p_costo = (select( floor ( random() * 1000 + 35)::int));
	p_fecha = cast((now() + '1 year'::interval * random()) as date);
	PERFORM dblink('host=localhost user=postgres password=postgres dbname=nodeii', --aquí va la sede
		    FORMAT('update servicios_reservas set idServicio = %s, cantidadPersonas= %s, costo= %s where idReserva = %s'
		    ,p_idServicio,p_cantidad, p_costo, p_idReserva));
	update reservas set montoTotal = p_costo*p_cantidad, fecha=p_fecha
		where idReserva = p_idReserva;
END;
$$
LANGUAGE plpgsql;

---------------------------------------------DATA---------------------------------------------
---------------------------------------LOCATIONS REGISTER centralBD---------------------------
INSERT INTO usuarios values (1,'CHRISTIAN', 'SANCHEZ', 'SALAS'); --PRIMER DATO QUEMADO INSERTADO EN nodeII
INSERT INTO sedes(idSede, nombre, ubicacion) values(1, 'C.TURISTICO A', 'SAN_JOSE');
INSERT INTO sedes(idSede, nombre, ubicacion) values(2, 'C.TURISTICO B', 'ALAJUELA');
INSERT INTO sedes(idSede, nombre, ubicacion) values(3, 'C.TURISTICO C', 'CARTAGO');
INSERT INTO sedes(idSede, nombre, ubicacion) values(4, 'C.TURISTICO D', 'HEREDIA');
INSERT INTO sedes(idSede, nombre, ubicacion) values(5, 'C.TURISTICO E', 'GUANACASTE');
INSERT INTO sedes(idSede, nombre, ubicacion) values(6, 'C.TURISTICO F', 'PUNTARENAS');
INSERT INTO sedes(idSede, nombre, ubicacion) values(7, 'C.TURISTICO G', 'LIMON');
--------------------------------------RESERVATIONS centralBD----------------------------------
--SELECT * from usuarios limit 10
--SELECT * from reservas

--DATO ID SERIAL, SE DEBE INICIALIZAR SECUENCIA INGRENSANDO UN PRIMER DATO QUEMADO.
insert into reservas (idSede, idUsuario, montoTotal, fecha)values(2, 1, 800,'01-10-2018');
SELECT insReservacionN(100000); --INSERTA 'n' CANTIDAD DE RESERVACIONES
--select delReservacion(100);
--select updReservacion(1,199,3) --IDRESERVA, IDSERVICIO, CANTIDADPERSONAS (también se modifica la fecha a otra aleatoria)
--select count(*) from usuarios
--select count(*) from reservas
--select count(*) from sedes

--------------------------------------QUERIES centralBD-------------------------------------------------

--HAY QUE CREAR OTROS SERVIDORES DE MANERA QUE LAS CONSULTAS CONSIDEREN TODAS LAS BD
--TODAS LAS CONSULTAS SE REALIZAN DESDE centralDB
--PARA ESTAS CONSULTAS SOLO SE ESTÁ CONSULTANDO centralDB & nodeII

--servicios-reservas más caros --idx costo
select * from dblink('host=localhost user=postgres password=aniram dbname=nodeII',
		'select s.idServicio, s.nombre, sr.costo from servicios s inner join
		servicios_reservas sr on s.idServicio=sr.idServicio where sr.costo>=900 order by sr.costo desc limit 100 ') as serviciosCostosII(idServicio int, nombre varchar(20), costo int)
union
select * from dblink('host=localhost user=postgres password=aniram dbname=nodeIII',
		'select s.idServicio, s.nombre, sr.costo from servicios s inner join
		servicios_reservas sr on s.idServicio=sr.idServicio where sr.costo>=900 order by sr.costo desc limit 100') as serviciosCostosIII(idServicio int, nombre varchar(20), costo int);

---------------------------------------------------------------------------------------------------------
--usuarios por tipo de preferencia--idx tipo
--explain analyze



--servicios-reservas más caros --idx costo
-----------------------------------------------------------------------------------------------------------ingresos de cada sede en un tiempo x
CREATE OR REPLACE FUNCTION servisiosMasCaros() --idx fecha
AS
$$
BEGIN

    select uc.idUsuario, uc.nombre from usuarios uc inner join
    (select * from dblink('host=localhost user=postgres password=aniram dbname=nodeII',
            'select * from usuarios u where u.preferencia = ''tipo1'' ') as
            usr_node(
            idUsuario int,
            email varchar(20),
            psswrd varchar(10),
            preferencia varchar(15)) limit 200) usr_nodeII on uc.idUsuario=usr_nodeII.idUsuario
    inner join
    (select * from dblink('host=localhost user=postgres password=aniram dbname=nodeIII',
            'select * from usuarios u where u.preferencia = ''tipo1'' ') as
            usr_node(
            idUsuario int,
            email varchar(20),
            psswrd varchar(10),
            preferencia varchar(15)) limit 200)usr_nodeIII on uc.idUsuario = usr_nodeIII.idUsuario; --asignar para una preferencia de un usuario espec

END;
$$
LANGUAGE plpgsql;
-----------------------------------------------------------------------------------------------------------ingresos de cada sede en un tiempo x

--usuarios por tipo de preferencia--idx tipo
--explain analyze
CREATE OR REPLACE FUNCTION usuariosPorPreferencia() --idx fecha
AS
$$
BEGIN
    select uc.idUsuario, uc.nombre from usuarios uc inner join
    (select * from dblink('host=localhost user=postgres password=aniram dbname=nodeII',
            'select * from usuarios u where u.preferencia = ''tipo1'' ') as
            usr_node(
            idUsuario int,
            email varchar(20),
            psswrd varchar(10),
            preferencia varchar(15)) limit 200) usr_nodeII on uc.idUsuario=usr_nodeII.idUsuario
    inner join
    (select * from dblink('host=localhost user=postgres password=aniram dbname=nodeIII',
            'select * from usuarios u where u.preferencia = ''tipo1'' ') as
            usr_node(
            idUsuario int,
            email varchar(20),
            psswrd varchar(10),
            preferencia varchar(15)) limit 200)usr_nodeIII on uc.idUsuario = usr_nodeIII.idUsuario; --asignar para una preferencia de un usuario espec

END;
$$
LANGUAGE plpgsql;
---------------------------------------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION ingresosSede(p_idSede int, p_fechaA date, p_fechaB date, out result int) --idx fecha
AS
$$
BEGIN
	select sum(r.montoTotal) as ingresosSede2
	from reservas r
	where r.idSede=p_idSede and r.fecha between p_fechaA and p_fechaB group by r.idSede
	into result;
END;
$$
LANGUAGE plpgsql;


select sum(r.montoTotal) as ingresosSede2  --modificar consulta
	from reservas r
	where r.idSede=2 and r.fecha between '2018-01-01' and '2019-12-30' group by r.idSede

select *
from reservas r

select *
from reservas r
where r.fecha>'2018-01-01' and r.fecha>'2019-12-31'
limit 10

--select ingresosSede(2, '2018-01-01', '2019-02-20');
---------------------------------------------------INDEXES------------------------------------------------------
--select * from reservas limit 20
--select count(*) from reservas
--CREATE index idx_fecha_reservas on reservas(fecha);
---------------------------------------------------CRECIMIENTO BD-----------------------------------------------

