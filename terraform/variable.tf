variable "region" {
    description= "region of aws resources"
    type = string
    default ="us-east-1"
}

variable "az"{
    description= "Availability zone"
    type = string
    default = "us-east-1a"
}


variable "bucket_name" {
  description = "Name of s3 bucket"
  type        = string
}

variable "redshift_password" {
  description = "Password for the database in the Redshift cluster"
  type        = string
}

variable "redshift_cluster_name" {
  description = "Name of Redshift cluster"
  type        = string
}

variable "dbname" {
  description = "Name of Redshift cluster"
  type        = string
}
