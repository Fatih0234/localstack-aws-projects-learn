{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject"
      ],
      "Resource": [
        "arn:aws:s3:::${images_bucket}",
        "arn:aws:s3:::${images_bucket}/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:GetObject"
      ],
      "Resource": [
        "arn:aws:s3:::${styled_bucket}",
        "arn:aws:s3:::${styled_bucket}/*"
      ]
    }
  ]
}
