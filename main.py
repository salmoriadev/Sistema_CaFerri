"""
Ponto de entrada principal do Sistema CaFerri.

Este módulo é responsável por inicializar o sistema de gerenciamento de cafés,
máquinas de café, clientes, fornecedores, estoque e vendas. Ao ser executado,
cria uma instância do ControladorSistema, que orquestra toda a aplicação e
gerencia o fluxo de navegação entre os diferentes módulos do sistema.

O sistema utiliza arquitetura em camadas (MVC), com separação clara entre:
- Camada de Apresentação (limite/): Interfaces gráficas com o usuário
- Camada de Controle (controle/): Lógica de negócio e orquestração
- Camada de Dados (entidade/ e DAOs/): Modelos de dados e persistência
"""

from controle.controladorSistema import ControladorSistema

if __name__ == "__main__":
    controlador_principal = ControladorSistema()
    controlador_principal.inicializa_sistema()
