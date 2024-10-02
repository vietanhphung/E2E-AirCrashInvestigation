help:
	@echo "  run_container:		Init docker-compose and run container"
	@echo "  stop:     			Stop and remove all docker volumnes"
	@echo "  build_infra      	Builds AWS infrastructures using terraform"
	@echo "  destroy_infra      Destroy all the infrastructures created on AWS"


run_container:
	cd airflow && docker-compose up airflow-init
	cd airflow && docker-compose up -d
	@echo "opening interface..."
	@echo  '#####                     (33%)\r'
	@sleep 10
	@echo  '#############             (66%)\r'
	@sleep 10
	@echo  '#######################   (99%)\r'
	@open http://0.0.0.0:8080/
	@echo "default username and password is 'airflow', please refresh browser if not loaded"

stop:
	cd airflow && docker-compose down -v

build_infra:
	cd terraform && terraform plan
	cd terraform && terraform apply
	cd terraform && terraform output > ../airflow/tasks/pipeline.conf
	@echo Enter AWS S3 access key and secret key in airflow/tasks/credentials.conf



destroy_infra:
	cd terraform && terraform destroy


