# AWS instructions

## Services used

1.  Elastic Container Registry
    - Used to upload and store images of different containers
2. Elastic Container Service
    - Running the containers as separate instances. Using Fargate clusters to run all container tasks in a single service
3. Elastic File System
    - Running storage for shared volumes (MySQL, ES, config, and processing data) storage.
4. EC2 Load balancer
    - Used to route traffic from PortML domain to correct instances on ECS
5. CloudWatch
    - Logging for ECS containers

## Compiling AWS images


## Uploading new images
Once per session connect docker to AWS ECR:
```
aws ecr get-login-password --region [AWS_REGION] | docker login --username AWS --password-stdin [AWS_ACCOUNT_ID].dkr.ecr.[AWS_REGION].amazonaws.com
```
Fill in the AWS region (twice) and the AWS account ID

Next tag your images to push:
```
docker tag [DOCKER_IMAGE_NAME] [AWS_ACCOUNT_ID].dkr.ecr.[AWS_REGION].amazonaws.com/[AWS_ECR_REPOSITORY_NAME]
```
When successful push the image to AWS ECR:
```
docker push [AWS_ACCOUNT_ID].dkr.ecr.[AWS_REGION].amazonaws.com/[AWS_ECR_REPOSITORY_NAME]
```

## Setting the task definitions on AWS ECS
Copy ``.reactenv`` file in ``[FLASK directory]`` and rename to ``.reactenv_aws`` and set all the settings according to the AWS settings to be used

Instead of the default ``docker compose`` up command use the following chained commands to make use of the defined AWS compose file: ``docker-compose-aws.yml`` 
```
docker-compose rm -f ; docker-compose pull ; docker-compose -f docker-compose.yml -f docker-compose-aws.yml up --build
```

## Running config commands

```
aws ecs execute-command --region [AWS_REGION] --cluster fargate-cluster --task [TASKID] --container website --command "php index.php cron init_local_env" --interactive
```


## Additional info
Extra information regarding AWS previously posted into Slack

### To update loadbalancers on service:
```
aws ecs update-service --service portml-dev-service --cluster fargate-cluster --cli-input-json file://D:\Work\PortML\load-v3.json
```
jsonContent:
```
{
	"loadBalancers" :
	[
		{
			"targetGroupArn": "arn:aws:elasticloadbalancing:eu-west-1:482280224187:targetgroup/portml-dev-website-new-tg/1771310010e11e59",
			"containerName": "website_new",
			"containerPort": 5000
		},
		{
			"targetGroupArn": "arn:aws:elasticloadbalancing:eu-west-1:482280224187:targetgroup/portml-dev-elasticsearch-tg/1ff8abd71c2954a6",
			"containerName": "elasticsearch",
			"containerPort": 9200
		},
		{
			"targetGroupArn": "arn:aws:elasticloadbalancing:eu-west-1:482280224187:targetgroup/portml-dev-website-tg/6171a39595c1fd72",
			"containerName": "website",
			"containerPort": 80
		}
	]
}
```

### Run PhP my admin for AWS (if port is open)
```
docker run --name myadmin -d -e PMA_HOST=[IP of task] -p 8000:80 phpmyadmin
```