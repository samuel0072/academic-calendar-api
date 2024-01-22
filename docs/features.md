# Funcionalidades planejadas

## Criar um novo calendário acadêmico
    entrada: data de ínicio, data final
    saída: um identificado da instância de calendário acadêmico que foi criada e persistida    

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
    comportamento: o sistema vai criar, associar ao calendário e persistir a lista. Caso o rótulo dos dias seja "não-letivos" o sistema vai alterar a coontagem de dias letivos e não letivos
    saída: um identificador do evento criado

## Adicionar dia não letivo
    entrada: calendário acadêmico, um campus, uma data, uma descrição, um rótulo
    comportamento: o sistema vai criar, associar ao calendário e aos campus e persistir o dia não letivo com sua descrição e rótulo
    saída: um identificador do registro criado

- adicionar importação de feriados nacionais 
- adicionar importação de feriados regionais - informar qual campus vai ter aqueles feriados
- adicionar importação de eventos através de uma planilha
    - nessa importação o usuário vai ter que informar a data de inicio
    e os espaços entre cada evento. Tipo matriculas incia dia X e o proximo evento inicia 10 dias depois da matricula. O inicio do semestre letivo pode ser um bom dia inicial pro evento
- Adicionar capacidade do usuário informar os campi pro sistema considerar
- Adicionar a possibilidade do usuário pode habilitar e desabilitar um sábado letivo