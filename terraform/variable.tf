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

variable "redshift_password" {
  description = "Password for the database in the Redshift cluster"
  type        = string
}