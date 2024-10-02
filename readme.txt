#########  Project Overview  ########

This project uses Docker, Airflow, and Terraform to build and deploy infrastructure on AWS, manage ETL pipelines, and run tasks. Data is extracted from source http://planecrashinfo.com
Infrastructure provisioning through [Terraform](https://www.terraform.io/), containerized through [Docker](https://www.docker.com/) and orchestrated through [Airflow](https://airflow.apache.org/). 


###### Tasks ######

1. Scrape Data from Source: flightDataWebScrape.py
2. Validate, clean and initial data transfromation: dataValidate.py
3. Load data into a Redshift database: loadRedshift.py




###### Prerequisites ######

Before running the project, ensure that the following tools are installed on your system:

1. Configure AWS account through [AWS CLI](https://aws.amazon.com/cli/). [Reqruired for Terraform]
2. [Terraform](https://www.terraform.io/). [Required to provision AWS services]
3. [Docker / Docker-Compose](https://www.docker.com/). [Required to run Airflow DAG / pipeline]
4. Install make / gmake to run make file
5. airflow/tasks/credentials.conf: You need to manually input your AWS S3 access key and secret key in this file after running the build_infra command.

Additional Notes
Ensure your AWS credentials are correctly configured before running build_infra.
If any issues arise during the execution of Terraform or Docker commands, consult the logs or verify your AWS permissions and Docker installation.
flightDataWebScrape.py would slowly extract data on website to ensure not exceeding request limit, this process would take around 3 hours.


###### Run Pipeline ######

	`make run_container`	    Init docker-compose and run container"
	`make stop`    			    Stop and remove all docker volumnes"
	`make build_infra`      	Builds AWS infrastructures using terraform"
	`make destroy_infra`        Destroy all the infrastructures created on AWS"