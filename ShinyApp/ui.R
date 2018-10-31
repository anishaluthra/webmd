library(shinydashboard)

shinyUI(dashboardPage(
  dashboardHeader(title = "Most Common Drugs on Webmd",
                  titleWidth = 400),
  dashboardSidebar(
    sidebarMenu(
      menuItem("By Drug", tabName = "byDrug", icon = icon("map")),
      menuItem("By Condition", tabName = "byCondition", icon = icon("database")))
  ),
  dashboardBody(
    tabItems(
      tabItem(tabName = "byDrug",
              selectizeInput("selectDrug",
                             "Select Drug",
                             choices = sort(unique(webmd_alldrugs$drug))),
              plotlyOutput("ratingsChart"),
              plotlyOutput("treatmentTime")),
      tabItem(tabName = "byCondition",
              selectizeInput("selectCondition",
                             "Select Condition",
                             choices = sort(unique(webmd_alldrugs$condition))),
              selectizeInput("selectDrugByCondition",
                             "Select Drug",
                             choices = "selectDrugByCondition"),
              plotlyOutput("ratingsCondition")))
  )
))