-- Table: public.covid19_tasa_inf

-- DROP TABLE public.covid19_tasa_inf;

CREATE TABLE covid19_tasa_inf
(
  fecha timestamp without time zone,
  pais character varying(40),
  infectados integer,
  infectadosxhora integer
)
WITH (
  OIDS=FALSE
);
ALTER TABLE covid19_tasa_inf
  OWNER TO pi;
