-- Table: public.infectadosxdia

-- DROP TABLE public.infectadosxdia;

CREATE TABLE infectadosxdia
(
  dia date,
  pais character varying(40),
  infecxdia bigint
)
WITH (
  OIDS=FALSE
);
ALTER TABLE infectadosxdia
  OWNER TO pi;
