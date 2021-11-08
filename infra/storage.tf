resource "aws_s3_bucket" "firehose_bucket" {
  bucket = var.firehose_bucket
  acl    = "private"
}

resource "aws_s3_bucket" "events_database" {
  bucket = var.athena_results_bucket
}
