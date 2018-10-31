shinyServer(function(input, output, session) {
  
  observe({
    condition = input$selectCondition
    drugsByConditionAll <- webmd_alldrugs %>%
                     filter(., condition == input$selectCondition)
    drugsByCondition <- sort(unique(drugsByConditionAll$drug))
    updateSelectizeInput(
      session, "selectDrugByCondition",
      choices = drugsByCondition,
      selected = drugsByCondition[1])
  })
  
  output$ratingsChart <- renderPlotly({
    drug = input$selectDrug
    drug_easeOfUse = drugs_easeOfUse[drugs_easeOfUse$drug == drug,]
    drug_effectiveness = drugs_effectiveness[drugs_effectiveness$drug == drug,]
    drug_satisfaction = drugs_satisfaction[drugs_satisfaction$drug == drug,]
    data <- data.frame(Rating = drug_easeOfUse$easeOfUse, Ease = drug_easeOfUse$count,
                       Effectiveness = drug_effectiveness$count,
                       Satisfaction = drug_satisfaction$count)
    plot_ly(data, x = ~Rating, y = ~Ease, type = 'bar', name = 'Ease of Use') %>%
      add_trace(y = ~Effectiveness, name = 'Effectiveness') %>%
      add_trace(y = ~Satisfaction, name = 'Satisfaction') %>%
      layout(yaxis = list(title = 'Count'), barmode = 'group')
  })
  
  output$treatmentTime <- renderPlotly({
    drug = input$selectDrug
    drug_timeUsed = webmd_alldrugs[webmd_alldrugs$drug == drug,] %>%
      group_by(., timeUsed) %>%
      summarise(., count = n())
    drug_timeUsed = drug_timeUsed[2:8,1:2]
    drug_timeUsed$timeUsed <- factor(drug_timeUsed$timeUsed,
                                     levels = c("less than 1 month", "1 to 6 months",
                                                "6 months to less than 1 year", "1 to less than 2 years",
                                                "2 to less than 5 years", "5 to less than 10 years",
                                                "10 years or more"))
    plot_ly(drug_timeUsed, x = ~timeUsed, y = ~count, name = 'Treatment Time', type =)
  })
  
  output$ratingsCondition <- renderPlotly({
    drug = input$selectDrugByCondition
    drug_ratings = webmd_alldrugs[webmd_alldrugs$drug == drug,] %>%
      filter(., condition == input$selectCondition)
    drugCondition_ease = drug_ratings %>% group_by(., easeOfUse) %>% summarise(., count = n())
    drugCondition_effectiveness = drug_ratings %>% group_by(., effectiveness) %>% summarise(., count = n())
    drugCondition_satisfaction = drug_ratings %>% group_by(., satisfaction) %>% summarise(., count = n())
    
    dataCondition <- data.frame(Rating = drugCondition_ease$easeOfUse, Ease = drugCondition_ease$count,
                       Effectiveness = drugCondition_effectiveness$count,
                       Satisfaction = drugCondition_satisfaction$count)
    plot_ly(dataCondition, x = ~Rating, y = ~Ease, type = 'bar', name = 'Ease of Use') %>%
      add_trace(y = ~Effectiveness, name = 'Effectiveness') %>%
      add_trace(y = ~Satisfaction, name = 'Satisfaction') %>%
      layout(yaxis = list(title = 'Count'), barmode = 'group')
  })
  
  
})