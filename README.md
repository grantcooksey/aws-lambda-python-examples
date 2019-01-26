# AWS Lambda Python Examples

This repo serves as a starting point for building reliable aws lambda functions in python. These examples are focused 
on not only teaching the basics, but providing examples of common use cases, and discussing the developer workflow that
I have learned to use.

This repo focuses on:
* development
* unit testing
* monitoring
* deployment


Each example will have the basic structure:

```bash
.
├── events			<-- Sample events
├── src                         <-- Source code for a lambda function
│   └── service
│   	 ├── __init__.py
│   	 └── app.py             <-- Lambda function code
├── tests                       <-- Unit tests
│	     ├── __init__.py
│	     └── test_handler.py
├── requirements.txt            <-- Python dependencies
├── template.yaml               <-- SAM template
├── setup.py                    <-- setup script 
└── tox.ini               	    <-- tox configuration
```

[More information on why this is the structure I use for Python projects.](https://blog.ionelmc.ro/2014/05/25/python-packaging/)

## Requirements

* AWS CLI already configured with Administrator permission
* [SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html) >=0.7 installed
* [Python 3 installed](https://www.python.org/downloads/)
* [Docker installed](https://www.docker.com/community-edition)
* [Virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/) or roll your own with [Python Virtual Environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/)

### Python 3.6

You can either use homebrew or use [pyenv](https://github.com/pyenv/pyenv).

For homebrew

1. `brew unlink python`
2. `brew install https://raw.githubusercontent.com/Homebrew/homebrew-core/f2a764ef944b1080be64bd88dca9a1d80130c558/Formula/python.rb` We are installing the latest 3.6 formula here, the current on homebrew is 3.7.
3. `brew switch python 3.6.5_1`

## Setup process

### Env setup

Using virtualenvwapper

1. `mkvirtualenv sf -p python3` (sf for salesfeed)
2. `workon sf`

To exit the env run `deactivate`.

### Installing local dependencies

When in your virtual environment:

```bash
> pip install -r requirements.txt tox
```


### Pycharm setup

Add the interpreter in Preferences->Project->Project Interpreter:

1. Hit the setup icon->add and select existing env
2. Hit the "..." and select the python executable in the env you created (probably ~/.env/sf/bin/python) and add the interpreter

You will need to mark the src directory as a sources folder. (right click)

##  Development

[AWS Lambda requires a flat folder](https://docs.aws.amazon.com/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html) with the application as well as its dependencies. SAM will use `CodeUri` property to know where to look up for both application and dependencies:

```yaml
...
    HelloWorldFunction:
        Type: AWS::Serverless::Function
        Properties:
            CodeUri: hello_world/
            ...
```

Create this file and build the proper dependencies.

```bash
> make build
```

> **See [Serverless Application Model (SAM) HOWTO Guide](https://github.com/awslabs/serverless-application-model/blob/master/HOWTO.md) for more details in how to get started.**

The `build` command in the `Makefile` uses `sam build` to build the app. The following happens:

* Moves the python module defined in `template.yaml` into a `.aws-sam/build` directory, ie the event-selector-service
* Spins up an aws compatible docker container with a volume mapped to the `build` folder
* Installs dependencies into the fresh container using [PyPI](https://pypi.org/). Native dependencies get built here.

We can locally run the lambda in a docker container to test. Build the application first.

```bash
> make run
```

## Testing

We use **Pytest** and **pytest-mock** for testing our code and automate testing with different python versions using [Tox](https://tox.readthedocs.io/en/latest/).

```bash
> tox
```

If you add a new dependency, add the `--recreate` flag.

## Packaging and Deployment

Firstly, we need a `S3 bucket` where we can upload our Lambda functions packaged as ZIP before we deploy anything - If you don't have a S3 bucket to store code artifacts then this is a good time to create one:

```bash
> aws s3 mb s3://BUCKET_NAME
```

The lambda is packaged by pulling all source code into a new directory under `.aws-sam/build` and zipped up.
The zip file is then uploaded an the S3 bucket.

We must first create the lambda function with the zip file and set up all the configuration. Once the lambda exists, we can deploy a new
version by using the `aws lambda update-function-code` command.  This will not change the configuration but replaces the
function code with a new zip file.

Take a look at the [AWS lambda docs](https://docs.aws.amazon.com/cli/latest/reference/lambda/index.html) for more info. 
Now would be a good time to take a look at the Makefile to see the individual commands run. The two env vars `AWS_USER`
and `AWS_SALESFEED_S3BUCKET` deal with how the resources will be named in AWS.

Move into the function directory. We can now package the function and all its dependencies into a zip file:

```bash
> make zip
```

The path of the zip file created is `.aws-sam/package/FUNCTION_NAME.zip`. If you want to look at the source code that
gets included in the zip file, take a look inside `.aws-sam/build`.
 
Now upload the zip file to S3:

```bash
> aws s3 cp .aws-sam/package/FUNCTION_NAME.zip s3://BUCKET_NAME
```

Lets create the aws lambda function. You'll need the arn of a valid [IAM role](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html)
for your new function. Take a look at the
[`create-function`](https://docs.aws.amazon.com/cli/latest/reference/lambda/create-function.html) documentation if you
want to configure the function further, such as adding environment variables or placing the lambda inside a vpc. 
Alternatively to doing this in your cli, you can create the function inside the aws lambda console.

```bash
aws lambda create-function --function-name FUNCTION_NAME --role IAM_ROLE_ARN --handler service.app.lambda_handler --runtime python3.6 --code S3Bucket=S3_BUCKET_NAME,S3Key=FUNCTION_NAME.zip
```

The function has been created. You can [invoke](https://docs.aws.amazon.com/cli/latest/reference/lambda/invoke.html)
it from your cli:

```bash
aws lambda invoke --function-name FUNCTION_NAME --payload '{"key1":"value1", "key2":"value2"}' outfile.txt
```

If you make further changes to your source code, you can upload an updated zip from S3 using [update-function-code](https://docs.aws.amazon.com/cli/latest/reference/lambda/update-function-code.html)
so you don't need to delete and recreate your function. Use:

```bash
> aws lambda update-function-code --s3-bucket S3_BUCKET_NAME --s3-key FUNCTION_NAME.zip
```
