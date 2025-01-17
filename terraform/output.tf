output "s3_bucket_url" {
  value = aws_s3_bucket.weather_data_bucket.bucket_regional_domain_name
}

output "glue_database_name" {
  value = aws_glue_catalog_database.weather_database.name
}

output "glue_crawler_name" {
  value = aws_glue_crawler.weather_crawler.name
}