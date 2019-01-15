SERVICE=Inputs
OWNER=${AWS_USER}
S3BUCKET=$(OWNER)-${AWS_SALESFEED_S3BUCKET}
ROLE=${AWS-LAMBDA-ROLE}

build:
	sam build -m requirements.txt --use-container

run:
	sam local invoke "$(SERVICE)" -e ./events/basic.json

upload: zip
	aws s3 sync .aws-sam/package s3://$(S3BUCKET)

zip:
	./zip.bash $(SERVICE)

create-function:
	aws lambda create-function --function-name $(OWNER)-$(SERVICE) --role $(ROLE) --handler app.lambda_handler --runtime python3.6 --code S3Bucket=$(S3BUCKET),S3Key=$(SERVICE).zip

deploy: upload
	aws lambda update-function-code --function-name $(OWNER)-$(SERVICE) --s3-bucket $(S3BUCKET) --s3-key $(SERVICE).zip

clean:
	rm -rf .aws-sam
