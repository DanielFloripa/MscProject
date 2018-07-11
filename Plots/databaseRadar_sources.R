# sources table for databaseRadar.R
#Sys.setenv("plotly_username"="Daniel13")
#Sys.setenv("plotly_api_key"="tEEharsCr0RaDBhGsmqB")
#streamming<-"1mvsw4web5"

#devtools::install_github("ropensci/plotly")
#library(plotly)

#options(browser = 'false')
#api_create(p, filename = "r-docs-midwest-boxplots")

metric2<-"t.gvt as gvt, t.energy_0, t.energy_f, max(t.energy_0-t.energy_f) as reduc_val, (t.energy_0-t.energy_f)/t.energy_0 as reduc_p, t.val_0 as fals_pos, t.val_f as migrations, l.val_0 as load, t.info as info"


AZ_ERR_CONS<-data.frame(
AZ1<-matrix(c(18, 1e-04, "SELECT t.gvt as gvt, t.energy_0, t.energy_f, max(t.energy_0-t.energy_f) as reduc_val, (t.energy_0-t.energy_f)/t.energy_0 as reduc_p, t.val_0 as fals_pos, t.val_f as migrations, l.val_0 as load, t.info as info FROM consol_d as t inner join az_load_l as l on l.gvt=t.gvt and (l.val_0 <= 0.25330513 and l.val_0 >= 0.25310513)",
  16, 0.0417, "SELECT t.gvt as gvt, t.energy_0, t.energy_f, max(t.energy_0-t.energy_f) as reduc_val, (t.energy_0-t.energy_f)/t.energy_0 as reduc_p, t.val_0 as fals_pos, t.val_f as migrations, l.val_0 as load, t.info as info FROM consol_d as t inner join az_load_l as l on l.gvt=t.gvt and (l.val_0 <= 0.29490513 and l.val_0 >= 0.21150513)",
 14, 1e-04, "SELECT t.gvt as gvt, t.energy_0, t.energy_f, max(t.energy_0-t.energy_f) as reduc_val, (t.energy_0-t.energy_f)/t.energy_0 as reduc_p, t.val_0 as fals_pos, t.val_f as migrations, l.val_0 as load, t.info as info FROM consol_d as t inner join az_load_l as l on l.gvt=t.gvt and (l.val_0 <= 0.25330513 and l.val_0 >= 0.25310513)",
  17, 0.0097, "SELECT t.gvt as gvt, t.energy_0, t.energy_f, max(t.energy_0-t.energy_f) as reduc_val, (t.energy_0-t.energy_f)/t.energy_0 as reduc_p, t.val_0 as fals_pos, t.val_f as migrations, l.val_0 as load, t.info as info FROM consol_d as t inner join az_load_l as l on l.gvt=t.gvt and (l.val_0 <= 0.26290513 and l.val_0 >= 0.24350513)",
  82, 1e-04, "SELECT t.gvt as gvt, t.energy_0, t.energy_f, max(t.energy_0-t.energy_f) as reduc_val, (t.energy_0-t.energy_f)/t.energy_0 as reduc_p, t.val_0 as fals_pos, t.val_f as migrations, l.val_0 as load, t.info as info FROM consol_d as t inner join az_load_l as l on l.gvt=t.gvt and (l.val_0 <= 0.25330513 and l.val_0 >= 0.25310513)",
  11, 1e-04, "SELECT t.gvt as gvt, t.energy_0, t.energy_f, max(t.energy_0-t.energy_f) as reduc_val, (t.energy_0-t.energy_f)/t.energy_0 as reduc_p, t.val_0 as fals_pos, t.val_f as migrations, l.val_0 as load, t.info as info FROM consol_d as t inner join az_load_l as l on l.gvt=t.gvt and (l.val_0 <= 0.25330513 and l.val_0 >= 0.25310513)",
 7, 0.0065, "SELECT t.gvt as gvt, t.energy_0, t.energy_f, max(t.energy_0-t.energy_f) as reduc_val, (t.energy_0-t.energy_f)/t.energy_0 as reduc_p, t.val_0 as fals_pos, t.val_f as migrations, l.val_0 as load, t.info as info FROM consol_d as t inner join az_load_l as l on l.gvt=t.gvt and (l.val_0 <= 0.25970513 and l.val_0 >= 0.24670513)"), ncol=3, byrow = TRUE),
AZ5<-matrix(c(
  13, 0.0021, "SELECT t.gvt as gvt, t.energy_0, t.energy_f, max(t.energy_0-t.energy_f) as reduc_val, (t.energy_0-t.energy_f)/t.energy_0 as reduc_p, t.val_0 as fals_pos, t.val_f as migrations, l.val_0 as load, t.info as info FROM consol_d as t inner join az_load_l as l on l.gvt=t.gvt and (l.val_0 <= 0.71681774 and l.val_0 >= 0.71261774)",
  14, 0.0242, "SELECT t.gvt as gvt, t.energy_0, t.energy_f, max(t.energy_0-t.energy_f) as reduc_val, (t.energy_0-t.energy_f)/t.energy_0 as reduc_p, t.val_0 as fals_pos, t.val_f as migrations, l.val_0 as load, t.info as info FROM consol_d as t inner join az_load_l as l on l.gvt=t.gvt and (l.val_0 <= 0.73891774 and l.val_0 >= 0.69051774)",
  18, 0.0021, "SELECT t.gvt as gvt, t.energy_0, t.energy_f, max(t.energy_0-t.energy_f) as reduc_val, (t.energy_0-t.energy_f)/t.energy_0 as reduc_p, t.val_0 as fals_pos, t.val_f as migrations, l.val_0 as load, t.info as info FROM consol_d as t inner join az_load_l as l on l.gvt=t.gvt and (l.val_0 <= 0.71681774 and l.val_0 >= 0.71261774)",
  48, 0.0192, "SELECT t.gvt as gvt, t.energy_0, t.energy_f, max(t.energy_0-t.energy_f) as reduc_val, (t.energy_0-t.energy_f)/t.energy_0 as reduc_p, t.val_0 as fals_pos, t.val_f as migrations, l.val_0 as load, t.info as info FROM consol_d as t inner join az_load_l as l on l.gvt=t.gvt and (l.val_0 <= 0.73391774 and l.val_0 >= 0.69551774)",
  15, 1e-04, "SELECT t.gvt as gvt, t.energy_0, t.energy_f, max(t.energy_0-t.energy_f) as reduc_val, (t.energy_0-t.energy_f)/t.energy_0 as reduc_p, t.val_0 as fals_pos, t.val_f as migrations, l.val_0 as load, t.info as info FROM consol_d as t inner join az_load_l as l on l.gvt=t.gvt and (l.val_0 <= 0.71481774 and l.val_0 >= 0.71461774)",
  3, 0.0041, "SELECT t.gvt as gvt, t.energy_0, t.energy_f, max(t.energy_0-t.energy_f) as reduc_val, (t.energy_0-t.energy_f)/t.energy_0 as reduc_p, t.val_0 as fals_pos, t.val_f as migrations, l.val_0 as load, t.info as info FROM consol_d as t inner join az_load_l as l on l.gvt=t.gvt and (l.val_0 <= 0.71881774 and l.val_0 >= 0.71061774)",
 8, 0.0051, "SELECT t.gvt as gvt, t.energy_0, t.energy_f, max(t.energy_0-t.energy_f) as reduc_val, (t.energy_0-t.energy_f)/t.energy_0 as reduc_p, t.val_0 as fals_pos, t.val_f as migrations, l.val_0 as load, t.info as info FROM consol_d as t inner join az_load_l as l on l.gvt=t.gvt and (l.val_0 <= 0.71981774 and l.val_0 >= 0.70961774)"), ncol=3, byrow = TRUE),
AZ6<-matrix(c(
  184, 1e-04, "SELECT t.gvt as gvt, t.energy_0, t.energy_f, max(t.energy_0-t.energy_f) as reduc_val, (t.energy_0-t.energy_f)/t.energy_0 as reduc_p, t.val_0 as fals_pos, t.val_f as migrations, l.val_0 as load, t.info as info FROM consol_d as t inner join az_load_l as l on l.gvt=t.gvt and (l.val_0 <= 0.64658438 and l.val_0 >= 0.64638438)",
  1, 1e-04, "SELECT t.gvt as gvt, t.energy_0, t.energy_f, max(t.energy_0-t.energy_f) as reduc_val, (t.energy_0-t.energy_f)/t.energy_0 as reduc_p, t.val_0 as fals_pos, t.val_f as migrations, l.val_0 as load, t.info as info FROM consol_d as t inner join az_load_l as l on l.gvt=t.gvt and (l.val_0 <= 0.64658438 and l.val_0 >= 0.64638438)",
  336, 1e-04, "SELECT t.gvt as gvt, t.energy_0, t.energy_f, max(t.energy_0-t.energy_f) as reduc_val, (t.energy_0-t.energy_f)/t.energy_0 as reduc_p, t.val_0 as fals_pos, t.val_f as migrations, l.val_0 as load, t.info as info FROM consol_d as t inner join az_load_l as l on l.gvt=t.gvt and (l.val_0 <= 0.64658438 and l.val_0 >= 0.64638438)",
  7, 1e-04, "SELECT t.gvt as gvt, t.energy_0, t.energy_f, max(t.energy_0-t.energy_f) as reduc_val, (t.energy_0-t.energy_f)/t.energy_0 as reduc_p, t.val_0 as fals_pos, t.val_f as migrations, l.val_0 as load, t.info as info FROM consol_d as t inner join az_load_l as l on l.gvt=t.gvt and (l.val_0 <= 0.64658438 and l.val_0 >= 0.64638438)",
  336, 1e-04, "SELECT t.gvt as gvt, t.energy_0, t.energy_f, max(t.energy_0-t.energy_f) as reduc_val, (t.energy_0-t.energy_f)/t.energy_0 as reduc_p, t.val_0 as fals_pos, t.val_f as migrations, l.val_0 as load, t.info as info FROM consol_d as t inner join az_load_l as l on l.gvt=t.gvt and (l.val_0 <= 0.64658438 and l.val_0 >= 0.64638438)",
  3, 1e-04, "SELECT t.gvt as gvt, t.energy_0, t.energy_f, max(t.energy_0-t.energy_f) as reduc_val, (t.energy_0-t.energy_f)/t.energy_0 as reduc_p, t.val_0 as fals_pos, t.val_f as migrations, l.val_0 as load, t.info as info FROM consol_d as t inner join az_load_l as l on l.gvt=t.gvt and (l.val_0 <= 0.64658438 and l.val_0 >= 0.64638438)",
 2, 0.003, "SELECT t.gvt as gvt, t.energy_0, t.energy_f, max(t.energy_0-t.energy_f) as reduc_val, (t.energy_0-t.energy_f)/t.energy_0 as reduc_p, t.val_0 as fals_pos, t.val_f as migrations, l.val_0 as load, t.info as info FROM consol_d as t inner join az_load_l as l on l.gvt=t.gvt and (l.val_0 <= 0.64948438 and l.val_0 >= 0.64348438)"), ncol=3, byrow = TRUE)
)
colnames(AZ_ERR_CONS)=(c("AZ1.qtd", "AZ1.err", "AZ1.query", "AZ5.qtd", "AZ5.err", "AZ5.query", "AZ6.qtd", "AZ6.err", "AZ6.query"))
rownames(AZ_ERR_CONS)=this_tests_names
as.character(AZ_ERR_CONS["Unlock_HA","AZ1.err"])

