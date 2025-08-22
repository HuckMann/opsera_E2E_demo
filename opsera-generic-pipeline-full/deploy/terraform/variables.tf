variable "region" { type = string }
variable "project" { type = string }
variable "ecr_repos" {
  type = list(string)
  default = ["inventory","orders","billing","scheduling"]
}
