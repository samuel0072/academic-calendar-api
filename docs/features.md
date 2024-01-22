# Funcionalidades planejadas do back-end

## Criar um novo calendário acadêmico
    entrada: data de ínicio, data final
    comportamento: cria um calendário e salva com o org_id igual do usuário logado
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
    comportamento: o sistema vai criar, associar ao calendário e persistir a lista. Caso o rótulo dos dias seja "não-letivos" o sistema vai alterar a contagem de dias letivos e não letivos
    saída: um identificador do evento criado

## Adicionar dia não letivo
    entrada: calendário acadêmico, um campus, uma data, uma descrição, um rótulo
    comportamento: o sistema vai criar, associar ao calendário e aos campus e persistir o dia não letivo com sua descrição e rótulo
    saída: um identificador do registro criado

## Importação de Feriados Nacionais 
    entrada: planilha com os feríados nacionais
    comportamento: Adiciona os feríados na organização do usuário
    saída: resposta padrão de sucesso, se houver erro, detalhamento dos erros encontrados

## importação de feriados regionais 
    entrada: planilha com os feríados nacionais, lista de campi que vão aderir a esses feríados
    comportamento: Adiciona os feríados na organização do usuário. Adiciona uma relação entre os feríados e os campi
    saída: resposta padrão de sucesso, se houver erro, detalhamento dos erros encontrados

## importação de eventos através de uma planilha
    entrada: calendário acadêmico, uma planilha com os eventos cadastrados
    comportamento: nessa importação o usuário vai ter que informar a data de inicio e os espaços(em contagem de dias) entre cada evento. Tipo matriculas inicia dia X e o proximo evento inicia 10 dias depois da matricula. O inicio do semestre letivo pode ser um bom dia inicial pro evento
    saída: resposta padrão de sucesso. Caso haja erro, informar quais foram os erros

##  possibilidade do usuário pode habilitar e desabilitar um sábado letivo
    entrada: sábado especifico, calendário acadêmico
    comportamento: criar uma rota para habilitar e uma rota para desablitar o sabádo
    saída: resposta padrão de sucesso. Caso haja erro, informar quais foram os erros

##  Exportação do calendário acadêmico em um arquivo PDF
    - deve seguir os padrões da UFAL

# Funcionalidades planejadas do front-end
    
## Criar um novo calendário acadêmico
    Como usuário
    Gostaria de criar um novo calendário acadêmico
    Para planejar o ano escolar da minha instituição acadêmica

    entrada: data de ínicio, data final
    comportamento: envia a requisição para o back-end
    saída: abre uma visualização de calendário pro usuário em caso de sucesso. Caso haja erro, exibir os erros ao usuário

## Contagem de dias letivos
    Como usuário 
    Gostaria de visualizar quantos dias letivos tem no meu calendário
    Para verificar se o calendário obdece a legislação

## Listar de dias letivos
    entrada: calendário acadêmico
    saída: uma lista de todos os dias letivos nesse calendário(exclui-se domingo, feriados, recesso acadêmico, sabados não letivos e qualquer outro dia não letivo)

## Listar de dias não letivos
    entrada: calendário acadêmico
    saída: uma lista contendo os sabados não letivos, domingos, feriados, recesso acadêmico e qualquer outro dia não letivo

## Criar um evento
    entrada: calendário acadêmico, uma lista de dias, uma descrição do evento, rótulo dos dias
    comportamento: o sistema vai criar, associar ao calendário e persistir a lista. Caso o rótulo dos dias seja "não-letivos" o sistema vai alterar a contagem de dias letivos e não letivos
    saída: um identificador do evento criado

## Adicionar dia não letivo
    entrada: calendário acadêmico, um campus, uma data, uma descrição, um rótulo
    comportamento: o sistema vai criar, associar ao calendário e aos campus e persistir o dia não letivo com sua descrição e rótulo
    saída: um identificador do registro criado

## Importação de Feriados Nacionais 
    entrada: planilha com os feríados nacionais
    comportamento: Adiciona os feríados na organização do usuário
    saída: resposta padrão de sucesso, se houver erro, detalhamento dos erros encontrados

## importação de feriados regionais 
    entrada: planilha com os feríados nacionais, lista de campi que vão aderir a esses feríados
    comportamento: Adiciona os feríados na organização do usuário. Adiciona uma relação entre os feríados e os campi
    saída: resposta padrão de sucesso, se houver erro, detalhamento dos erros encontrados

## importação de eventos através de uma planilha
    entrada: calendário acadêmico, uma planilha com os eventos cadastrados
    comportamento: nessa importação o usuário vai ter que informar a data de inicio e os espaços(em contagem de dias) entre cada evento. Tipo matriculas inicia dia X e o proximo evento inicia 10 dias depois da matricula. O inicio do semestre letivo pode ser um bom dia inicial pro evento
    saída: resposta padrão de sucesso. Caso haja erro, informar quais foram os erros

##  possibilidade do usuário pode habilitar e desabilitar um sábado letivo
    entrada: sábado especifico, calendário acadêmico
    comportamento: criar uma rota para habilitar e uma rota para desablitar o sabádo
    saída: resposta padrão de sucesso. Caso haja erro, informar quais foram os erros