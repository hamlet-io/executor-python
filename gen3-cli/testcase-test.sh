# NOTE: all JSON scalar values must be in json format. Ex. true vs True
cot-testcases test \
  --no-lint \
  --file tests/data/system/testcases/valid-syntax-cf.yml \
  --match Parameters.ApplicationName.Type String \
  --match Parameters.Environment.AllowedValues.0 Dev \
  --match Resources.untaggedInstance '{"Type":"AWS::EC2::Instance","Properties":{"ImageId":"ami-123456"}}' \
  --length Parameters.Environment.AllowedValues 2 \
  --exists Parameters.Environment.AllowedValues.0 \
  --not-empty Resources \
  --resource untaggedInstance AWS::EC2::Instance
