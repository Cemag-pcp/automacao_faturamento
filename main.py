from selenium import webdriver

from utils import *
from verificar_chrome import *
from ligacao_plan import *

# AttributeError: 'str' object has no attribute 'capabilities'

def automacao_faturamento(nav,data_pedido,chave,valor_total,transportador,volume):

    """
    
    """

    # venda > pedido > baixa de pedido de saída
    # 89196617
    # 3° etapa: Navegar pelo menu
    carregamento(nav)
    menu_cadastro(nav)

    nav.switch_to.default_content() # sair do iframe
    iframes(nav) # entrar no iframe

    # Localizar e preencher o campo "Chave de criação"
    processo_input = WebDriverWait(nav, 1).until(EC.element_to_be_clickable((
        By.XPATH, '//*[@id="variaveis"]//input[@name="chavesDeCriacao"]')))
    processo_input.send_keys(Keys.CONTROL + 'A')
    time.sleep(1.5)
    processo_input.send_keys(chave)
    time.sleep(1.5)
    processo_input.send_keys(Keys.TAB)
    print("Preenchido campo Chave de criação")
    
    carregamento(nav)
    
    erro = verificar_se_erro(nav)
    if erro:
        fechar_todas_abas(nav)
        return erro,2


    # Clicar em "Pesquisar pendência"
    nav.switch_to.default_content() # sair do iframe
    grupo_botao_pesq_pendencia = WebDriverWait(nav, 10).until(EC.element_to_be_clickable((
        By.XPATH, '//*[@id="buttonsCell"]//td[@class="buttonsContainer"]//span[@class="wf-button default"]')))
    grupo_botao_pesq_pendencia.click()
    print("Clicado botão Pesquisa de pendência")

    
    carregamento(nav)

    erro = verificar_se_erro(nav)
    if erro:
        fechar_todas_abas(nav)
        return erro,2

    # Clicar em selecionar todos
    iframes(nav) # entrar no iframe
    grupo_botao_resultado_busca_pendencia = WebDriverWait(nav, 10).until(EC.element_to_be_clickable((
        By.XPATH, '//*[@id="pedidosDaBuscaDePendencia"]')))
    grupo_botao_selecionar_todos = WebDriverWait(nav, 10).until(EC.element_to_be_clickable((
        By.XPATH, '//*[@id="pedidosDaBuscaDePendencia"]//*[@id="invertSelectionButton"]')))
    
    grupo_botao_resultado_busca_pendencia.click() # ativa os campos
    time.sleep(1.5)
    grupo_botao_selecionar_todos.click()
    print("Clicado selecionar todos")

    erro = verificar_se_erro(nav)
    if erro:
        fechar_todas_abas(nav)
        return erro,2

    # Verificar a quantidade de produtos do pedido
    grupo_botao_qtd_produtos = WebDriverWait(nav, 3).until(EC.element_to_be_clickable((
        By.XPATH, '//*[@id="pedidosDaBuscaDePendencia"]//*[@id="pedidosDaBuscaDePendencia_gridPosition_rec_count"]')))
    quantidade_produtos = int(grupo_botao_qtd_produtos.text.strip())
    print(type(quantidade_produtos))
    

    

    # Clicar em "Incluir pendências na baixa"
    nav.switch_to.default_content() # sair do iframe
    grupo_botao_pesq_pendencia = WebDriverWait(nav, 10).until(EC.element_to_be_clickable((
        By.XPATH, '//*[@id="buttonsCell"]//td[@class="buttonsContainer"]//span[@class="wf-button default"]')))
    grupo_botao_pesq_pendencia.click()
    print("Clicado Incluir pendências na baixa")

    carregamento(nav)

    # Validações antes de preencher os campos
    iframes(nav) # entrar no iframe

    # Verificar o campo aprovação
    # campo_aprovacao= WebDriverWait(nav, 3).until(EC.element_to_be_clickable((
    #     By.XPATH, '//*[@id="pedidoOuProvisao"]//input[@name="APROVACAO"]')))
    # data_aprovacao = campo_aprovacao.get_attribute("value")
    # print("Coletado campo Aprovação")
    # print(data_aprovacao," e ",data_pedido)

    # if data_aprovacao != data_pedido:
    #     fechar_todas_abas(nav)
    #     return "Data do pedido não confere",3

    # Verificar a localização da pessoa (confirmar como será feito)
    campo_pessoa = WebDriverWait(nav, 3).until(EC.element_to_be_clickable((
        By.XPATH, '//*[@id="pedidoOuProvisao"]//textarea[@name="PESSOA"]'))) 

    #Double click
    ActionChains(nav).double_click(campo_pessoa).perform()
    carregamento(nav)


    iframes(nav) # entrar no iframe
    # Pegando o valor da UF
    campo_uf = WebDriverWait(nav, 5).until(EC.element_to_be_clickable((
        By.XPATH, '//*[@id="0"]//*[@fieldname="UF"]')))
    
    uf = campo_uf.get_attribute("value")
    print("Coletado valor campo uf")
    # Pegando o campo Cidade
    campo_cidade = WebDriverWait(nav, 5).until(EC.element_to_be_clickable((
        By.XPATH, '//*[@id="0"]//*[@fieldname="LOCALIDADE"]')))
    cidade = campo_cidade.get_attribute("value")
    print("Coletado valor campo cidade")

    zona_franca = False
    venda_interestadual = False
    # Verificar se é imposto interno ou interestadual
    if uf != "CE":
        venda_interestadual = True
        print("Venda interestadual")
        if uf in ["AM","AC","RR"]:
            zona_franca = True
            print("Zona Franca: ",uf)
            fechar_todas_abas(nav)
            return "Pedido em Zona Franca",3
        elif uf == "RO" and cidade == "Guajara-mirim":
            zona_franca = True
            print("Zona Franca: ",uf)
            fechar_todas_abas(nav)
            return "Pedido em Zona Franca",3
    
    

    fechar_aba_atual(nav)

    time.sleep(1.5)
    iframes(nav)
    
    #Verificando o valor do Total Baixa - Se não for ZONA FRANCA
    campo_valor_total = WebDriverWait(nav, 10).until(EC.element_to_be_clickable((
        By.XPATH, '//*[@id="pedidoOuProvisao"]//input[@name="XTOTAL"]')))
    valor_total_pedido = round(float(campo_valor_total.get_attribute("value").strip()),2)
    print("Coletado campo total da baixa")

    print(valor_total_pedido)
    print('-----')
    print(valor_total)

    #Faz a conferência do valor total do pedido
    if not zona_franca:
        if valor_total_pedido != valor_total:
            fechar_todas_abas(nav)
            return "Valor total do pedido não confere",3
    print("Confere o valor total sem ZF")
    
    time.sleep(1.5)
    # Preencher os campos
    
    # Preencher Transportador
    campo_transportador = WebDriverWait(nav, 10).until(EC.element_to_be_clickable((
        By.XPATH, '//*[@id="pedidoOuProvisao"]//input[@name="TRANSPORTA"]')))
    campo_transportador.click()
    campo_transportador.send_keys(transportador)
    time.sleep(1.5)
    campo_transportador.send_keys(Keys.TAB)

    erro = verificar_se_erro(nav)
    if erro:
        fechar_todas_abas(nav)
        return erro,2
    
 
    #Preencher o Tipo
    campo_tipo = WebDriverWait(nav, 10).until(EC.element_to_be_clickable((
        By.XPATH, '//input[@name="TIPO"]')))  #Campo Tipo
    campo_tipo.click()
    campo_tipo.send_keys('NFe')
    time.sleep(1.5)
    campo_tipo.send_keys(Keys.TAB)
    carregamento(nav)
    print("Preenchido campo Tipo")

    # Preencher o Série/Subserie
    campo_seriesubs = WebDriverWait(nav, 10).until(EC.element_to_be_clickable((
        By.XPATH, '//input[@name="SERIESUBS"]'))) #Campo Série Subsérie
    campo_seriesubs.send_keys('1')
    time.sleep(1.5)
    campo_seriesubs.send_keys(Keys.TAB)
    carregamento(nav)
    print("Preenchido Campo Série Subsérie")

    # Preencher o Indicação de Presença
    campo_tipo_indpres = WebDriverWait(nav, 10).until(EC.element_to_be_clickable((
        By.XPATH, '//input[@name="INDPRES"]'))) #Campo Indicação de presença
    campo_tipo_indpres.send_keys('9')
    time.sleep(1.5)
    campo_tipo_indpres.send_keys(Keys.TAB)
    carregamento(nav)

    print("Preenchido Campo Indicação de presença")

    erro = verificar_se_erro(nav)
    if erro:
        fechar_todas_abas(nav)
        return erro,2


    # Preencher Indicativo de intermediador
    campo_tipo_indintermed = WebDriverWait(nav, 10).until(EC.element_to_be_clickable((
        By.XPATH, '//input[@name="INDINTERMED"]'))) #Campo Indicativo de intermediador
    campo_tipo_indintermed.send_keys('s')
    time.sleep(1.5)
    campo_tipo_indintermed.send_keys(Keys.TAB)
    carregamento(nav)
    print("Preenchido Campo Indicativo de intermediador")
    

    grupo_botao_indintermed = WebDriverWait(nav, 10).until(EC.element_to_be_clickable((
        By.XPATH, '//*[@id="grLookup"]//*[@id="0"]//input[@type="checkbox"]')))
    grupo_botao_indintermed.click()
    

    botao_indintermed_ok = WebDriverWait(nav, 10).until(EC.element_to_be_clickable((
        By.XPATH, '//*[@id="grLookup"]//*[@id="buttonsBar_grLookup"]//span[@class="wf-button"]')))
    botao_indintermed_ok.click()

    print("Seleciona checkbox campo Indicativo de intermediador")
    carregamento(nav)

    botao_mudar_visao = WebDriverWait(nav, 10).until(EC.element_to_be_clickable((
        By.XPATH, '//*[@id="pedidoOuProvisao_itempedidoouprovisao"]//*[@id="changeViewButton"]')))
    botao_mudar_visao.click()
    print("Selecionado Campo mudar visão")
    carregamento(nav)
    
    #preencher o campo volume
    campo_qtd_volumes = WebDriverWait(nav,10).until(EC.element_to_be_clickable((
        By.XPATH,'//input[@name="VOLQDE"]')))
    campo_qtd_volumes.click()
    campo_qtd_volumes.send_keys(volume)
    carregamento(nav)
    campo_qtd_volumes.send_keys(Keys.TAB)
    print("Preenchido Campo Volume")

    # conferir impostos

    # calcular BC ICMS, ICMS, BC PIS e COFINS, PIS, COFINS

    # guardar os valores dos impostos na planilha
    impostos_pedido = 0
    
    for i in range(0,quantidade_produtos):

        # Guardando o valor do item
        campo_item = WebDriverWait(nav,10).until(EC.element_to_be_clickable((
            By.XPATH,'//*[@id="pedidoOuProvisao_itempedidoouprovisao"]//input[@name="ITEM"]')))
        valor_produto = float(campo_item.get_attribute("value"))
        print("Coletado valor do item")
        
        campo_recurso = WebDriverWait(nav,10).until(EC.element_to_be_clickable((
            By.XPATH,'//*[@id="pedidoOuProvisao_itempedidoouprovisao"]//input[@name="RECURSO"]')))
        recurso = campo_recurso.get_attribute("value")
        print("Coletado nome do recurso")

        # Definindo a função utilizada com base tipo de venda

        if venda_interestadual:
            bc_icms, icms, bc_pis_cofins, pis, cofins = calculo_VInterestadual(valor_produto)
            print(calculo_VInterestadual(valor_produto))
        else:
            bc_icms, icms, bc_pis_cofins, pis, cofins = calculo_VInterno(valor_produto)
            print(calculo_VInterno(valor_produto))

        #valida campo BC ICMS    
        campo_bc_icms = WebDriverWait(nav,10).until(EC.element_to_be_clickable((
            By.XPATH,'//*[@id="pedidoOuProvisao_itempedidoouprovisao"]//input[@name="ICMSBC"]')))
        valor_bc_icms = float(campo_bc_icms.get_attribute("value"))
        print("Coletado campo BC ICMS")

        if valor_bc_icms != bc_icms:
            fechar_todas_abas(nav)
            return 'O campo BC ICMS não confere', 3
        print("Validado campo BC ICMS")
        
        # validar campo ICMS próprio
        campo_icms = WebDriverWait(nav,10).until(EC.element_to_be_clickable((
            By.XPATH,'//*[@id="pedidoOuProvisao_itempedidoouprovisao"]//input[@name="ICMSPROPRIO"]')))
        valor_icms = float(campo_icms.get_attribute("value"))
        print("Coletado campo ICMS")

        if valor_icms != icms:
            fechar_todas_abas(nav)
            return "O campo ICMS não confere",3
        print("Validado campo ICMS")
        
        # validar campo bc_pis_cofins
        campo_bc_pis_cofins = WebDriverWait(nav,10).until(EC.element_to_be_clickable((
            By.XPATH,'//*[@id="pedidoOuProvisao_itempedidoouprovisao"]//input[@name="COFINSBC"]')))
        
        valor_bc_pis_cofins = float(campo_bc_pis_cofins.get_attribute("value"))
        print("Coletado campo BC COFINS")

        if valor_bc_pis_cofins != bc_pis_cofins:
            fechar_todas_abas(nav)
            return "O campo BC PIS COFINS não confere",3
        print("Validado campo BC COFINS")

        # validar campo pis 
        campo_pis = WebDriverWait(nav,10).until(EC.element_to_be_clickable((
            By.XPATH,'//*[@id="pedidoOuProvisao_itempedidoouprovisao"]//input[@name="PIS"]')))
        
        valor_campo_pis = float(campo_pis.get_attribute("value"))
        print("Coletado campo PIS")
        
        if valor_campo_pis != pis:
            fechar_todas_abas(nav)
            return "O campo PIS não confere",3
        print("Validado campo PIS")
        
        # validar campo cofins
        campo_cofins = WebDriverWait(nav,10).until(EC.element_to_be_clickable((
            By.XPATH,'//*[@id="pedidoOuProvisao_itempedidoouprovisao"]//input[@name="COFINS"]')))
        
        valor_campo_cofins = float(campo_cofins.get_attribute("value"))
        print("Coletado campo COFINS")
        
        if valor_campo_cofins != cofins:
            fechar_todas_abas(nav)
            return "O campo COFINS não confere",3
        print("Validado campo COFINS")
        
        # ZONA FRANCA - Deduzir do valor total da nota a quantidade de impostos
        if zona_franca:
            impostos_pedido += icms + pis + cofins
            valor_total_pedido += impostos_pedido
            print("Deduzido valor do item na nota")

        # Preencher a planilha com os impostos do item específico
        itens, sheet = busca_worksheet("IMPOSTOS")
        sheet.append_row([chave,recurso,bc_icms,icms,bc_pis_cofins,pis,cofins,"Sucesso"])
        print("IMPOSTOS preenchidos na planilha de impostos ")
        # iframes(nav)
        # Aperta o next_button até o último item
        next_button = WebDriverWait(nav,10).until(EC.element_to_be_clickable((
            By.XPATH,'//*[@id="pedidoOuProvisao_itempedidoouprovisao"]//*[@id="trButtonsBar_pedidoOuProvisao_itempedidoouprovisao"]//td[@class="grid-buttonBar-active"]//*[@id="nextButton"]')))
        next_button.click()
        print("Selecionado próximo item")

    try:
        # Verificar valor do pedido caso ZONA FRANCA
        if zona_franca:
            if valor_total_pedido != valor_total:
                fechar_todas_abas(nav)
                return "Valor total do pedido não confere (ZF)",3
            print("Validado valor do pedido (ZF)")
        
        #confirmar pedido
        post_button = WebDriverWait(nav, 10).until(EC.element_to_be_clickable((
            By.XPATH, '//*[@id="pedidoOuProvisao_itempedidoouprovisao"]//*[@id="postButton"]')))
        post_button.click()
        print("Pressionado botão de confirmar pedido")

        #clicar em Calcular
        nav.switch_to.default_content() # sair do iframe
        grupo_botao_calcular = WebDriverWait(nav, 10).until(EC.element_to_be_clickable((
            By.XPATH, '//*[@id="buttonsCell"]//td[@class="buttonsContainer"]//span[@class="wf-button default"]')))
        grupo_botao_calcular.click()
        print("Pressionado botão calcular")
        if carregamento(nav) == 0:
            nav.switch_to.default_content() # sair do iframe
            grupo_botao_calcular.click()
            carregamento(nav)

        # validações e conferência dos dados

        # clicar em emitir NF
        nav.switch_to.default_content() # sair do iframe
        emitir_nf_button = WebDriverWait(nav, 10).until(EC.element_to_be_clickable((
            By.XPATH,'/html/body/div[4]/div/div[1]/table/tbody/tr/td[2]/table/tbody/tr/td[13]/span[2]')))
        
        # //*[@id="buttonsCell"]//td[@class="buttonsContainer"]//span[@class="wf-button"]//p[text()="0Emitir NF"]'
        emitir_nf_button.click()
        print("Pressionado botão Emitir NF")
        if carregamento(nav) == 0:
            nav.switch_to.default_content() # sair do iframe
            emitir_nf_button.click()
            print("Tentativa de outro clique")
            carregamento(nav)

        # # clicar em Sim
        nav.switch_to.default_content() # sair do iframe
        sim_nf_button = WebDriverWait(nav, 10).until(EC.element_to_be_clickable((
            By.XPATH, '//*[@id="promptMessageBox"]//*[@id="answers_0"]')))
        sim_nf_button.click()
        print("Pressionado botão SIM - Confirmar Emissão NF")
        carregamento(nav)

        erro = verificar_se_erro(nav)
        if erro:
            fechar_todas_abas(nav)
            return erro,2
        
        # fechar aba 
        # nav.switch_to.default_content() # sair do iframe
        fechar_todas_abas(nav)

        #retorna status ok para a planilha
        status = 'Ok'

        return status,1
    except Exception as e:
        erro = f"Erro encontrado: {e}"
        fechar_todas_abas(nav)
        return erro,2

# loop for
def main():
    # 1° etapa: acessar site 
    chrome_driver_path = verificar_chrome_driver() # Verificação do driver do chrome
    nav = webdriver.Chrome()#chrome_driver_path) # Inicia o navegador
    nav.maximize_window() # Maximiza a tela
    # nav.get("http://127.0.0.1/sistema") # base de produção
    nav.get("http://192.168.3.140/sistema") # base de produção
    # nav.get("https://hcemag.innovaro.com.br/sistema") # base de teste

    # 2° etapa: Login
    login(nav)

    itens,sheet = buscar_itens('Relação de CH - Faturamento')

    #iterrows

    #index é a linha da planilha
    for index, row in itens.iterrows():
        print(row)
        if row['CH Pedido'] == None:
            break

        status,codigo_status = automacao_faturamento(nav,row['Data do pedido'], row['CH Pedido'],float(row['Valor total do pedido'].replace(".","").replace(",",".")), row['Transportador'], row['Volume'])

        # status = [[status]]
        intervalo = f'G{index+1}:H{index+1}'

        # escrever na planilha o status
        sheet.update(intervalo,[[status,codigo_status]])
        print(status)
        
    nav.close()

if __name__ == "__main__":
    main()