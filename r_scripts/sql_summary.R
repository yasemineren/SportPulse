#!/usr/bin/env Rscript

if (!requireNamespace("DBI", quietly = TRUE) ||
    !requireNamespace("RSQLite", quietly = TRUE)) {
  stop("Gerekli paketler eksik: DBI ve RSQLite")
}

library(DBI)
library(RSQLite)

db_path <- "sportpulse.db"
if (!file.exists(db_path)) {
  stop(paste("Veritabanı bulunamadı:", db_path))
}

con <- dbConnect(SQLite(), db_path)
query <- "
  SELECT
    facility_id,
    ROUND(AVG(y), 2) AS avg_demand,
    ROUND(AVG(price), 2) AS avg_price,
    ROUND(AVG(distance_to_event), 2) AS avg_event_distance,
    COUNT(*) AS obs_count
  FROM sport_data
  GROUP BY facility_id
  ORDER BY avg_demand DESC
"
summary_df <- dbGetQuery(con, query)
dbDisconnect(con)

write.csv(summary_df, "sportpulse_sql_summary_r.csv", row.names = FALSE)
message("R SQL özeti oluşturuldu: sportpulse_sql_summary_r.csv")
