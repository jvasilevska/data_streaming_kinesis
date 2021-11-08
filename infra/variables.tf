variable "access_key" {
  description = "AWS access key"
  type        = string
  sensitive   = true
}

variable "secret_key" {
  description = "AWS secret key"
  type        = string
  sensitive   = true
}

variable "region" {
  description = "AWS region"
  type        = string
  sensitive   = true
}

variable "kinesis_stream" {
  default = "kinesis-data-stream"
  type    = string
}

variable "kinesis_firehose" {
  default = "firehose-data-delivery"
  type    = string
}

variable "firehose_bucket" {
  default = "firehose-data-sink"
  type    = string
}

variable "firehose_role" {
  default = "firehose-iam-role"
  type    = string
}

variable "firehose_policy" {
  default = "firehose-iam-policy"
  type    = string
}

variable "firehose_s3_access_policy" {
  default = "firehose-s3-access-iam-policy"
  type    = string
}

variable "firehose_lambda_role" {
  default = "firehose-lambda-iam-role"
  type    = string
}

variable "firehose_lambda_policy" { 
  type        = string
  default = "firehose-lambda-iam-policy"
} 

variable "lambda_logging" {
  default = "lambda-logging"
  type    = string
}

variable "lambda_processor_filename" {
  default = "../dist/lambda.zip"
  type    = string
}

variable "lambda_processor_function" {
  default = "firehose-lambda-processor"
  type    = string
}

variable "lambda_processor_handler" {
  default = "firehose_data_transformation.lambda_handler"
  type    = string
}

variable "lambda_cloudwatch_log_group" {
  default = "/aws/lambda/firehose_data_transformation.lambda_handler"
  type    = string
}

variable "glue_role_name" {
  default = "glue-iam-role"
  type    = string
}

variable "glue_policy_name" {
  default = "glue-iam-policy"
  type    = string
}

variable "events_database_name" {
  default = "events_db"
  type    = string
}

variable "athena_results_bucket" {
  default = "events-athena-results"
  type    = string
}

variable "events_table_name" {
  default = "events"
  type    = string
}

variable "events_table_input_format" {
  default = "org.apache.hadoop.mapred.TextInputFormat"
  type    = string
}

variable "events_table_output_format" {
  default = "org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat"
  type    = string
}

variable "events_table_serde_name" {
  default = "serde_events_table"
  type    = string
}

variable "events_table_serde_serialization" {
  default = "org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe"
  type    = string
}