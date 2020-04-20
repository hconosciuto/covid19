-- Table: public.covid19

-- DROP TABLE public.covid19;

CREATE TABLE covid19
(
  fecha timestamp without time zone,
  pais character varying(40),
  infectados integer,
  muertes integer,
  recuperados integer,
  porcentaje_muertes double precision,
  porcentaje_recuperados double precision,
  inf_por_millon integer,
  mue_por_millon integer
)
WITH (
  OIDS=FALSE
);
ALTER TABLE covid19
  OWNER TO pi;
