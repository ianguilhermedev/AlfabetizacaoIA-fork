# Feature Specification: Alfabot Marajoara

**Feature Branch**: `001-alfabot-marajoara`

**Created**: 2026-06-02

**Status**: Draft

**Input**: User description: "Auxiliar na alfabetização de alunos de forma personalizada utilizando elementos e contextos da cultura marajoara, utilizando o WhatsApp como interface de acessibilidade. Aluno envia mensagem de texto ou áudio no WhatsApp; o sistema responde adaptando o vocabulário ao nível pedagógico (Iniciante, Básico, Intermediário) e integrando conhecimento local. Se o áudio estiver corrompido ou incompreensível, pedir para gravar novamente. Se o usuário for novo, iniciar fluxo interativo com botões para mapear o nível de leitura inicial."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Acolhimento e diagnóstico inicial (Priority: P1)

Como um aluno novo, quero iniciar uma conversa com o bot e responder a perguntas com botões para que o sistema descubra meu nível inicial de leitura sem exigir explicações longas.

**Why this priority**: O primeiro contato define a experiência do aluno e permite personalizar o restante da interação desde o início.

**Independent Test**: Pode ser testado iniciando uma conversa com um número nunca visto antes e verificando se o bot apresenta opções guiadas para mapear o nível de leitura.

**Acceptance Scenarios**:

1. **Given** um usuário sem histórico, **When** ele envia a primeira mensagem, **Then** o sistema inicia um fluxo interativo com botões para identificar o nível de leitura.
2. **Given** que o aluno escolhe um nível, **When** a escolha é confirmada, **Then** o sistema salva o nível inicial e prossegue com uma resposta de boas-vindas adequada.

---

### User Story 2 - Resposta adaptada ao nível do aluno (Priority: P1)

Como um aluno, quero enviar uma dúvida ou resposta em texto ou áudio e receber uma resposta com linguagem adequada ao meu nível pedagógico para conseguir acompanhar a conversa com mais facilidade.

**Why this priority**: A adaptação de linguagem é o valor central do bot e sustenta a alfabetização personalizada.

**Independent Test**: Pode ser testado com um aluno já classificado em cada nível e verificando se a resposta muda conforme o nível informado.

**Acceptance Scenarios**:

1. **Given** um aluno com nível Iniciante, **When** ele envia uma dúvida em texto, **Then** o sistema responde com vocabulário simples e frases curtas.
2. **Given** um aluno com nível Básico ou Intermediário, **When** ele envia uma resposta ou pergunta, **Then** o sistema ajusta a complexidade da linguagem ao nível correspondente.

---

### User Story 3 - Cultura marajoara nas interações (Priority: P2)

Como um aluno, quero que as interações tragam elementos da cultura marajoara para tornar o aprendizado mais próximo da minha realidade e mais interessante.

**Why this priority**: O contexto cultural diferencia o bot e reforça a aprendizagem com referências significativas.

**Independent Test**: Pode ser testado pedindo exemplos, estímulos ou explicações e verificando se a resposta inclui referências locais relevantes.

**Acceptance Scenarios**:

1. **Given** uma solicitação de explicação ou estímulo, **When** o sistema responde, **Then** a resposta inclui pelo menos um elemento cultural local relevante, como fauna, flora ou lendas do Marajó.
2. **Given** um diálogo contínuo, **When** o sistema mantém a conversa, **Then** ele preserva o contexto marajoara sem perder a clareza pedagógica.

---

### User Story 4 - Tratamento de áudio incompreensível (Priority: P2)

Como um aluno, quero receber orientação gentil quando meu áudio não puder ser entendido para que eu possa tentar novamente sem frustração.

**Why this priority**: Isso evita bloqueios na comunicação e mantém a experiência acessível.

**Independent Test**: Pode ser testado enviando um áudio corrompido ou sem fala compreensível e verificando a mensagem de fallback.

**Acceptance Scenarios**:

1. **Given** um áudio corrompido, **When** o sistema não conseguir compreender a mensagem, **Then** ele pede gentilmente para o aluno gravar novamente.
2. **Given** um áudio com ruído excessivo ou fala indecifrável, **When** a transcrição não for confiável, **Then** o sistema não inventa uma resposta e solicita nova gravação.

---

### Edge Cases

- O aluno envia apenas emojis, áudios vazios ou mensagens sem sentido pedagógico.
- O aluno novo responde fora da ordem esperada durante o fluxo inicial com botões.
- O aluno muda de nível ao longo do tempo e o sistema precisa respeitar o nível mais recente salvo.
- O bot precisa manter o contexto cultural mesmo em respostas curtas.
- A resposta precisa continuar compreensível quando o aluno usa linguagem muito informal.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: O sistema MUST iniciar um fluxo guiado para novos usuários antes de assumir qualquer nível pedagógico.
- **FR-002**: O sistema MUST permitir que o aluno interaja por mensagem de texto ou áudio.
- **FR-003**: O sistema MUST adaptar a linguagem da resposta ao nível pedagógico atual do aluno: Iniciante, Básico ou Intermediário.
- **FR-004**: O sistema MUST incluir elementos da cultura marajoara nas interações sempre que responder a dúvidas, estímulos ou explicações.
- **FR-005**: O sistema MUST pedir uma nova gravação de forma gentil quando um áudio estiver corrompido, vazio ou incompreensível.
- **FR-006**: O sistema MUST registrar o nível inicial do aluno após a conclusão do fluxo de diagnóstico.
- **FR-007**: O sistema MUST preservar o nível pedagógico salvo até que um novo diagnóstico ou atualização o substitua.
- **FR-008**: O sistema MUST oferecer botões interativos para orientar o aluno novo no fluxo inicial.
- **FR-009**: O sistema MUST responder de forma adequada ao contexto da conversa sem exigir que o aluno repita informações já fornecidas.
- **FR-010**: O sistema MUST manter a experiência acessível e acolhedora, evitando respostas que exponham falha técnica quando uma entrada não puder ser entendida.

### Key Entities *(include if feature involves data)*

- **Aluno**: representa a pessoa que interage com o bot, incluindo identificador de contato, nível pedagógico atual e histórico mínimo necessário para personalização.
- **Nível pedagógico**: representa a classificação de leitura do aluno, com os valores Iniciante, Básico e Intermediário.
- **Interação**: representa cada troca de mensagem ou áudio, incluindo o tipo de entrada, o resultado do processamento e a resposta enviada.
- **Contexto cultural**: representa os elementos marajoaras usados na conversa, como referências a fauna, flora e lendas locais.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Pelo menos 90% dos alunos novos conseguem concluir o fluxo inicial de diagnóstico sem ajuda externa.
- **SC-002**: Em pelo menos 9 de cada 10 interações válidas, a resposta é percebida como adequada ao nível pedagógico selecionado.
- **SC-003**: Em pelo menos 9 de cada 10 respostas pedagógicas, há pelo menos uma referência cultural marajoara pertinente ao conteúdo da conversa.
- **SC-004**: Em 100% dos casos em que um áudio não puder ser compreendido, o aluno recebe um pedido gentil para gravar novamente.
- **SC-005**: A maioria dos alunos consegue concluir uma interação simples em menos de 2 minutos a partir do primeiro contato.

## Assumptions

- O fluxo inicial considera apenas os níveis Iniciante, Básico e Intermediário.
- O bot atende alunos por WhatsApp como canal principal de acesso.
- As referências culturais marajoaras usadas na conversa serão apropriadas à faixa etária e ao contexto pedagógico.
- Quando o sistema não entender uma entrada de áudio, ele prioriza segurança pedagógica e pede uma nova gravação em vez de tentar adivinhar a mensagem.
- O registro do nível do aluno é suficiente para personalizar as respostas iniciais.
