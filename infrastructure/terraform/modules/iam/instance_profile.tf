resource "aws_iam_instance_profile" "ec2" {
  name = "${var.project_name}-${var.environment}-instance-profile"

  role = aws_iam_role.ec2.name
}