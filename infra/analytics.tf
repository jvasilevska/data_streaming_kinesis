resource "aws_athena_database" "events_database" {
  name   = var.events_database_name
  bucket = aws_s3_bucket.events_database.bucket
}

resource "aws_glue_catalog_table" "events_table" {
  name          = var.events_table_name
  database_name = aws_athena_database.events_database.name

  table_type = "EXTERNAL_TABLE"

  parameters = {
    EXTERNAL = "TRUE"
  }

  storage_descriptor {
    location      = "s3://${aws_s3_bucket.firehose_bucket.bucket}/"
    input_format  = var.events_table_input_format
    output_format = var.events_table_output_format

    ser_de_info {
      name                  = var.events_table_serde_name
      serialization_library = var.events_table_serde_serialization

      parameters = {
        "field.delim" = ","
      }
    }

    columns {
      name = "id"
      type = "string"
    }

    columns {
      name = "aggregate_id"
      type = "string"
    }

    columns {
      name = "type"
      type = "string"
    }

    columns {
      name = "timestamp"
      type = "string"
    }

    columns {
      name = "customer_name"
      type = "string"
    }

    columns {
      name = "customer_dob"
      type = "string"
    }

    columns {
      name = "product_name"
      type = "string"
    }
  }
}