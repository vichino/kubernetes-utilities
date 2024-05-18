kubectl delete pod trivy-results-inspect -n default
kubectl delete configmap trivy-images
kubectl delete job trivy-scan -n default
kubectl delete pod trivy -n default
kubectl delete pvc trivy-pvc
kubectl delete pv trivy-pv
