import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Cria as variáveis de entrada
temperatura = ctrl.Antecedent(np.arange(60, 111, 1), 'temperatura')
corrente = ctrl.Antecedent(np.arange(90, 131, 1), 'corrente')
superaquecimento = ctrl.Antecedent(np.arange(2, 9, 1), 'superaquecimento')
temperatura_ar_condensador = ctrl.Antecedent(np.arange(5, 41, 1), 'temperatura_ar_condensador')
tempo_vida_util = ctrl.Antecedent(np.arange(0, 61, 1), 'tempo_vida_util')

# Cria a variável de saída
probabilidade_quebra = ctrl.Consequent(np.arange(0, 101, 1), 'probabilidade_quebra')

# Definição dos conjuntos fuzzy para temperatura
temperatura['baixa'] = fuzz.trimf(temperatura.universe, [60, 60, 85])
temperatura['média'] = fuzz.trimf(temperatura.universe, [70, 85, 100])
temperatura['alta'] = fuzz.trimf(temperatura.universe, [85, 110, 110])

# Definição dos conjuntos fuzzy para corrente
corrente['baixa'] = fuzz.trimf(corrente.universe, [90, 90, 110])
corrente['média'] = fuzz.trimf(corrente.universe, [100, 110, 120])
corrente['alta'] = fuzz.trimf(corrente.universe, [110, 130, 130])

# Definição dos conjuntos fuzzy para superaquecimento
superaquecimento['baixo'] = fuzz.trimf(superaquecimento.universe, [2, 2, 5])
superaquecimento['médio'] = fuzz.trimf(superaquecimento.universe, [3, 5, 7])
superaquecimento['alto'] = fuzz.trimf(superaquecimento.universe, [5, 8, 8])

# Definição dos conjuntos fuzzy para temperatura do ar no condensador
temperatura_ar_condensador['baixa'] = fuzz.trimf(temperatura_ar_condensador.universe, [5, 5, 22.5])
temperatura_ar_condensador['média'] = fuzz.trimf(temperatura_ar_condensador.universe, [15, 22.5, 30])
temperatura_ar_condensador['alta'] = fuzz.trimf(temperatura_ar_condensador.universe, [22.5, 40, 40])

# Definição dos conjuntos fuzzy para tempo de vida útil
tempo_vida_util['baixo'] = fuzz.trimf(tempo_vida_util.universe, [0, 0, 30])
tempo_vida_util['médio'] = fuzz.trimf(tempo_vida_util.universe, [10, 30, 50])
tempo_vida_util['alto'] = fuzz.trimf(tempo_vida_util.universe, [30, 60, 60])

# Definição dos conjuntos fuzzy para probabilidade de quebra
probabilidade_quebra['baixa'] = fuzz.trimf(probabilidade_quebra.universe, [0, 0, 50])
probabilidade_quebra['média'] = fuzz.trimf(probabilidade_quebra.universe, [20, 50, 80])
probabilidade_quebra['alta'] = fuzz.trimf(probabilidade_quebra.universe, [50, 100, 100])

# Regras fuzzy
regra1 = ctrl.Rule(temperatura['alta'] | corrente['alta'] | superaquecimento['alto'] | temperatura_ar_condensador['alta'] | tempo_vida_util['baixo'], probabilidade_quebra['alta'])
regra2 = ctrl.Rule(temperatura['média'] & corrente['média'] & superaquecimento['médio'] & temperatura_ar_condensador['média'] & tempo_vida_util['médio'], probabilidade_quebra['média'])
regra3 = ctrl.Rule(temperatura['baixa'] & corrente['baixa'] & superaquecimento['baixo'] & temperatura_ar_condensador['baixa'] & tempo_vida_util['alto'], probabilidade_quebra['baixa'])

# Sistema de controle
sistema_controle = ctrl.ControlSystem([regra1, regra2, regra3])
sistema = ctrl.ControlSystemSimulation(sistema_controle)

# Simulação
sistema.input['temperatura'] = 90
sistema.input['corrente'] = 110
sistema.input['superaquecimento'] = 4
sistema.input['temperatura_ar_condensador'] = 20
sistema.input['tempo_vida_util'] = 40

# Computa o resultado
sistema.compute()

# Resultado
probabilidade_quebra_value = sistema.output['probabilidade_quebra']
# Limita a probabilidade entre 0 e 100
probabilidade_quebra_value = min(max(probabilidade_quebra_value, 0), 100)
probabilidade_quebra_value_percent = round(probabilidade_quebra_value, 1)
print("Probabilidade de quebra:", "{:.1f}%".format(probabilidade_quebra_value_percent))
