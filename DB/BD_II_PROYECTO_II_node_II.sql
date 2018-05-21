--nodeII SQL QUERY
use nodeII
CREATE TABLE usuarios(
	idUsuario serial,
	email varchar(20) check (email similar to ('[A-z]%@[A-z]%.[A-z]%')),
	psswrd varchar(10),
	preferencia varchar(15),
	CONSTRAINT PK_idUsuario PRIMARY KEY(idUsuario)
);
CREATE TABLE servicios(
	idServicio integer not null,
	nombre varchar(20),
	idSede integer,
	img bytea,
	tipo varchar(15), --idx-
	CONSTRAINT PK_idServicio_servicios PRIMARY KEY(idServicio)
);

CREATE TABLE servicios_reservas(
	idServicio integer,
	idReserva integer,
	cantidadPersonas integer, --new
	costo integer, --idx
	CONSTRAINT PK_idServicio_idReserva PRIMARY KEY(idReserva, idServicio),
	CONSTRAINT FK_idServicio_servicios FOREIGN KEY(idServicio) REFERENCES servicios
);

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
--debe haber al menos 1 usr insertado a pata para q la función corra bien, x ser atributo serial debe estar inicializado
--en cada sesion
--INSERTA N CANTIDAD DE USUARIOS ALEATORIOS
CREATE OR REPLACE FUNCTION insUsr(i int)RETURNS VOID
AS
$$
DECLARE
	p_idUsr int;
	p_email varchar(20);
	p_emailid int;
	p_psswrd varchar(10);
	p_preferencia varchar(15);
	p_nombre varchar(15);
	p_apellido1 varchar(20);
	p_apellido2 varchar(15);

BEGIN
	WHILE (i>1) LOOP --TRYCATCH:--posible error d indices al almacenar otro nodo
		p_idUsr = cast((select currval('usuarios_idUsuario_seq')+1)as int);
		p_email = 'xxx@xxx'||cast(p_idUsr as varchar(10))||'.com'; --verificar que idusr quede igual en int
		p_psswrd = 'ab'||cast(p_idUsr as varchar(10))||'z';
		p_preferencia = 'tipo'||(select cast((floor(random() * 3 + 1)::int) as varchar(1))) ;
		p_nombre = 'USR'||cast(p_idUsr as varchar(10));
		p_apellido1 ='A1_'||cast(p_idUsr as varchar(10));
		P_apellido2 ='A2_'||cast(p_idUsr as varchar(10));
		PERFORM dblink('host=localhost user=postgres password=postgres dbname=centralDB',
				FORMAT('INSERT INTO usuarios VALUES
				(%s,''%s'',''%s'',''%s'')', p_idUsr, p_nombre,p_apellido1,p_apellido2));
		INSERT INTO usuarios (email, psswrd, preferencia) VALUES (p_email, p_psswrd, p_preferencia);
		i = i-1;
	END LOOP;
END;
$$
LANGUAGE PLPGSQL;

CREATE OR REPLACE FUNCTION insServicio( i int )RETURNS VOID
AS
--verificar que en otros nodos no hayan mismos pk_idServicio
--empezar contador desde el último id en este servidor
$$
DECLARE
	p_idServicio int;
	p_nombre varchar(20);
	p_idSede int;
	p_costo int;
	p_img bytea;
	p_tipo varchar(15);


BEGIN
	p_idServicio = 1; --otros nodos deben empezar desde el último índice agregado
	WHILE( p_idServicio <= i )LOOP
		p_nombre = 'SERVICIO'||cast(p_idServicio as varchar(10));
		p_idSede = 2; --cambiar este parámetro en otros nodos
		p_costo = (SELECT floor (random() * 45000 + 15000)::int);
		p_img = (SELECT bytea_import('/home/erwin-salas/Imágenes'));
		p_tipo = 'tipo'||(select cast((floor(random() * 3 + 1)::int) as varchar(1))) ;
		INSERT INTO servicios values(p_idServicio, p_nombre, p_idSede, p_img, p_tipo);
		p_idServicio = p_idServicio + 1;
	END LOOP;


END;
$$
LANGUAGE PLPGSQL;
----------------------------------SERVICES FOR nodeII (idSede: 2)----------------------------------
SELECT insServicio(500);
--select * from servicios
----------------------------------USERS FOR nodeII (idSede: 2)-------------------------------------
--delete from usuarios
--INSERT INTO usuarios(email, psswrd, preferencia) VALUES ('xxx@xxx.com','123a','tipo1');
SELECT insUsr(10008); -- 10008 mil reg actuales
--select count(*) from usuarios
--SELECT pg_size_pretty( pg_total_relation_size('usuarios') );
-------------------------------------SERVICIOS-RESERVAS--------------------------------------------------------------
--insert into servicios_reservas values(1, 1, 2, 400);--primer dato desde central
select * from servicios_reservas limit 200
--select count(*) from servicios_reservas

---------------------------------------------------INDEXES------------------------------------------------------
--CREATE index idx_tipo_servicio on servicios(tipo)
--CREATE index idx_costo_serviciosreservas on servicios_reservas(costo)

