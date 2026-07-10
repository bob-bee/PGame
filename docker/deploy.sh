To configure multi-stage Docker builds for your full stack and automate deployment to a local K3s cluster, follow these steps:

### Step 1: Update the Dockerfile

Ensure that each service in your application has a corresponding Dockerfile configured for multi-stage builds. Below is an example of how you might structure one of these Dockerfiles:

```Dockerfile
# Stage 1: Build
FROM golang:1.17 as builder

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o main .

# Stage 2: Prepare the container
FROM alpine:latest

WORKDIR /root/

COPY --from=builder /app/main .

CMD ["./main"]
```

### Step 2: Configure Health Check Endpoints in the Dockerfile

If your application does not already include health check endpoints, you can add them. For example, if your application is a web server and you are using Go with Echo:

```go
package main

import (
    "github.com/labstack/echo/v4"
    "net/http"
)

func main() {
    e := echo.New()

    e.GET("/health", func(c echo.Context) error {
        return c.String(http.StatusOK, "I'm alive!")
    })

    e.Logger.Fatal(e.Start(":8080"))
}
```

### Step 3: Create K3s Manifest Files

For each service in your application, create a Kubernetes manifest file. Here’s an example for a web server:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-service-deployment
spec:
  replicas: 2
  selector:
    matchLabels:
      app: my-service
  template:
    metadata:
      labels:
        app: my-service
    spec:
      containers:
      - name: my-service-container
        image: your-dockerhub-username/my-service-image:tag
        ports:
        - containerPort: 8080
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10

---
apiVersion: v1
kind: Service
metadata:
  name: my-service-service
spec:
  selector:
    app: my-service
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
  type: LoadBalancer
```

### Step 4: Automate Deployment with a CI/CD Pipeline

To automate the deployment process, you can use tools like GitHub Actions, GitLab CI, or Jenkins. Below is an example using GitHub Actions:

```yaml
name: Deploy to K3s

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v2

    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v1

    - name: Login to Docker Hub
      run: echo "${{ secrets.DOCKER_PASSWORD }}" | docker login --username ${DOCKER_USERNAME} --password-stdin

    - name: Build and push image
      run: |
        DOCKER_BUILDKIT=1 docker build . --file Dockerfile --tag your-dockerhub-username/my-service-image:tag
        docker push your-dockerhub-username/my-service-image:tag

    - name: Apply K3s manifest
      run: kubectl apply -f path/to/your-manifest.yaml
```

### Step 5: Run a Local K3s Cluster

To run a local K3s cluster, you can use Docker Compose or simply run the K3s binary with a few command-line flags:

```sh
# Using Docker Compose (requires docker-compose.yml)
docker-compose up -d

# Or using K3s binary
curl -sfL https://get.k3s.io | sh -
```

### Summary

1. **Update the Dockerfile**: Use multi-stage builds and add health check endpoints.
2. **Create K3s Manifest Files**: Define Deployments and Services for each service.
3. **Automate Deployment**: Set up a CI/CD pipeline to build, push images, and apply Kubernetes manifests.
4. **Run a Local K3s Cluster**: Use Docker Compose or the K3s binary to run your cluster locally.

By following these steps, you will have a fully automated deployment pipeline for your full stack application running on a local K3s cluster.