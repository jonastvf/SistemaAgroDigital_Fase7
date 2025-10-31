options(repos = c(CRAN = "https://cran.r-project.org/"))
install.packages("dplyr")
library(dplyr)

cat('\014')

caminho_atual <- getwd()
arquivo_csv <- file.path(caminho_atual, "dados.csv")

if (!file.exists(arquivo_csv)) {
  cat("Dados não encontrados\n")
  quit(status = 1)
}

dados <- read.csv(arquivo_csv, sep = ',', header = TRUE, stringsAsFactors = FALSE)

if (nrow(dados) == 0) {
  cat("Dados não encontrados\n")
  quit(status = 1)
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

for (i in 1:nrow(resultado)) {
  cat("\nCultura:", resultado$culture[i], "\n")
  cat("Média da área total:", resultado$`Média da área total`[i], "\n")
  cat("Mediana da área total:", resultado$`Mediana da área total`[i], "\n")
  cat("Desvio padrão área total:", resultado$`Desvio padrão área total`[i], "\n")
  cat("Média da área plantada:", resultado$`Média da área plantada`[i], "\n")
  cat("-------------------------\n")
}
