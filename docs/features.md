# Funcionalidades planejadas

## Criar um novo calendário acadêmico
    entrada: data de ínicio, data final
    saída: uma nova instância de calendário acadêmico vai ser criada e persistida    

## Contagem de dias letivos
    entrada: calendário acadêmico
    saída: a quantidade de dias letivos nesse calendário

## Listar de dias letivos
    entrada: calendário acadêmico
    saída: uma lista de todos os dias letivos nesse calendário(exclui-se domingo, feriados, recesso acadêmico, sabados não letivos e qualquer outro dia não letivo)

## Listar de dias não letivos
    entrada: calendário acadêmico
    saída: uma lista contendo os sabados não letivos, domingos, feriados, recesso acadêmico e qualquer outro dia não letivo

## Criar um evento
    entrada: calendário acadêmico, uma lista de dias, uma descrição do evento, rótulo dos dias
    saída: o sistema vai criar, associar ao calendário e persistir a lista. Caso o rótulo dos dias seja "não-letivos" o sistema vai alterar a coontagem de dias letivos e não letivos

## Adicionar dia não letivo
    entrada: calendário acadêmico, um campus, uma data, uma descrição, um rótulo
    saída: o sistema vai criar, associar ao calendário e aos campus e persistir o dia não letivo com sua descrição e rótulo

