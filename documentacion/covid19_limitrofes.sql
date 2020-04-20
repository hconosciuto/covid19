-- View: public.covid19_limitrofes

-- DROP VIEW public.covid19_limitrofes;

CREATE OR REPLACE VIEW public.covid19_limitrofes AS 
 SELECT date(covid19.fecha) AS dia,
    covid19.pais,
    max(covid19.infectados) AS infectados,
    max(covid19.muertes) AS muertes,
    max(covid19.inf_por_millon) AS inf_por_millon,
    max(covid19.mue_por_millon) AS mue_por_millon
   FROM covid19
  WHERE covid19.pais in = ('Argentina', 'Brazil', 'Bolivia', 'Chile', 'Paraguay', 'Uruguay')
  GROUP BY (date(covid19.fecha)), covid19.pais
  ORDER BY covid19.pais, (date(covid19.fecha));
