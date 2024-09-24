terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Configure the AWS Provider
provider "aws" {
  region = var.region
}

# Create a VPC to host the Redshift cluster
resource "aws_vpc" "flightanalysis" {
  cidr_block = "10.0.0.0/16"
  tags = {
    Name = "flightanalysis-vpc"
  }
}

# Create a subnet for the Redshift cluster
resource "aws_subnet" "flightanalysis" {
  vpc_id                  = aws_vpc.flightanalysis.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = var.az
  tags = {
    Name = "flightanalysis-subnet"
  }
}

# Internet Gateway for public access
resource "aws_internet_gateway" "flightanalysis" {
  vpc_id = aws_vpc.flightanalysis.id

  tags = {
    Name = "flightanalysis-igw"
  }
}

# Route Table to direct traffic to the internet
resource "aws_route_table" "flightanalysis" {
  vpc_id = aws_vpc.flightanalysis.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.flightanalysis.id
  }

  tags = {
    Name = "flightanalysis-route-table"
  }
}

# Associate the route table with the subnet
resource "aws_route_table_association" "flightanalysis" {
  subnet_id      = aws_subnet.flightanalysis.id
  route_table_id = aws_route_table.flightanalysis.id
}

# Security Group to allow inbound traffic (e.g., public access on port 5439)
resource "aws_security_group" "flightanalysis_redshift_sg" {
  name        = "flightanalysis-redshift-sg"
  description = "Allow public access to Redshift cluster"
  vpc_id      = aws_vpc.flightanalysis.id

  ingress {
    from_port   = 5439
    to_port     = 5439
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # Public access
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "flightanalysis-redshift-sg"
  }
}

# Create an S3 bucket
resource "aws_s3_bucket" "flightanalysis" {
  bucket = "flightdatabucket1"
  force_destroy = true
  tags = {
    Name        = "flightanalysis-bucket"
    Environment = "Dev"
  }
}

# IAM Role for Redshift to access S3
resource "aws_iam_role" "flightanalysis_redshift_role" {
  name = "flightanalysis-redshift-s3-access-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action    = "sts:AssumeRole",
        Effect    = "Allow",
        Principal = {
          Service = "redshift.amazonaws.com"
        }
      }
    ]
  })
}

# Attach S3 access policy to the IAM role
resource "aws_iam_policy" "flightanalysis_redshift_s3_access_policy" {
  name        = "FlightanalysisRedshiftS3AccessPolicy"
  description = "Policy to allow Redshift to access S3"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect   = "Allow",
        Action   = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:ListBucket"
        ],
        Resource = [
          "arn:aws:s3:::${aws_s3_bucket.flightanalysis.bucket}",        # S3 Bucket ARN
          "arn:aws:s3:::${aws_s3_bucket.flightanalysis.bucket}/*"        # S3 Bucket objects ARN
        ]
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "flightanalysis_redshift_s3_policy_attachment" {
  role       = aws_iam_role.flightanalysis_redshift_role.name
  policy_arn = aws_iam_policy.flightanalysis_redshift_s3_access_policy.arn
}

# Redshift Subnet Group
resource "aws_redshift_subnet_group" "flightanalysis" {
  name       = "flightanalysis-subnet-group"
  subnet_ids = [aws_subnet.flightanalysis.id]

  tags = {
    Name = "flightanalysis-redshift-subnet-group"
  }
}

# Redshift Cluster
resource "aws_redshift_cluster" "flightanalysis_cluster" {
  cluster_identifier          = "flightanalysis-cluster"
  node_type                   = "dc2.large"  # Adjust node type as needed
  master_username             = "admin"
  master_password             = var.redshift_password
  cluster_type                = "single-node"
  iam_roles                   = [aws_iam_role.flightanalysis_redshift_role.arn]
  publicly_accessible         = true         # Public access enabled
  number_of_nodes             = 1
  port                        = 5439
  vpc_security_group_ids      = [aws_security_group.flightanalysis_redshift_sg.id]
  cluster_subnet_group_name   = aws_redshift_subnet_group.flightanalysis.name
  skip_final_snapshot         = true

  tags = {
    Name = "flightanalysis-redshift-cluster"
  }
}

# Output the Redshift endpoint and IAM role
output "redshift_endpoint" {
  value = aws_redshift_cluster.flightanalysis_cluster.endpoint
}

output "redshift_iam_role" {
  value = aws_iam_role.flightanalysis_redshift_role.arn
}


resource "aws_budgets_budget" "monthly-budget" {
  name              = "monthly-budget"
  budget_type       = "COST"
  limit_amount      = "10"
  limit_unit        = "USD"
  time_period_start = "2024-09-19_00:00"
  time_unit         = "MONTHLY"

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 100
    threshold_type             = "PERCENTAGE"
    notification_type          = "FORECASTED"
    subscriber_email_addresses = ["anh.phung@torontomu.ca"]
  }
}
