build:
	docker-compose -f infra_setup/infra_spark/docker-compose-spark.yml build
build-infra:
	docker-compose -f infra_setup/docker-compose-infra.yml build
build-yarn:
	docker-compose -f docker-compose.yarn.yml build

build-yarn-nc:
	docker-compose -f docker-compose.yarn.yml build --no-cache

build-nc:
	docker-compose -f infra_setup/infra_spark/docker-compose-spark.yml build --no-cache

build-progress:
	docker-compose build --no-cache --progress=plain

down:
	docker-compose -f infra_setup/infra_spark/docker-compose-spark.yml down --volumes --remove-orphans

down_infra:
	docker-compose -f infra_setup/infra/docker-compose-infra.yml down --volumes --remove-orphans
down-yarn:
	docker-compose -f docker-compose.yarn.yml down --volumes --remove-orphans

run:
	make down && docker-compose -f infra_setup/infra_spark/docker-compose-spark.yml up
run-infra:
	make down_infra && docker-compose -f infra_setup/infra/docker-compose-infra.yml up
run-infra-d:
	docker-compose -f infra_setup/infra/docker-compose-infra.yml up -d
run-scaled:
	make down && docker-compose -f infra_setup/docker-compose-spark.yml up --scale spark-worker=3

run-d:
	docker-compose -f infra_setup/infra_spark/docker-compose-spark.yml up -d


stop:
	docker-compose -f infra_setup/docker-compose-spark.yml stop


submit:
	docker exec spark-master spark-submit --master spark://spark-master:7077 --deploy-mode client ./apps/$(app)

submit-da-book:
	make submit app=$(app)


rm-results:
	rm -r book_data/results/*