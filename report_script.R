library(tidyverse)
library(tidyquant)

lap_times <- read_csv("python/data.csv", show_col_types = FALSE)
lap_times$driver[lap_times$driver == "MAX"] <- "VER"
df_vec <- c()

cols <- c("ALO" = "#00594E", "HAM" = "#04EAC1", "PER" = "#3671C6", "VER" = "#3A4162")

# Functions
plot_func <- function(dframe, gp, driver1, driver2, gp_color) {
  svg(file = paste0("plots_and_images/", gp, "_constructors.svg"), width = 6, height = 4)

  plot(dframe %>%
         group_by(constructor) %>%
         ggplot(aes(x = constructor, y = time, fill = constructor)) +
         geom_boxplot(outlier.size = 0.75, outlier.shape = 15, show.legend = FALSE) +
         coord_flip() +
         labs(x = "Constructor", y = "Lap Time (s)"))

  dev.off()

  svg(file = paste0("plots_and_images/", gp, "_h2h.svg"), width = 6, height = 4)

  plot(dframe %>%
         filter(driver %in% c(driver1, driver2)) %>%
         group_by(driver) %>%
         ggplot(aes(x = lap, y = time, color = driver)) +
         geom_point(size = 0.1) +
         geom_ma(ma_fun = SMA, n = 5, linetype = "solid") +
         scale_color_manual(values = cols) +
         labs(x = "Lap", y = "Lap Time (s)"))

  dev.off()

  svg(file = paste0("plots_and_images/", gp, "_fuel.svg"), width = 6, height = 4)

  plot(dframe %>%
         group_by(lap) %>%
         summarise(median = median(time)) %>%
         ggplot(aes(x = lap, y = median)) +
         geom_line(lwd = 0.75) +
         geom_smooth(method = lm, se = FALSE, color = gp_color, formula = y ~ x) +
         labs(x = "Lap", y = "Median Lap Time (s)"))

  dev.off()
}

# Bahrain Grand Prix
bahrain <- lap_times %>% filter(grand_prix == "Bahrain")
df_vec[1] <- quantile(bahrain$time, 0.75) - quantile(bahrain$time, 0.25)
df_vec[2] <- quantile(bahrain$time, 0.75) + 1.5 * df_vec[1]
bahrain <- filter(bahrain, time <= df_vec[2])

plot_func(bahrain, "Bahrain", "ALO", "HAM", "maroon")

# Saudi Arabian Grand Prix
saudi <- lap_times %>% filter(grand_prix == "Saudi Arabia")
df_vec[1] <- quantile(saudi$time, 0.75) - quantile(saudi$time, 0.25)
df_vec[2] <- quantile(saudi$time, 0.75) + 1.5 * df_vec[1]
saudi <- filter(saudi, time <= df_vec[2])

plot_func(saudi, "Saudi Arabia", "PER", "VER", "forestgreen")

# Australian Grand Prix
australia <- lap_times %>% filter(grand_prix == "Australia")
df_vec[1] <- quantile(australia$time, 0.75) - quantile(australia$time, 0.25)
df_vec[2] <- quantile(australia$time, 0.75) + 1.5 * df_vec[1]
australia <- filter(australia, time <= 90)

plot_func(australia, "Australia", "ALO", "HAM", "navy")

# Azerbaijan Grand Prix
azerbaijan <- lap_times %>% filter(grand_prix == "Azerbaijan")
df_vec[1] <- quantile(azerbaijan$time, 0.75) - quantile(azerbaijan$time, 0.25)
df_vec[2] <- quantile(azerbaijan$time, 0.75) + 1.5 * df_vec[1]
azerbaijan <- filter(azerbaijan, time <= df_vec[2])

plot_func(azerbaijan, "Azerbaijan", "PER", "VER", "red4")

# Miami Grand Prix
miami <- lap_times %>% filter(grand_prix == "Miami")
df_vec[1] <- quantile(miami$time, 0.75) - quantile(miami$time, 0.25)
df_vec[2] <- quantile(miami$time, 0.75) + 1.5 * df_vec[1]
miami <- filter(miami, time <= df_vec[2])

plot_func(miami, "Miami", "PER", "VER", "cyan2")

# Monaco Grand Prix
monaco <- lap_times %>% filter(grand_prix == "Monaco")
df_vec[1] <- quantile(monaco$time, 0.75) - quantile(monaco$time, 0.25)
df_vec[2] <- quantile(monaco$time, 0.75) + 1.5 * df_vec[1]
monaco <- filter(monaco, time <= 80)

plot_func(monaco, "Monaco", "ALO", "VER", "red1")