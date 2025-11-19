options(repos = c(CRAN = "https://cran.r-project.org/"))

suppressPackageStartupMessages({
  library(dplyr)
  library(jsonlite)
})


cat('\014')

caminho_atual <- getwd()
arquivo_csv <- file.path(caminho_atual, "dados.csv")

if (!file.exists(arquivo_csv)) {
  cat(toJSON(list(
    has_data = FALSE,
    message = "Dados não encontrados (arquivo CSV não existe)"
  ), auto_unbox = TRUE))
  quit(status = 0)
}

dados <- read.csv(arquivo_csv, sep = ',', header = TRUE, stringsAsFactors = FALSE)

if (nrow(dados) == 0) {
  cat(toJSON(list(
    has_data = FALSE,
    message = "Dados não encontrados (arquivo CSV está vazio)"
  ), auto_unbox = TRUE))
  quit(status = 0)
}

dados$totalArea <- as.numeric(dados$totalArea)
dados$plantingArea <- as.numeric(dados$plantingArea)
dados$productQtd <- as.numeric(dados$productQtd)

resultado <- dados %>%
  group_by(culture) %>%
  summarise(
    `Média da área total` = mean(totalArea, na.rm = TRUE),
    `Mediana da área total` = median(totalArea, na.rm = TRUE),
    `Desvio padrão área total` = sd(totalArea, na.rm = TRUE),
    `Média da área plantada` = mean(plantingArea, na.rm = TRUE)
  )

names(resultado) <- c(
  "culture",
  "media_area_total",
  "mediana_area_total",
  "desvio_padrao_area_total",
  "media_area_plantada"
)

resultado$has_data <- TRUE

cat(toJSON(resultado, auto_unbox = TRUE))

