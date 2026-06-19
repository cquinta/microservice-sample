docker network rm microservices
docker network create microservices
docker run --network microservices --name mssum -p 8001:80 -d cquinta/mssum
docker run --network microservices --name mssub -p 8002:80 -d cquinta/mssub
docker run --network microservices --name msapi -p 8000:80 -d cquinta/calcapi


