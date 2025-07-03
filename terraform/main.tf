# Google Cloud Storage
resource "google_storage_bucket" "chart_csv_bucket" {
  name         = "asiapop_charts"
  location     = "asia-northeast1"
}

resource "google_storage_bucket_object" "countries_folder" {
  for_each     = toset(var.country_codes)
  bucket       = google_storage_bucket.chart_csv_bucket.name
  name         = "${each.value}/"
  content      = ""
}

# BigQuery
resource "google_bigquery_dataset" "asiapop_dataset" {
  dataset_id   = var.dataset_id
  location     = var.location
}

resource "google_bigquery_table" "dailytop50_tables" {
  for_each     = toset(var.country_codes)
  dataset_id   = google_bigquery_dataset.asiapop_dataset.dataset_id
  table_id     = "${each.value}_dailytop50"

  schema = <<EOF
[
  {
    "name": "date_field_0",
    "type": "DATE",
    "mode": "NULLABLE"
  },
  {
    "name": "int64_field_1",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "string_field_2",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "string_field_3",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "int64_field_4",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "int64_field_5",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "string_field_6",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "int64_field_7",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "int64_field_8",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "int64_field_9",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "int64_field_10",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "int64_field_11",
    "type": "INTEGER",
    "mode": "NULLABLE"
  }
]
EOF
}

