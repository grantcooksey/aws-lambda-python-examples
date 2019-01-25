SERVICE=ListObjectsS3

build:
	sam build -m requirements.txt --use-container

run:
	sam local invoke "$(SERVICE)" -e ./events/basic.json

zip:
	./zip.bash $(SERVICE)

clean:
	rm -rf .aws-sam
