provider "aws" {
    region = "eu-west-2"
    access_key = var.ACCESS_KEY
    secret_key = var.SECRET_ACCESS_KEY
}

data "aws_vpc" "c11-VPC" {
    id = "vpc-04b15cce2398e57f7"
}

data "aws_iam_role" "ecs_task_execution_role" {
  name = "ecsTaskExecutionRole"
}

## Data Movement


resource "aws_ecs_task_definition" "long-term-extract-task-def" {
    family = "c11-kelpie-long-term-extract-task-def"
    requires_compatibilities = ["FARGATE"]
    network_mode = "awsvpc"
    cpu = 1024
    memory = 3072
    execution_role_arn = data.aws_iam_role.ecs_task_execution_role.arn
    container_definitions = jsonencode(([
        {
            name = "c11-kelpie-long-term-extract-image"
            image = "129033205317.dkr.ecr.eu-west-2.amazonaws.com/c11-kelpie-long-term-extract-load-image:latest"
            cpu = 1024
            memory = 3072
            essential = true
            environment = [
                {
                    "name" : "ACCESS_KEY",
                    "value" : var.ACCESS_KEY
                },
                {
                    "name" : "SECRET_ACCESS_KEY",
                    "value" : var.SECRET_ACCESS_KEY
                },
                {
                    "name" : "BUCKET",
                    "value" : var.BUCKET
                },
                {
                    "name" : "FILE_NAME",
                    "value" : var.FILE_NAME
                },
                {
                    "name" : "DB_HOST",
                    "value" : var.DB_HOST
                },
                {
                    "name" : "DB_PORT",
                    "value" : var.DB_PORT
                },
                {
                    "name" : "DB_PASSWORD",
                    "value" : var.DB_PASSWORD
                },
                {
                    "name" : "DB_USER",
                    "value" : var.DB_USER
                },
                {
                    "name" : "DB_NAME",
                    "value" : var.DB_NAME
                },
                {
                    "name" : "DB_SCHEMA",
                    "value" : var.DB_SCHEMA
                }
            ]
        }
    ]))
    runtime_platform {
      operating_system_family = "LINUX"
      cpu_architecture = "X86_64"
    }

}

resource "aws_iam_role" "long_term_extract_schedule_role" {
    name = "c11-kelpie-long-term-extract-schedule-role"

    assume_role_policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
            {
                Effect = "Allow"
                Principal = {
                Service = "scheduler.amazonaws.com"
                }
                Action = "sts:AssumeRole"
            }
        ]
    })
}

resource "aws_iam_policy" "schedule-policy-execution-for-long-term-extract" {
    name = "c11-kelpie-terraform-long-term-extract-execution-policy"
    policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
            {
                Effect = "Allow"
                Action = "ecs:RunTask"
                Resource = aws_ecs_task_definition.long-term-extract-task-def.arn
                Condition = {
                    ArnLike = {
                        "ecs:cluster" = var.CLUSTER_ARN
                    }
                }
            },
            {
                Effect = "Allow"
                Action = "iam:PassRole"
                Resource = "*"
                Condition = {
                    StringLike = {
                        "iam:PassedToService" = "ecs-tasks.amazonaws.com"
                    }
                }
            }
        ]
    })
}

resource "aws_iam_role_policy_attachment" "policy_attach_thing" {
    role = aws_iam_role.long_term_extract_schedule_role.name
    policy_arn = aws_iam_policy.schedule-policy-execution-for-long-term-extract.arn
}

resource "aws_scheduler_schedule" "long-term-extract-schedule" {
    name = "c11-kelpie-long-term-extract-schedule"
    flexible_time_window {
      mode = "OFF"
    }
    schedule_expression = "cron(0 8 * * ? *)"
    target {
        arn = var.CLUSTER_ARN
        role_arn = aws_iam_role.long_term_extract_schedule_role.arn
        ecs_parameters {
            task_definition_arn = aws_ecs_task_definition.long-term-extract-task-def.arn
            launch_type = "FARGATE"
        
            network_configuration {
                subnets = ["subnet-07de213eeae1f6307","subnet-0e6c6a8f959dae31a","subnet-08781450402b81aa2"]
                assign_public_ip = true
            }
        }
    }
}

# Dashboard

resource "aws_ecs_task_definition" "dashboard_task_def" {
    family = "c11-kelpie-dashboard-task-def"
    requires_compatibilities = ["FARGATE"]
    network_mode = "awsvpc"
    cpu = 1024
    memory = 3072
    execution_role_arn = data.aws_iam_role.ecs_task_execution_role.arn
    container_definitions = jsonencode(([
        {
            name = "c11-kelpie-dashboard-ecr"
            image = "129033205317.dkr.ecr.eu-west-2.amazonaws.com/c11-kelpie-plant-dashboard:latest"
            cpu = 1024
            memory = 3072
            essential = true
            portMappings = [
                {
                    hostPort = 80
                    containerPort = 80
                },
                {
                    hostPort = 8501
                    containerPort = 8501
                }
            ]
            environment = [
                {
                    "name": "DB_HOST",
                    "value": var.DB_HOST
                },
                {
                    "name": "DB_NAME",
                    "value": var.DB_NAME
                },
                {
                    "name": "DB_PASSWORD",
                    "value": var.DB_PASSWORD
                },
                {
                    "name": "DB_PORT",
                    "value": var.DB_PORT
                },
                {
                    "name": "DB_SCHEMA",
                    "value": var.DB_SCHEMA
                },
                {
                    "name": "DB_USER",
                    "value": var.DB_USER
                },
                {
                    "name": "ACCESS_KEY",
                    "value": var.ACCESS_KEY
                },
                {
                    "name": "SECRET_ACCESS_KEY",
                    "value": var.SECRET_ACCESS_KEY
                }
            ]
        }
    ]))
    runtime_platform {
      operating_system_family = "LINUX"
      cpu_architecture = "X86_64"
    }

}


resource "aws_security_group" "dashboard_allow_all_sg" {
    name="c11-kelpie-dashboard-allow-all-sg"
    description="Security group to allow all HTTP inbound and outbound traffice"
    vpc_id = data.aws_vpc.c11-VPC.id

    tags = {
        Name="allow all"
    }

    egress {
        from_port = 0
        to_port = 0
        protocol = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }

    ingress {
        from_port = 0
        to_port = 0
        protocol = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }
}

resource "aws_ecs_service" "dashboard_service" {
    name = "c11-kelpie-dashboard-service-terraform"
    cluster = var.CLUSTER_ARN
    task_definition = aws_ecs_task_definition.dashboard_task_def.arn
    desired_count = 1
    launch_type = "FARGATE"
    network_configuration {
      subnets = ["subnet-07de213eeae1f6307","subnet-0e6c6a8f959dae31a","subnet-08781450402b81aa2"]
      security_groups = [aws_security_group.dashboard_allow_all_sg.id]
      assign_public_ip = true
    }
}


# Pipeline Lambda

variable "pipeline_lambda_name" {
    default =  "c11-kelpie-pipeline-lambda-tf"
}

data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "iam_for_lambda" {
  name               = "c11-berkay-lambda-role"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

resource "aws_cloudwatch_log_group" "lambda_pipeline_cloudwatch" {
  name              = "/aws/lambda/${var.pipeline_lambda_name}"
  retention_in_days = 0
}

data "aws_iam_policy_document" "lambda_logging" {
  statement {
    effect = "Allow"

    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
    ]

    resources = ["arn:aws:logs:*:*:*"]
  }
}

resource "aws_iam_policy" "lambda_logging" {
  name        = "c11-berkay-lambda_logging"
  path        = "/"
  description = "IAM policy for logging from a lambda"
  policy      = data.aws_iam_policy_document.lambda_logging.json
}

resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.iam_for_lambda.name
  policy_arn = aws_iam_policy.lambda_logging.arn
}

resource "aws_lambda_function" "test_lambda" {
    function_name = var.pipeline_lambda_name
    role = aws_iam_role.iam_for_lambda.arn
    image_uri = "129033205317.dkr.ecr.eu-west-2.amazonaws.com/c11-kelpie-pipeline:latest"
    environment {
        variables = {
            DB_HOST = "${var.DB_HOST}",
            DB_NAME = "${var.DB_NAME}",
            DB_PASSWORD = "${var.DB_PASSWORD}",
            DB_PORT = "${var.DB_PORT}",
            DB_SCHEMA = "${var.DB_SCHEMA}",
            DB_USER = "${var.DB_USER}",
            API_URL = "${var.API_URL}",
            NUM_PLANTS = "${var.NUM_PLANTS}"
        }
    }
    package_type = "Image"
    depends_on = [
    aws_iam_role_policy_attachment.lambda_logs,
    aws_cloudwatch_log_group.lambda_pipeline_cloudwatch,
    ]
    memory_size = 10240
    timeout = 60
}




resource "aws_iam_role" "pipeline_schedule_role" {
    name = "c11-kelpie-pipeline-schedule-role"

    assume_role_policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
            {
                Effect = "Allow"
                Principal = {
                Service = "scheduler.amazonaws.com"
                }
                Action = "sts:AssumeRole"
            }
        ]
    })
}


resource "aws_iam_policy" "schedule_policy_execution_etl_lambda" {
    name = "c11-kelpie-terraform-etl-lambda-execution-policy"
    policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
            {
                Effect = "Allow"
                Action = "lambda:InvokeFunction"
                Resource = aws_lambda_function.test_lambda.arn
            }
        ]
    })
}

resource "aws_iam_role_policy_attachment" "policy_attachment_etl_lambda" {
    role = aws_iam_role.pipeline_schedule_role.name
    policy_arn = aws_iam_policy.schedule_policy_execution_etl_lambda.arn
}

resource "aws_scheduler_schedule" "etl_lambda_schedule" {
    name = "c11-kelpie-etl-lambda-schedule-tf"
    flexible_time_window {
      mode = "OFF"
    }
    schedule_expression = "cron(* * * * ? *)"
    target {
        arn=aws_lambda_function.test_lambda.arn
        role_arn = aws_iam_role.pipeline_schedule_role.arn
    }
}

# Anomaly Detection

variable "anomaly_detection_lambda_name" {
    default =  "c11-kelpie-anomaly-detection-lambda-tf"
}

resource "aws_iam_role" "iam_for_anomaly_detection_lambda" {
  name               = "c11-kelpie-anomaly-detection-lambda-role"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

resource "aws_cloudwatch_log_group" "lambda_anomaly_detection_cloudwatch" {
  name              = "/aws/lambda/${var.anomaly_detection_lambda_name}"
  retention_in_days = 0
}

resource "aws_iam_role_policy_attachment" "anomaly_detection_lambda_logs" {
  role       = aws_iam_role.iam_for_anomaly_detection_lambda.name
  policy_arn = aws_iam_policy.lambda_logging.arn
}

resource "aws_lambda_function" "anomaly_detection_lambda" {
    function_name = var.anomaly_detection_lambda_name
    role = aws_iam_role.iam_for_anomaly_detection_lambda.arn
    image_uri = "129033205317.dkr.ecr.eu-west-2.amazonaws.com/c11-kelpie-anomaly-detection-ecr:latest"
    environment {
        variables = {
            ACCESS_KEY = "${var.ACCESS_KEY}",
            SECRET_ACCESS_KEY = "${var.SECRET_ACCESS_KEY}",
            DB_HOST = "${var.DB_HOST}",
            DB_NAME = "${var.DB_NAME}",
            DB_PASSWORD = "${var.DB_PASSWORD}",
            DB_PORT = "${var.DB_PORT}",
            DB_SCHEMA = "${var.DB_SCHEMA}",
            DB_USER = "${var.DB_USER}",
            API_URL = "${var.API_URL}",
            NUM_PLANTS = "${var.NUM_PLANTS}",
            ANOMALY_THRESHOLD = "${var.ANOMALY_THRESHOLD}",
            COUNT_TO_BE_ANOMALY = "${var.COUNT_TO_BE_ANOMALY}",
            TIME_FRAME = "${var.TIME_FRAME}",
            SNS_ARN = "${aws_sns_topic.botanist_notification.arn}"
        }
    }
    package_type = "Image"
    depends_on = [
    aws_iam_role_policy_attachment.anomaly_detection_lambda_logs,
    aws_cloudwatch_log_group.lambda_anomaly_detection_cloudwatch,
    ]
    memory_size = 128
    timeout = 15
}




resource "aws_iam_role" "anomaly_detection_schedule_role" {
    name = "c11-kelpie-anomaly-detection-schedule-role"

    assume_role_policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
            {
                Effect = "Allow"
                Principal = {
                Service = "scheduler.amazonaws.com"
                }
                Action = "sts:AssumeRole"
            }
        ]
    })
}


resource "aws_iam_policy" "schedule_policy_execution_anomaly_detection_lambda" {
    name = "c11-kelpie-terraform-anomaly-detection-lambda-execution-policy"
    policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
            {
                Effect = "Allow"
                Action = "lambda:InvokeFunction"
                Resource = aws_lambda_function.anomaly_detection_lambda.arn
            }
        ]
    })
}

resource "aws_iam_role_policy_attachment" "policy_attachment_anomaly_detection_lambda" {
    role = aws_iam_role.anomaly_detection_schedule_role.name
    policy_arn = aws_iam_policy.schedule_policy_execution_anomaly_detection_lambda.arn
}

resource "aws_scheduler_schedule" "anomaly_detection_lambda_schedule" {
    name = "c11-kelpie-anomaly-detection-lambda-schedule-tf"
    flexible_time_window {
      mode = "OFF"
    }
    schedule_expression = "cron(* * * * ? *)"
    target {
        arn=aws_lambda_function.anomaly_detection_lambda.arn
        role_arn = aws_iam_role.anomaly_detection_schedule_role.arn
    }
}

# SNS

resource "aws_sns_topic" "botanist_notification" {
    name = "c11-kelpie-botanist-notification-topic"
  
}

resource "aws_sns_topic_subscription" "sns-topic-email-sign-up-berkay" {
    endpoint = "trainee.berkay.dur@sigmalabs.co.uk"
    protocol = "email"
    topic_arn = aws_sns_topic.botanist_notification.arn
    endpoint_auto_confirms = true
}

resource "aws_sns_topic_subscription" "sns-topic-email-sign-up-umar" {
    endpoint = "trainee.umar.haider@sigmalabs.co.uk"
    protocol = "email"
    topic_arn = aws_sns_topic.botanist_notification.arn
    endpoint_auto_confirms = true
}