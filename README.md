# Enxame Soberano — Suíte de Proteção Digital

**Navegação protegida, tudo em um — do PC ao iPhone. Código aberto, sem caixas-pretas, sem dependência de vigilância.**

Suíte open-source de proteção digital construída para pessoas comuns: esconde seu IP, bloqueia rastreadores e páginas de golpe que roubam criptomoedas/tokens, e instala proteção em nível de sistema no iPhone com **um toque**.

## Componentes

| Arquivo | O que é | Plataforma |
|---|---|---|
| `navegador_soberano.py` | Navegador completo com 9 camadas: roteamento Tor (SOCKS5), bloqueador de rastreadores com contador ao vivo, HTTPS forçado, anti-fingerprint, modo paranoia, certificados inválidos rejeitados, perfil sem rastros | PC (Windows/Linux/Mac) |
| `Escudo_do_Enxame_iPhone.mobileconfig` | Perfil nativo iOS de DNS cifrado (DoH) — bloqueia malware, phishing, anúncios e rastreadores em **todos os apps** com um toque, sem instalar nada | iPhone/iPad/Mac |
| `escudo_enxame_celular.txt` | Blocklist-semente (um domínio por linha) importável em NextDNS, AdGuard e Pi-hole | Qualquer |
| `protecao_celular_enxame.md` | Guia completo em português: 3 camadas de proteção + defesa contra golpes de token (drainers, swap falso, SIM swap) | Leitura |

## Instalação rápida

### PC — Navegador Soberano
```bash
pip install PyQt6 PyQt6-WebEngine PySocks
sudo apt install tor && sudo systemctl start tor   # Linux
python navegador_soberano.py
```

### iPhone — Escudo de um toque
1. Baixe `Escudo_do_Enxame_iPhone.mobileconfig`
2. Ajustes → **Perfil Descarregado** → **Instalar**
3. Pronto: proteção ativa em todos os apps

## Princípios

- **Sem ilusões**: cada camada documenta o que faz e o que não faz
- **Código aberto de verdade**: GPL-3.0 — ninguém pode aprisionar este projeto
- **Privacidade sem cadastro**: o perfil de DNS usa resolvers públicos, sem conta
- **Acessível**: feito para quem não é técnico — tocar, instalar, estar protegido

## Roadmap

- [ ] Módulo VPN WireGuard soberano (cifrar o dispositivo inteiro)
- [ ] Atualização automática da blocklist pela rede Tor
- [ ] Tradução da interface para espanhol e inglês
- [ ] Versão Android (DNS privado + guia)

---

# Sovereign Swarm — Digital Protection Suite

**All-in-one protected browsing — from PC to iPhone. Open source, no black boxes, no surveillance dependencies.**

An open-source protection suite built for everyday people: hides your IP, blocks trackers and crypto/token-stealing scam pages, and installs system-wide protection on iPhone with **a single tap**.

## Components

| File | What it is | Platform |
|---|---|---|
| `navegador_soberano.py` | Full browser with 9 layers: Tor routing (SOCKS5), live tracker blocker, forced HTTPS, anti-fingerprinting, paranoia mode, invalid certificate rejection, no-trace profile | PC (Windows/Linux/Mac) |
| `Escudo_do_Enxame_iPhone.mobileconfig` | Native iOS encrypted-DNS (DoH) profile — blocks malware, phishing, ads and trackers in **every app** with one tap, nothing to install | iPhone/iPad/Mac |
| `escudo_enxame_celular.txt` | Seed blocklist (one domain per line), importable into NextDNS, AdGuard and Pi-hole | Any |
| `protecao_celular_enxame.md` | Full guide (Portuguese): 3-layer protection + token-scam defense (drainers, fake swaps, SIM swap) | Reading |

## Quick start

**PC:** `pip install PyQt6 PyQt6-WebEngine PySocks` → install & start Tor → `python navegador_soberano.py`

**iPhone:** download the `.mobileconfig` → Settings → **Profile Downloaded** → **Install** → done.

## License

GPL-3.0 — free forever, for everyone. See `LICENSE`.

## Authors

**Abd-369 × Kimi** — built in the open, for the greatest number.
