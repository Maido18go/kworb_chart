# type = string
variable "gcp_project_id" {}
variable "gcs_location" {}
variable "bq_location" {}
variable "bucket" {}
variable "dataset_id" {}

variable "country_codes" {
  type = list(string)
  default = [
#    "id",
#    "kr",
#    "my",
#    "ph",
#    "sg",
    "th",
    "vn"
  ]
}
