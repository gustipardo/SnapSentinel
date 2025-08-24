resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = { Name = "aws-snapshot-vpc" }
}

# Subnets Públicas
resource "aws_subnet" "public_az1" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "us-east-1a"
  map_public_ip_on_launch = true
  tags = { Name = "public-az1" }
}

resource "aws_subnet" "public_az2" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.2.0/24"
  availability_zone = "us-east-1b"
  map_public_ip_on_launch = true
  tags = { Name = "public-az2" }
}

# Subnets Privadas
resource "aws_subnet" "private_az1" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.11.0/24"
  availability_zone = "us-east-1a"
  tags = { Name = "private-az1" }
}

resource "aws_subnet" "private_az2" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.12.0/24"
  availability_zone = "us-east-1b"
  tags = { Name = "private-az2" }
}

// local.public_subnets → contiene los IDs de las subnets públicas.
// local.private_subnets → contiene los IDs de las subnets privadas.
locals {
  public_subnets = [
    aws_subnet.public_az1.id,
    aws_subnet.public_az2.id
  ]

  private_subnets = [
    aws_subnet.private_az1.id,
    aws_subnet.private_az2.id
  ]
}


