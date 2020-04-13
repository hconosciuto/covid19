-- Table: public.infectadosxdia

-- DROP TABLE public.infectadosxdia;

CREATE TABLE public.infectadosxdia
(
  dia date,
  pais character varying(40),
  infecxdia bigint
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.infectadosxdia
  OWNER TO pi;
