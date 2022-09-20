# Sprint3 (CICD Pipeline creation)
In this Sprint we have implement a pipeline to automate the build and deployment process of app development. This way we can focus more on developing our application.

In Sprint 2 we were building and deploying the application using ```cdk synth and cdk deploy``` after every change but now our pipeline takes care of the whole process.

## Tech Stack
* AWS Lambda
* AWS Cloud Watch
* AWS Code Pipeline

## Sprint 3 include following tasks:

1. To automate the build and development process of the application using CICD pipeline.

2. Create different stages of pipeline i.e. Beta stage, Gamme stage and Prod stage.

3. Create Unit Tests for pre-beta stage and add manual approval check for pre-pod stage.

4. Add roll back to previous function functionaly depending on duration and invocation alarm.

# How it works

We have developed a pipeline whose structure is like 

```
app.py ---> pipeline stack ---> Stages ---> Application stack 
```

Our app will point towrads the pipeline stack unlike our pervious sprints where it was pointing towards applicaion stack. 

We just have to ``` git commit && git push ``` to register our changes to GitHub and the reset will be taken care by our pipeline. It will take the changes from our GitHub repo and will synth and deploy it automatically after running the desired tests.


# How to Run

The benefit of CICD pipeline is that there is very little human interventation required. We, developers, only have to deploy the pipeline once using

``` 
cdk synth && cdk deploy 
```

After that we can focus on the application's core services and the pipeline will take care of the rest.

<!-- # Improvements required
It is planned to add functionality test in pre-gamma stage in near future. -->

Two additional metrices were created to monitor the pipeline i.e. Duration metric and Invocation metric. 
<!-- The system will roll back to previos -->

We can also set the deployment speed of our application to the application servers. We can specify the time limit and the percentage of the application deployed in that time. In this Sprint, we have set the 10 % every minute using ```LINEAR_10PERCENT_EVERY_1MINUTE``` 
