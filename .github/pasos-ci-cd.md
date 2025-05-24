
# CI CD con githubactions y argocd

## argo

### crear namespace
```
kubectl create namespace argocd
```

### levantar la config de argo
```
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

### hacer port forwarding en argo con el cluster
```
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

### loguearse a argo por consola
```
./argocd.exe login localhost:8080 --username admin --password ZhuH5RFtekwODkNg --insecure
```

### obtener password de argo
```
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

### crear app en argo
```
./argocd.exe app create mypla-frontend --repo https://github.com/Juanbrero/MyPla.git --path deploy/frontend --dest-server https://kubernetes.default.svc --dest-namespace default --sync-policy automated --revision SIP-73-armar-deployment-en-cloud
```

### borrar app en argo
```
./argocd.exe app delete mypla-frontend
```

### entrar a argo en el navegador
https://localhost:8080/