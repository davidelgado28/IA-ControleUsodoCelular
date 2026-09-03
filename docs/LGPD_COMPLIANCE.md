# Diretrizes de Privacidade e Conformidade Legal
## Sistema de Monitoramento Escolar via Webcam para Identificação de Uso de Smartphones

**Documento elaborado por:** David Carlos Miranda Delgado
**Finalidade do sistema:** Apoio à gestão de atenção em sala de aula por meio da identificação, em tempo real, do uso de smartphones por estudantes
**Base normativa principal:** Lei nº 13.709/2018 (LGPD), com atenção especial ao art. 14 (tratamento de dados de crianças e adolescentes)

---

## 1. Objetivo e Escopo

Este documento estabelece as diretrizes mínimas de governança de dados e privacidade que devem ser observadas no desenvolvimento, implantação e operação do sistema de monitoramento por webcam. Ele se aplica a:

- Captura de imagem em salas de aula;
- Processamento de imagem por algoritmos de visão computacional para detecção de smartphones;
- Qualquer armazenamento, transmissão ou exibição de dados derivados dessa captura;
- Todos os agentes envolvidos: mantenedora escolar (controladora), fornecedor de tecnologia (operador), corpo docente e gestão pedagógica (usuários finais).

Este projeto trata de **dados de crianças e adolescentes**, categoria à qual a LGPD atribui proteção reforçada. Qualquer decisão de design deve partir do princípio do **melhor interesse da criança e do adolescente** (art. 14, *caput*, c/c ECA e Marco Civil da Internet).

---

## 2. Princípios da LGPD Aplicáveis ao Projeto

| Princípio (art. 6º) | Aplicação prática no sistema |
|---|---|
| Finalidade | O sistema só pode ser usado para apoio pedagógico à gestão de atenção e nunca para avaliação disciplinar automatizada, punição ou perfilamento individual de comportamento. |
| Necessidade | Coletar o mínimo de dado biométrico/de imagem necessário para detectar o objeto "smartphone", evitando reconhecimento facial nominal quando não for indispensável. |
| Não discriminação | O modelo não pode gerar decisões automatizadas que resultem em tratamento discriminatório de estudantes. |
| Transparência | Alunos, pais e responsáveis devem ser informados de forma clara sobre a existência, funcionamento e finalidade do sistema. |
| Segurança e prevenção | Medidas técnicas e administrativas para evitar acesso não autorizado, vazamento ou uso indevido. |
| Responsabilização (accountability) | Registro documental de todas as decisões de tratamento e das medidas de mitigação de risco adotadas. |

---

## 3. Anonimização Automática de Rostos (Face Blurring)

### 3.1 Regra geral
O sistema deve aplicar **desfoque (blur) ou pixelização automática de todos os rostos captados**, como etapa obrigatória do pipeline de processamento, **antes** de qualquer armazenamento, exibição em dashboard ou exportação de imagem.

### 3.2 Especificações técnicas mínimas
- O blurring deve ocorrer **em tempo real, na borda (edge)** ou no primeiro estágio de processamento, nunca após persistência da imagem original.
- A imagem bruta (sem blur) não deve ser gravada em disco, nem mesmo temporariamente, salvo em buffer de memória volátil necessário à inferência do modelo (descartado imediatamente após o processamento, em milissegundos).
- Apenas metadados não identificáveis podem ser persistidos: por exemplo, "smartphone detectado às 14h32, fileira 3", sem vínculo a rosto ou identidade.
- Deve haver **auditoria técnica periódica** (trimestral, no mínimo) para validar que nenhum frame com rosto não anonimizado é armazenado, incluindo logs de erro e cópias de cache temporário.
- Caso o sistema utilize algum grau de reconhecimento facial para outra finalidade (ex.: controle de presença), essa função deve ser **segregada tecnicamente e legalmente** da função de detecção de smartphones, com base legal e consentimento próprios.

### 3.3 Falhas do sistema de blurring
- Em caso de falha na anonimização (ex: rosto não detectado pelo algoritmo de blur), o frame correspondente deve ser **descartado automaticamente**, não devendo haver fallback que armazene a imagem sem tratamento.
- Deve existir mecanismo de "kill switch" que interrompe a captura em caso de falha sistêmica do módulo de anonimização.

---

## 4. Política de Retenção Mínima de Dados

### 4.1 Princípio orientador
Nenhum dado (nem mesmo anonimizado), deve ser guardado por período superior ao estritamente necessário à finalidade pedagógica de gestão de atenção.

### 4.2 Prazos sugeridos por tipo de dado

| Tipo de dado | Prazo de retenção sugerido | Justificativa |
|---|---|---|
| Imagem bruta (com rosto) | **Não persiste** (0 segundos além do buffer de inferência) | Não há finalidade legítima para retê-la |
| Imagem com blur aplicado | Até 24–72h (apenas se necessário para auditoria técnica do próprio algoritmo) | Permite verificação de falso positivo/negativo pontual |
| Metadados agregados e anonimizados (contagem de eventos por turma/horário) | Até o fim do semestre letivo, renovável mediante nova avaliação de necessidade | Uso pedagógico e estatístico agregado |
| Logs técnicos de sistema (sem dado pessoal) | 90 dias | Segurança da informação e auditoria técnica |
| Relatórios individualizados nominais (se algum dia existirem) | **Não recomendado.** Caso exista exigência pedagógica específica, retenção máxima de 30 dias e apenas mediante base legal e finalidade documentadas | Minimização de risco a direitos de crianças/adolescentes |

### 4.3 Descarte
- O descarte deve ser **automatizado** (rotina programada), não dependente de ação manual.
- Deve haver certificado ou log de eliminação, para fins de comprovação de conformidade perante a ANPD, pais/responsáveis ou auditoria interna.
- Backups devem seguir a mesma política de retenção — dado eliminado da base principal não pode "sobreviver" indefinidamente em backup.

---

## 5. Base Legal e Consentimento no Ambiente Escolar

### 5.1 Base legal aplicável
Para tratamento de dados de crianças e adolescentes, a LGPD (art. 14, §1º) exige, em regra, **consentimento específico e em destaque dado por pelo menos um dos pais ou responsável legal**, exceto quando o tratamento for necessário para proteger a vida/incolumidade física do titular, ou dispensado por lei.

Recomendações:
- **Consentimento informado dos responsáveis**, coletado em linguagem simples e acessível, específico para esta finalidade (detecção de uso de smartphone), separado de outros consentimentos genéricos da matrícula escolar.
- Alternativamente, avaliar se a base legal pode ser fundamentada em **legítimo interesse da escola no cumprimento de sua função pedagógica** mas, tratando-se de crianças/adolescentes, a ANPD e a doutrina majoritária recomendam cautela redobrada e preferência pelo consentimento explícito sempre que viável.
- Direito de **oposição/recusa sem prejuízo**: famílias que não consentirem não podem sofrer prejuízo pedagógico, disciplinar ou de acesso a serviços escolares.

### 5.2 Transparência ativa
- Aviso de Privacidade específico do sistema, disponibilizado antes da implantação, contendo: finalidade, tipos de dados tratados, prazo de retenção, medidas de anonimização, direitos dos titulares e canal de contato do Encarregado (DPO).
- Sinalização física/visual nas salas de aula informando a existência de monitoramento por câmera.
- Comunicação também direcionada aos próprios estudantes, em linguagem adequada à idade, explicando o funcionamento do sistema.

---

## 6. Direitos dos Titulares (Alunos e Responsáveis)

Devem ser assegurados os direitos do art. 18 da LGPD, com fluxo de atendimento definido:
- Confirmação da existência de tratamento;
- Acesso aos dados (quando existentes e identificáveis);
- Correção de dados incompletos ou desatualizados;
- Eliminação de dados tratados com consentimento;
- Informação sobre entidades com as quais o controlador compartilhou dados (ex.: fornecedor de tecnologia);
- Revogação do consentimento a qualquer momento, sem efeito retroativo, mas com efeitos imediatos sobre tratamentos futuros.

Deve ser designado canal claro (e-mail, formulário) para exercício desses direitos, com prazo de resposta definido internamente (sugestão: até 15 dias corridos).

---

## 7. Medidas de Segurança Técnicas e Administrativas

- Criptografia em trânsito e em repouso para qualquer dado remanescente (mesmo anonimizado).
- Controle de acesso baseado em papéis (RBAC): apenas gestão pedagógica autorizada acessa relatórios agregados; nenhum professor individual deve ter acesso a fluxo de vídeo bruto.
- Segregação de ambientes entre fornecedor de tecnologia (operador) e escola (controladora), com contrato de operação de dados (art. 39 da LGPD) detalhando obrigações, sub-operadores e responsabilidades em caso de incidente.
- Plano de resposta a incidentes de segurança, com procedimento de comunicação à ANPD e aos titulares em caso de vazamento, conforme art. 48 da LGPD.
- Realização de **Relatório de Impacto à Proteção de Dados Pessoais (RIPD)** antes da implantação, dada a natureza sensível do público infantojuvenil e o uso de tecnologia de visão computacional.

---

## 8. Governança e Responsabilidades

| Papel | Responsabilidade |
|---|---|
| Controlador (mantenedora escolar) | Define finalidade, base legal, obtém consentimento, responde a titulares |
| Operador (fornecedor de tecnologia) | Implementa medidas técnicas (blurring, retenção, segurança), segue instruções do controlador, não trata dado para finalidade própria |
| Encarregado (DPO) | Ponto de contato com titulares e ANPD, supervisiona conformidade, revisa RIPD |
| Comitê de Ética/Pedagógico interno | Avalia periodicamente se a finalidade pedagógica ainda justifica o uso da tecnologia, considerando alternativas menos invasivas |

---

## 9. Recomendações Adicionais de Mitigação de Risco

- **Privacidade desde a concepção (privacy by design) e por padrão (by default)**: todas as configurações padrão do sistema devem ser as mais protetivas possíveis (blur ativado por padrão, retenção mínima por padrão).
- **Minimização por design de detecção**: sempre que tecnicamente possível, preferir modelos que detectem o **objeto "smartphone"** sem necessidade de processar ou reter dados biométricos faciais em qualquer etapa, mesmo que descartados posteriormente.
- **Vedação a perfilamento individual**: o sistema não deve gerar "pontuação de atenção" ou ranking individualizado de estudantes vinculado à imagem ou identidade.
- **Revisão periódica** (recomendação: semestral) da real necessidade e proporcionalidade do sistema, com possibilidade de descontinuação caso o benefício pedagógico não se confirme.

---

## 10. Auditoria e Revisão do Documento

Este documento deve ser revisado:
- A cada alteração relevante no sistema (mudança de fornecedor, novo modelo de IA, nova finalidade);
- Sempre que houver atualização regulatória da ANPD sobre dados de crianças e adolescentes ou sobre videomonitoramento;
- No mínimo, anualmente, pelo Encarregado de Dados (DPO) em conjunto com a gestão pedagógica.

---

*Este documento é uma diretriz de governança e não substitui parecer jurídico formal. Recomenda-se validação por assessoria jurídica especializada em proteção de dados antes da implantação do sistema, bem como elaboração do RIPD específico do projeto.*
