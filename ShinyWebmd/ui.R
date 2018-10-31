library(shinydashboard)

shinyUI(dashboardPage(
  dashboardHeader(title = "Most Common Drugs on Webmd",
                  titleWidth = 400),
  dashboardSidebar(
    sidebarMenu(
      selectizeInput("selectDrug",
                     "Select Drug",
                     choices = sort(unique(webmd_alldrugs$drug))),
      selectizeInput("selectCondition",
                     "Select Condition",
                     choices = sort(unique(webmd_alldrugs$condition))),
      selectizeInput("selectAge",
                     "Select Age",
                     choices = sort(unique(webmd_alldrugs$age))),
      selectizeInput("selectSex",
                     "Select Sex",
                     choices = c("Male","Female")))
  ),
  dashboardBody(
    tabItems(
  )
)))