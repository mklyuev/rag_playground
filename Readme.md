## Get Started

Service is using <a href="https://voyageai.com">Voyage AI</a> for embedding and <a href="https://www.trychroma.com">Chroma Db</a> for storing vectors 

>Please, create .env in the root folder of the project and set up VOYAGE_API_KEY

To run, start a docker compose:

```shell
docker-compose up -d
```

## Endpoints

The docker container exposes the following endpoints:

- Upload file for indexing
  ```shell
  curl --request POST \
  --url http://localhost:8000/upload \
  --header 'Content-Type: multipart/form-data' \
  --form file=/project/code/service.app
  ```
- Search related files by query
  ```shell
  curl --request GET --url 'http://localhost:8000/search?query=show all tests&limit=3'
  ```


Files are available on the same host with file path returned from the search endpoint