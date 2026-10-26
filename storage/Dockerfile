#Cone và biên dịch MinIO
FROM golang:1.25-alpine AS build
RUN apk add --no-cache git
RUN git clone --depth 1 --branch RELEASE.2025-09-07T16-13-09Z \
    https://github.com/minio/minio.git /src
WORKDIR /src
RUN CGO_ENABLED=0 go build -trimpath -ldflags "-s -w" -o /minio .

# Image chạy, chỉ chứa file binary
FROM alpine:3.20
COPY --from=build /minio /usr/bin/minio
EXPOSE 9000 9001
ENTRYPOINT ["/usr/bin/minio"]
CMD ["server", "/data", "--console-address", ":9001"]