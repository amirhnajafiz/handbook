# Jobs and CronJobs

## Quick Description (QD)

A Job creates one or more Pods and will continue to retry execution of the Pods until a specified number of them successfully terminate. As Pods successfully complete, the Job tracks the successful completions.

When a specified number of successful completions is reached, the task (i.e., the Job) is complete. Deleting a Job will clean up the Pods it created. Suspending a Job (`spec.suspend: true`) will delete its active Pods until the Job is resumed again.

Finished Jobs are usually no longer needed in the system. Keeping them around will put pressure on the API server. If the Jobs are managed directly by a higher-level controller, such as a CronJob, the Jobs can be cleaned up by the CronJob based on the specified history limits (`successfulJobsHistoryLimit` and `failedJobsHistoryLimit`). For a standalone Job you can use `ttlSecondsAfterFinished`.

A CronJob is meant for performing regular scheduled actions such as backups, report generation, and so on. One CronJob object is like one line of a crontab (cron table) file on a Unix system. It runs a Job periodically on a given schedule, written in Cron format.

## Installation

_Nothing here yet._

## Useful Tips/Commands (UToC)

_Nothing here yet._

## Examples (e.g.,)

A Job that computes pi to 2000 places. `backoffLimit` is the number of retries before the Job is marked as failed:

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: pi
spec:
  template:
    spec:
      containers:
      - name: pi
        image: perl:5.34.0
        command: ["perl",  "-Mbignum=bpi", "-wle", "print bpi(2000)"]
      restartPolicy: Never
  backoffLimit: 4
```

A CronJob that runs every minute:

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: hello
spec:
  schedule: "* * * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: hello
            image: busybox:1.28
            imagePullPolicy: IfNotPresent
            command:
            - /bin/sh
            - -c
            - date; echo Hello from the Kubernetes cluster
          restartPolicy: OnFailure
```

## References

- [K8S Jobs](https://kubernetes.io/docs/concepts/workloads/controllers/job/)
- [K8S CronJobs](https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/)
- [Indexed parallel processing](https://kubernetes.io/docs/tasks/job/indexed-parallel-processing-static/)
- [TTL after finished](https://kubernetes.io/docs/concepts/workloads/controllers/ttlafterfinished/)
