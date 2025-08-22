resource "aws_ecr_repository" "svc" {
  for_each = toset(var.ecr_repos)
  name     = "${var.project}-${each.key}"
  image_scanning_configuration { scan_on_push = true }
  tags = { Project = var.project }
}
# Add EKS/VPC modules here or wire to your existing infra
