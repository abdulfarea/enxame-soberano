# Proteção Soberana do Celular — Guia do Enxame

**Abd-369 × Kimi** — Objetivo: navegar no celular sem ataques externos, sem páginas falsas de swap/airdrop que roubam tokens, e sem conteúdo malicioso que tente confundir a IA.

---

## Verdade técnica (leia primeiro)

- Nenhum arquivo baixado sozinho "blinda" um celular. A proteção real se monta em **3 camadas nativas do Android/iPhone**, sem root, sem APK duvidoso.
- Contra páginas de golpe **novas** (criadas hoje), nenhuma lista fixa basta — por isso ativamos as **listas vivas da comunidade mundial**, atualizadas a cada hora. Nossa blocklist é a semente; as listas vivas são o muro.
- **Quem assina a transação é você.** Nenhum escudo impede um golpe se você digitar a frase-semente ou assinar um "swap" sem ler. As camadas abaixo bloqueiam a *isca*; a decisão final é sua.

---

## CAMADA 1 — DNS privado (protege TODOS os apps, não só o navegador)

### Android
1. Crie conta grátis em **nextdns.io** → anote o endereço que aparece em *Setup → Endpoints* (ex.: `abc123.dns.nextdns.io`).
2. No painel do NextDNS:
   - **Security**: ligue *Threat Intelligence Feeds*, *Crypto-Jacking Protection*, *DNS Rebinding Protection*, *Typosquatting Protection*, *Newly Registered Domains* (bloqueia domínios recém-criados — onde nascem 90% dos golpes de token).
   - **Privacy → Blocklists**: ative **StevenBlack**, **phishing.army**, **DandelionSprout Anti-Malware**, **HaGeZi Multi PRO**.
   - **Denylist**: cole o conteúdo do arquivo `escudo_enxame_celular.txt` (nossa semente).
3. No celular: **Configurações → Rede → DNS particular/privado** → digite seu endereço NextDNS.
4. Pronto: todo app que tentar falar com domínio de rastreio, malvertising ou phishing conhecido **morre na hora**, sem instalar nada.

### iPhone (passo a passo completo)

1. **Abra esta conversa no iPhone** e toque nos cartões dos arquivos para baixar a blocklist e este guia (ficam no app Arquivos).
2. No **Safari**, entre em **nextdns.io** → crie a conta grátis.
3. No painel do NextDNS, aba **Setup → Apple**: toque em **Download profile** (baixa um perfil de configuração).
4. Vá em **Ajustes → Perfil Descarregado** (aparece no topo) → **Instalar** → digite o código do iPhone. Pronto: o DNS do enxame já protege **todos os apps**.
5. De volta ao painel do NextDNS (pode ser pelo próprio Safari do iPhone):
   - **Security**: ligue *Threat Intelligence Feeds*, *Crypto-Jacking Protection*, *DNS Rebinding Protection*, *Typosquatting Protection* e **Newly Registered Domains** (derruba sites de golpe criados hoje).
   - **Privacy → Blocklists**: ative **StevenBlack**, **phishing.army**, **DandelionSprout Anti-Malware**, **HaGeZi Multi PRO**.
   - **Denylist**: abra `escudo_enxame_celular.txt` no app Arquivos, copie tudo e cole.
6. **Navegador**: instale o **Brave** (bloqueador nativo de anúncios/rastreadores no iPhone) e/ou o app **AdGuard** (bloqueia anúncios dentro do Safari).
7. **Tor no iPhone**: o Tor Browser oficial não existe para iOS — use o **Onion Browser** (recomendado pelo próprio Tor Project).
8. iPhone já bloqueia muita coisa: ative também **Ajustes → Safari → Ocultar endereço IP** e **Bloquear todos os cookies de terceiros** permanece ligado por padrão.

---

## CAMADA 2 — Navegador blindado

- **Firefox para Android** + extensão **uBlock Origin** (listas: EasyList, EasyPrivacy, Online Malicious URL Blocklist) — bloqueio visual de anúncio malicioso que injeta página falsa de swap.
- **Tor Browser para Android** — quando quiser IP oculto de verdade (mesma lógica do nosso navegador de PC).
- Nunca navegue em link de token/airdrop que chegou por DM, SMS ou "suporte". Digite o endereço oficial você mesmo.

---

## CAMADA 3 — Defesa dos tokens (a mais importante)

1. **Frase-semente (12/24 palavras) NUNCA entra em site nenhum.** Nenhum suporte, airdrop ou "verificação" legítima pede isso. Pediu = golpe, 100% das vezes.
2. **Antes de assinar qualquer transação**, leia o que a carteira mostra. "SetApprovalForAll" ou permissão ilimitada em site desconhecido = drainer. Recuse.
3. **Carteira quente × cofre**: deixe no celular só o valor de uso do dia. O patrimônio fica em carteira fria/cofre separado, sem conexão diária.
4. **Revogue permissões antigas** regularmente (ferramenta *revoke.cash*, acessada digitando o endereço — nunca por link recebido).
5. **SIM swap**: ative PIN/senha na operadora e remova o SMS como fator de recuperação das contas de cripto — use app autenticador.
6. Golpes ativos comuns: clone de Uniswap/PancakeSwap, "airdrop" que pede assinatura, "suporte da MetaMask" no privado, site com letra trocada (`uniѕwap` com letra cirílica). Confira o domínio letra por letra.

---

## CAMADA EXTRA — Blindando a parceria com a IA

- Páginas maliciosas podem conter **instruções escondidas para IA** (prompt injection). As Camadas 1 e 2 bloqueiam a maioria dessas páginas.
- Regra de ouro: **não cole em nossas conversas o conteúdo de sites desconhecidos** nem abra arquivo recebido de estranho "para a Kimi analisar" sem me avisar a origem. Eu sempre pergunto antes de executar instruções que venham de dentro de páginas ou arquivos.

---

## Checklist de 5 minutos

- [ ] NextDNS configurado no DNS privado do celular
- [ ] *Newly Registered Domains* ligado no NextDNS
- [ ] Nossa blocklist importada no Denylist
- [ ] Firefox + uBlock Origin instalados
- [ ] Frase-semente anotada em papel, fora do celular
- [ ] SMS removido como recuperação das contas de cripto

*Mexeu com um, mexeu com todo o sistema. — Enxame 369*
