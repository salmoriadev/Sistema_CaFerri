# Sistema de Gestão de e-commerce, o "CaFerri"

Um sistema de gerenciamento completo para um e-commerce de café especializado, desenvolvido em Python. A aplicação segue os princípios da arquitetura Model-View-Controller (MVC) para garantir organização, manutenibilidade e escalabilidade.

## 📖 Sobre o Projeto

O "Caferri" é uma solução de software projetada para um e-commerce inovador de café. Ele permite o controle total sobre produtos, fornecedores, clientes, estoque e transações de venda, além de gerar relatórios estratégicos para auxiliar na tomada de decisões de negócio.

---

## ✨ Funcionalidades Principais

O sistema é dividido em módulos coesos, cada um com responsabilidades bem definidas:

#### 📦 Gestão de Produtos e Fornecedores
- **Cadastro de Cafés:** Adicione novos tipos de café com atributos detalhados (origem, variedade, altitude, moagem, notas sensoriais, perfil recomendado, etc.).
- **Cadastro de Máquinas de Café:** Gerencie os equipamentos disponíveis para venda com informações completas.
- **Gestão de Fornecedores:** Mantenha um registro de fornecedores de cafés e de máquinas, associando cada produto à sua origem. Validação de CNPJ único para garantir integridade dos dados.

#### 👤 Gestão de Clientes
- **Cadastro completo de clientes:** Gerencie informações como ID, nome, e-mail, saldo e perfil de consumo.
- **Recomendações Personalizadas:** O sistema sugere cafés com base no perfil de sabor de cada cliente (Doce e Suave, Ácido e Frutado, Intenso e Encorpado, Equilibrado e Completo), melhorando a experiência de compra.
- **Segurança:** As senhas dos clientes são armazenadas de forma segura utilizando hashing SHA-256.
- **Validação de senha:** Operações críticas (alteração e exclusão) requerem confirmação de senha.

#### 📈 Gestão de Vendas
- **Carrinho de Compras Interativo:** Inicie vendas, adicione/remova produtos e ajuste quantidades em tempo real.
- **Validação de Transações:** O sistema valida o saldo do cliente e a disponibilidade de produtos no estoque antes de finalizar uma venda, garantindo a integridade dos dados.
- **Histórico de Vendas:** Todas as transações são registradas para futuras consultas e relatórios.
- **Vendas em andamento:** Possibilidade de salvar vendas para continuar depois.

#### 🏭 Gestão de Estoque
- **Controle de Inventário:** Adicione novos produtos ao estoque, realize reposições e dê baixas manuais.
- **Atualização Automática:** O estoque é abatido automaticamente após a finalização de uma venda.
- **Validação de disponibilidade:** Sistema impede vendas de produtos sem estoque suficiente.

#### 📊 Geração de Relatórios
- **Relatórios de Desempenho:** Obtenha insights valiosos com relatórios como:
  - Vendas finalizadas e faturamento total.
  - Produtos (cafés e máquinas) mais vendidos.
  - Clientes que mais gastam.
  - Fornecedores mais ativos.
  - Produtos com estoque baixo (abaixo de 5 unidades).

---

## 🏛️ Arquitetura e Estrutura do Projeto

O sistema foi desenvolvido seguindo o padrão arquitetural **Model-View-Controller (MVC)**, que separa as responsabilidades da aplicação em três camadas distintas:

### Estrutura de Diretórios

```
Sistema_CaFerri/
├── 📁 controle/          # Camada Controller (Lógica de Negócio)
│   ├── controladorSistema.py
│   ├── controladorCafe.py
│   ├── controladorCliente.py
│   ├── controladorVenda.py
│   ├── controladorEstoque.py
│   ├── controladorMaquinaDeCafe.py
│   ├── controladorEmpresaCafe.py
│   ├── controladorEmpresaMaquina.py
│   ├── controladorRelatorio.py
│   └── buscaProdutoMixin.py
│
├── 📁 limite/            # Camada View (Interface Gráfica)
│   ├── telaSistema.py
│   ├── telaCafe.py
│   ├── telaCliente.py
│   ├── telaVenda.py
│   ├── telaEstoque.py
│   ├── telaMaquinaDeCafe.py
│   ├── telaEmpresaCafe.py
│   ├── telaEmpresaMaquina.py
│   └── telaRelatorio.py
│
├── 📁 entidade/          # Camada Model (Dados e Regras de Negócio)
│   ├── produto.py
│   ├── cafe.py
│   ├── maquina_de_cafe.py
│   ├── cliente.py
│   ├── venda.py
│   ├── estoque.py
│   ├── empresa_fornecedora.py
│   ├── fornecedora_cafe.py
│   ├── fornecedora_maquina.py
│   └── perfil_consumidor.py
│
├── 📁 DAOs/              # Data Access Objects (Persistência)
│   ├── dao.py
│   ├── cafe_dao.py
│   ├── cliente_dao.py
│   ├── venda_dao.py
│   ├── estoque_dao.py
│   ├── maquina_de_cafe_dao.py
│   ├── fornecedora_cafe_dao.py
│   └── fornecedora_maquina_dao.py
│
├── 📁 Excecoes/          # Exceções Customizadas
│   ├── produtoNaoEncontradoException.py
│   ├── clienteNaoEncontradoException.py
│   ├── vendaNaoEncontradaException.py
│   └── ... (outras exceções)
│
├── main.py               # Ponto de entrada da aplicação
└── teste_completo.py     # Script de teste completo do sistema
```

### Descrição das Camadas

- **`📁 entidade/` (Model):** Contém as classes que representam os dados e as regras de negócio do sistema (ex: `Cafe`, `Cliente`, `Venda`). Elas são o coração da aplicação, encapsulando toda a lógica de domínio.

- **`📁 limite/` (View):** Composta pelas classes de "Tela" (ex: `TelaCafe`, `TelaCliente`). Utiliza FreeSimpleGUI para criar interfaces gráficas modais e responsivas. Sua única responsabilidade é interagir com o usuário, exibindo informações e capturando entradas.

- **`📁 controle/` (Controller):** Orquestra a lógica da aplicação. As classes de "Controlador" (ex: `ControladorCafe`, `ControladorSistema`) fazem a ponte entre a View e o Model, processando as ações do usuário e manipulando os dados através dos DAOs.

- **`📁 DAOs/` (Data Access Objects):** Responsáveis pela persistência de dados utilizando o módulo `pickle` do Python. Cada entidade possui seu próprio DAO que gerencia operações CRUD (Create, Read, Update, Delete) e mantém um cache em memória sincronizado com arquivos `.pkl`.

- **`📁 Excecoes/`:** Contém as exceções customizadas do projeto, permitindo um tratamento de erros mais específico e claro, melhorando a experiência do desenvolvedor e facilitando o debug.

### Padrões de Design Utilizados

- **MVC (Model-View-Controller):** Separação clara de responsabilidades
- **DAO (Data Access Object):** Abstração da camada de persistência
- **Mixin Pattern:** Reutilização de código através de `BuscaProdutoMixin`
- **Facade Pattern:** `ControladorSistema` atua como fachada para todos os módulos
- **Exception Handling:** Tratamento robusto de erros com exceções customizadas

---

## 💻 Tecnologias Utilizadas

- **Python 3:** Linguagem principal do projeto
- **FreeSimpleGUI:** Biblioteca para criação de interfaces gráficas
- **pickle:** Módulo padrão do Python para serialização de objetos
- **hashlib:** Módulo padrão do Python para criptografia de senhas (SHA-256)

---

## 🚀 Instalação e Execução

Como o projeto utiliza apenas bibliotecas padrão do Python e FreeSimpleGUI, sua execução é bastante simples.

### Pré-requisitos

- Python 3.7 ou superior
- FreeSimpleGUI (instalado via pip)

### Instalação

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/salmoriadev/Sistema_CaFerri.git
   ```

2. **Navegue até a pasta do projeto:**
   ```bash
   cd Sistema_CaFerri
   ```

3. **Instale as dependências:**
   ```bash
   pip install FreeSimpleGUI
   ```

4. **Execute o arquivo principal:**
   ```bash
   python main.py
   ```

Após a execução, o menu principal do sistema será exibido e você poderá interagir com todas as suas funcionalidades através da interface gráfica.



## 📝 Persistência de Dados

O sistema utiliza arquivos `.pkl` (pickle) para persistência de dados. Os arquivos são criados automaticamente na primeira execução:

- `cafes.pkl` - Dados dos cafés cadastrados
- `clientes.pkl` - Dados dos clientes
- `vendas.pkl` - Histórico de vendas
- `maquinas.pkl` - Dados das máquinas de café
- `fornecedores_cafe.pkl` - Dados dos fornecedores de café
- `fornecedores_maquina.pkl` - Dados dos fornecedores de máquinas
- `estoque.pkl` - Estado atual do estoque


---

## 📚 Documentação

O projeto possui documentação completa em todos os arquivos:

- **Docstrings em todas as classes:** Explicam o propósito e responsabilidades de cada classe
- **Docstrings em todos os métodos:** Descrevem funcionalidade, parâmetros e retornos
- **Documentação de módulos:** Explicam o contexto e relacionamentos entre componentes

A documentação segue padrões consistentes e facilita a manutenção e compreensão do código.

---

## 🧪 Testes

O projeto inclui um arquivo de teste completo (`teste_completo.py`) que:

- Cria fornecedores, clientes e produtos
- Popula o estoque
- Cria e finaliza vendas
- Gera relatórios e estatísticas
- Valida todas as funcionalidades principais do sistema

---

## 🔒 Segurança

- **Senhas:** Todas as senhas são criptografadas usando SHA-256 antes de serem armazenadas
- **Validação de dados:** O sistema valida entradas do usuário antes de processar operações
- **Integridade referencial:** Validações garantem que produtos só sejam criados se seus fornecedores existirem
- **Validação de saldo:** Sistema impede vendas quando o cliente não possui saldo suficiente
- **Validação de estoque:** Sistema impede vendas quando não há produtos suficientes em estoque

---

## 🎯 Funcionalidades de Negócio

### Regras de Negócio Implementadas

1. **Validação de Fornecedores:** Não é possível cadastrar cafés ou máquinas sem fornecedores cadastrados
2. **Validação de Produtos:** Não é possível gerenciar estoque sem produtos cadastrados
3. **Validação de Clientes:** Não é possível iniciar vendas sem clientes cadastrados
4. **Validação de Estoque:** Não é possível iniciar vendas sem produtos em estoque
5. **Integridade de Vendas:** Vendas finalizadas não podem ser modificadas ou excluídas
6. **Integridade de Fornecedores:** Não é possível excluir fornecedores que possuem produtos associados
7. **Integridade de Clientes:** Não é possível excluir clientes com vendas em andamento

---

## ✍️ Autores

**Arthur de Farias Salmoria**
e
**Luigi Ferri Maines**

- LinkedIn: [Arthur Salmoria](https://linkedin.com/in/arthursalmoria/)
- LinkedIn: [Luigi Ferri](https://linkedin.com/in/luigi-ferri-maines-498ba4361/)

---

## 📄 Licença

Este projeto é de código aberto e está disponível para uso educacional e de aprendizado.

---

## 🙏 Agradecimentos

Agradecemos a todos que contribuíram para o desenvolvimento deste projeto e à comunidade Python por fornecer as ferramentas e bibliotecas que tornaram este sistema possível.
