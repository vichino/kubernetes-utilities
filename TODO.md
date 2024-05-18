- connect to cluster
- pv
- pvc
- kubectl get pods --all-namespaces -o jsonpath='{range .items[*]}{.spec.containers[*].image}{"\n"}{end}' | sort | uniq > images.txt
- kubectl create configmap trivy-images --from-file=images.txt
- k apply -f trivy-job.yaml
- k apply -f trivy-pod.yaml
- kubectl exec -it pod/trivy-results-inspect -n default -- sh
  cd /mnt/trivy
