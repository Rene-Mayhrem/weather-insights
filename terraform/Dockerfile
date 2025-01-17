FROM hashicorp/hashicorp/terraform:latest

# ? Set working directory
WORKDIR /terraform

COPY . .

# ? Execute terraform -> init IaC
ENTRYPOINT [ "init" ]