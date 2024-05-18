- connect to cluster
- pv
- pvc
#- kubectl get pods --all-namespaces -o jsonpath='{range .items[*]}{.spec.containers[*].image}{"\n"}{end}' | sort | uniq > images.txt
# with *
- kubectl create configmap trivy-images --from-file=images.txt
- kubectl create configmap trivy-images --from-file=images.txt
- k apply -f trivy-job.yaml
#- k apply -f trivy-pod.yaml
- k apply -f pod-inspect-results.yaml
- kubectl exec -it pod/trivy-results-inspect -n default -- sh
  cd /mnt/trivy
- k cp default/trivy-results-inspect:/mnt/trivy /tmp
