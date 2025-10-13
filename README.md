# Sistema de Gestão de e-commerce, o "CaFerri"

Um sistema de gerenciamento completo para um e-commerce de café especializado, desenvolvido em Python. A aplicação segue os princípios da arquitetura Model-View-Controller (MVC) para garantir organização, manutenibilidade e escalabilidade.

## 📖 Sobre o Projeto

O "Caferri" é uma solução de software projetada para um e-commerce inovador de café. Ele permite o controle total sobre produtos, fornecedores, clientes, estoque e transações de venda, além de gerar relatórios estratégicos para auxiliar na tomada de decisões de negócio.

---

## ✨ Funcionalidades Principais

O sistema é dividido em módulos coesos, cada um com responsabilidades bem definidas:

#### 📦 Gestão de Produtos e Fornecedores
- **Cadastro de Cafés:** Adicione novos tipos de café com atributos detalhados (origem, variedade, moagem, perfil sensorial, etc.).
- **Cadastro de Máquinas de Café:** Gerencie os equipamentos disponíveis para venda.
- **Gestão de Fornecedores:** Mantenha um registro de fornecedores de cafés e de máquinas, associando cada produto à sua origem.

#### 👤 Gestão de Clientes
- **Cadastro completo de clientes:** Gerencie informações como nome, e-mail, saldo e perfil de consumo.
- **Recomendações Personalizadas:** O sistema sugere cafés com base no perfil de sabor de cada cliente, melhorando a experiência de compra.
- **Segurança:** As senhas dos clientes são armazenadas de forma segura utilizando hashing (SHA256).

#### 📈 Gestão de Vendas
- **Carrinho de Compras Interativo:** Inicie vendas, adicione/remova produtos e ajuste quantidades em tempo real.
- **Validação de Transações:** O sistema valida o saldo do cliente e a disponibilidade de produtos no estoque antes de finalizar uma venda, garantindo a integridade dos dados.
- **Histórico de Vendas:** Todas as transações são registradas para futuras consultas e relatórios.

#### 🏭 Gestão de Estoque
- **Controle de Inventário:** Adicione novos produtos ao estoque, realize reposições e dê baixas manuais.
- **Atualização Automática:** O estoque é abatido automaticamente após a finalização de uma venda.

#### 📊 Geração de Relatórios
- **Relatórios de Desempenho:** Obtenha insights valiosos com relatórios como:
  - Vendas finalizadas e faturamento total.
  - Produtos (cafés e máquinas) mais vendidos.
  - Clientes que mais gastam.
  - Fornecedores mais ativos.
  - Produtos com estoque baixo.

---

## 🏛️ Arquitetura e Estrutura do Projeto

O sistema foi desenvolvido seguindo o padrão arquitetural **Model-View-Controller (MVC)**, que separa as responsabilidades da aplicação em três camadas distintas:

- `📁 entidade/` (**Model**): Contém as classes que representam os dados e as regras de negócio do sistema (ex: `Cafe`, `Cliente`, `Venda`). Elas são o coração da aplicação.

- `📁 limite/` (**View**): Composta pelas classes de "Tela" (ex: `TelaCafe`, `TelaCliente`). Sua única responsabilidade é interagir com o usuário, exibindo informações e capturando entradas via console.

- `📁 controle/` (**Controller**): Orquestra a lógica da aplicação. As classes de "Controlador" (ex: `ControladorCafe`, `ControladorSistema`) fazem a ponte entre a View e o Model, processando as ações do usuário e manipulando os dados.

#### Outras Pastas:
- `📁 Excecoes/`: Contém as exceções customizadas do projeto, permitindo um tratamento de erros mais específico e claro.
- `main.py`: Ponto de entrada da aplicação, responsável por instanciar o `ControladorSistema` e iniciar o programa.

O projeto também faz uso de **Mixins** (como o `BuscaProdutoMixin`) para promover o reuso de código e evitar a duplicação de lógicas de busca entre diferentes controladores.

---

## 💻 Tecnologias Utilizadas

- **Python 3:** Linguagem principal do projeto.

---

## 🚀 Instalação e Execução

Como o projeto não possui dependências externas, sua execução é bastante simples.

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/salmoriadev/Sistema_CaFerri.git
    ```

2.  **Navegue até a pasta do projeto:**
    ```bash
    cd Sistema_CaFerri
    ```

3.  **Execute o arquivo principal:**
    ```bash
    python3 main.py
    ```

Após a execução, o menu principal do sistema será exibido no console e você poderá interagir com todas as suas funcionalidades.

---

## ✍️ Autores

**Arthur de Farias Salmoria**
e
**Luigi Ferri Maines**

- LinkedIn: [Arthur Salmoria](https://linkedin.com/in/arthursalmoria/)
- LinkedIn: [Luigi Ferri](https://linkedin.com/in/luigi-ferri-maines-498ba4361/)
