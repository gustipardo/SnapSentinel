// EKS Cluster y Node Group
module "network" {
  source = "../network"
}

resource "aws_eks_cluster" "this" {
  name     = "snapshot-cluster"
  role_arn = aws_iam_role.eks_cluster_role.arn
  version  = "1.29"

  vpc_config {
    subnet_ids = module.network.public_subnets
  }

  depends_on = [
    aws_iam_role_policy_attachment.eks_cluster_AmazonEKSClusterPolicy,
  ]
}

resource "aws_eks_node_group" "this" {
  cluster_name    = aws_eks_cluster.this.name
  node_group_name = "snapshot-nodes"
  node_role_arn   = aws_iam_role.eks_node_role.arn
  subnet_ids      = module.network.public_subnets

  instance_types = ["t3.micro"]
  scaling_config {
    desired_size = 1
    min_size     = 1
    max_size     = 2
  }

  depends_on = [
    aws_iam_role_policy_attachment.AmazonEKSWorkerNodePolicy,
    aws_iam_role_policy_attachment.AmazonEC2ContainerRegistryReadOnly,
    aws_iam_role_policy_attachment.AmazonEKS_CNI_Policy,
  ]
}
