options(repos = c(CRAN = "https://cran.r-project.org/"))

install.packages("httr")
install.packages("jsonlite")

library(httr)
library(jsonlite)


view_logo <- function() {
logo <- "___________                        _________      .__          __  .__                      
\\_   _____/____ _______  _____    /   _____/ ____ |  |  __ ___/  |_|__| ____   ____   ______
 |    __) \\__  \\\\_  __ \\/     \\   \\_____  \\ /  _ \\|  | |  |  \\   __\\  |/  _ \\ /    \\ /  ___/
 |     \\   / __ \\|  | \\/  Y Y  \\  /        (  <_> )  |_|  |  /|  | |  (  <_> )   |  \\\\___ \\ 
 \\___  /  (____  /__|  |__|_|  / /_______  /\\____/|____/____/ |__| |__|\\____/|___|  /____  >
     \\/        \\/            \\/          \\/                                       \\/     \\/

                             Ｐａｉｎｅｌ Ｍｅｔｅｏｒｏｌｏｇｉｃａ
"    
cat(logo, sep = "\n")
}


caption <- function(){
    message <- paste("\nSeja bem-vindo ao Painel Meteorológico! Aqui você pode consultar informações climáticas de qualquer cidade do mundo.\n",
                      "Pressione Enter para começar...\n")
    cat(message)
    invisible(readLines("stdin", n = 1))
}


userInitMessage <- function(){
    print("\nDigite o nome da cidade para obter as informações meteorológicas (ou 'sair' para encerrar): ")
}


styleMessage <- function(city){
    personalized_message <- paste("\nBuscando informações da cidade:", city, "...\n")
    print(personalized_message)
}


inputPause <- function(){
    sttats <- readline()
}


clear_console <- function(){
    # if (Sys.info()[['sysname']] == "Windows") {
    #     system("cls")
    # } else {
    #     system("clear")
    # }
}


api_key <- "645fed2436d7059e18c338cde46a6346"


repeat {
    clear_console()
    view_logo()
    caption()
    
    repeat {
        userInitMessage()
        city <- trimws(readLines("stdin", n = 1))
        
        if (tolower(city) == "sair") {
            cat("\nEncerrando o programa... Até logo!\n")
            quit()
        }

        styleMessage(city)
        formate_url_city <- URLencode(city) 

        url <- paste0("https://api.openweathermap.org/data/2.5/weather?q=", formate_url_city, "&appid=", api_key, "&units=metric")

        verified_city <- try(fromJSON(url), silent = TRUE)

        if (inherits(verified_city, "try-error") || is.null(verified_city$main)) {
            print(paste("Cidade não encontrada:", city, ". Por favor, tente novamente."))
        } else {
            break  
        }
    }

    
    df_climate <- data.frame(
        Cidade = verified_city$name,
        Temperatura = verified_city$main$temp,
        Umidade = verified_city$main$humidity,
        Pressao = verified_city$main$pressure,
        Vento = verified_city$wind$speed,
        Latitude = verified_city$coord$lat,
        Longitude = verified_city$coord$lon
    )

    
    print(df_climate)

    
    cat("\nDeseja consultar outra cidade? (s/n): ")
    resposta <- readLines("stdin", n = 1)
    
    if (tolower(resposta) != "s") {
        cat("\nEncerrando o programa... Até logo!\n")
        quit()
    }
}
