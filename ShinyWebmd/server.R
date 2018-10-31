shinyServer(function(input, output, session) {

  observe({
    condition = input$selectCondition
    drugsByCondition <- unique(webmd_alldrugs %>%
                                 filter(., condition == input$selectCondition))
    updateSelectizeInput(
      session, "selectDrugByCondition",
      choices = drugsByCondition,
      selected = drugsByCondition[1])
  })
  
  # drug_data <- reactive({
  #   webmd_alldrugs %>%
  #     filter(drug == input$selectDrug & condition == input$selectCondition & age = input$selectAge & sex = input$selectSex) %>%
  #     group_by(easeOfUse, effectiveness, satisfaction) %>%
  #     summarise(count = n())
  # })
  
  output$plot <- renderPlot({})
  
})