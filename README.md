# covid19

Grabado de informacion horaria y diaria del avance del Covid19. 

Explotación de datos, simulación de casos y comparativas.


Docker
docker build -t "covid19:1.0" .
docker run --name testCovid covid19:1.0

OCP
oc new-project covid-analytics

oc new-build --name covid-world-app --binary --strategy docker

oc start-build covid-world-app --from-dir .

