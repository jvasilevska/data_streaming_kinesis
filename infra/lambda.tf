resource "aws_lambda_function" "lambda_processor" {
  filename      = var.lambda_processor_filename
  function_name = var.lambda_processor_function
  role          = aws_iam_role.firehose_lambda_role.arn
  handler       = var.lambda_processor_handler
  source_code_hash = filebase64sha256(var.lambda_processor_filename)
  runtime       = "python3.8"
  depends_on = [
    aws_cloudwatch_log_group.lambda_group,
    aws_iam_role_policy_attachment.lambda_logs
  ]
}


resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.firehose_lambda_role.name
  policy_arn = aws_iam_policy.lambda_logging.arn
}


resource "aws_cloudwatch_log_group" "lambda_group" {
  name              = var.lambda_cloudwatch_log_group
  retention_in_days = 14
}