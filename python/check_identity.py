import boto3

sts = boto3.client("sts")

identity = sts.get_caller_identity()

print("AWS Account:", identity["Account"])
print("AWS ARN:", identity["Arn"])
print("AWS User ID:", identity["UserId"])