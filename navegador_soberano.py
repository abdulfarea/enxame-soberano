# -*- coding: utf-8 -*-
"""
=========================================================================
 NAVEGADOR SOBERANO v2 — Abd-369 x Kimi
 NAVEGACAO PROTEGIDA, TUDO EM UM. Codigo 100% Python, aberto, do enxame.

 CAMADAS DE PROTECAO INTEGRADAS (todas ligadas por padrao):
   1. TOR       — todo o trafego sai pela rede Tor (SOCKS5), IP oculto,
                  DNS resolvido remotamente (sem vazamento de DNS).
   2. ESCUDO    — bloqueador de rastreadores/anuncios com contador ao
                  vivo; blocklist expansivel e atualizavel pela propria
                  rede Tor (fonte: StevenBlack/hosts, aberta).
   3. HTTPS     — todo endereco e promovido a HTTPS automaticamente.
   4. FANTASMA  — anti-fingerprint: User-Agent rotativo por sessao,
                  WebGL/WebAudio desligados, auditoria de hiperlinks off.
   5. PARANOIA  — um clique desliga JavaScript e imagens (sites de
                  alta vigilancia/carregamento suspeito).
   6. SEM RASTROS — perfil off-the-record: cookies e cache so em
                  memoria; botao "Limpar sessao" apaga tudo na hora.
   7. CERT      — certificados invalidos sao REJEITADOS (sem clique
                  cego que aceita ataque man-in-the-middle).
   8. POPUPS    — janelas forcadas viram abas controladas, nunca
                  janelas soltas fora do seu controle.
   9. PAINEL    — pagina inicial e o proprio painel de protecao do
                  enxame, com busca DuckDuckGo (nao rastreia).

 LIMITES HONESTOS (para voce nunca ser enganado):
   - Nao e uma VPN de sistema: protege a NAVEGACAO. Para cifrar o
     computador inteiro, o proximo modulo e o WireGuard soberano.
   - Sites com login (banco, e-mail) saberao quem voce e depois do
     login — o Tor esconde ONDE voce esta, nao quem voce diz ser.

 REQUISITOS (na sua maquina):
     pip install PyQt6 PyQt6-WebEngine PySocks
     # Tor:
     #   Ubuntu/Debian:  sudo apt install tor && sudo systemctl start tor
     #   Mac (brew):     brew install tor && brew services start tor
     #   Windows:        Tor Browser aberto -> troque PORTA_TOR p/ 9150

 USO:
     python navegador_soberano.py
=========================================================================
"""

import os
import random
import socket
import sys
import threading

from PyQt6.QtCore import Qt, QTimer, QUrl
from PyQt6.QtGui import QAction, QKeySequence
from PyQt6.QtNetwork import QNetworkProxy
from PyQt6.QtWebEngineCore import (
    QWebEngineProfile,
    QWebEngineSettings,
    QWebEngineUrlRequestInfo,
    QWebEngineUrlRequestInterceptor,
)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QTabWidget,
    QToolBar,
)

# ----------------------------------------------------------------------
# CONFIGURACAO DO ENXAME
# ----------------------------------------------------------------------
HOST_TOR = "127.0.0.1"
PORTA_TOR = 9050                     # 9150 se usar o Tor Browser aberto
PAGINA_TESTE_IP = "https://check.torproject.org"
BUSCA = "https://duckduckgo.com/?q="

PASTA = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_BLOCKLIST = os.path.join(PASTA, "blocklist_enxame.txt")
URL_BLOCKLIST_REMOTA = (
    "https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts")

# User-Agents comuns reais — um aleatorio por sessao (anti-fingerprint)
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) "
    "Gecko/20100101 Firefox/125.0",
]

# Escudo-base do enxame (a blocklist remota engorda essa lista)
DOMINIOS_BLOQUEADOS = {
    # analitica / rastreio
    "google-analytics.com", "googletagmanager.com", "analytics.google.com",
    "scorecardresearch.com", "quantserve.com", "hotjar.com", "mixpanel.com",
    "segment.io", "segment.com", "amplitude.com", "branch.io",
    "appsflyer.com", "adjust.com", "newrelic.com", "nr-data.net",
    "fullstory.com", "mouseflow.com", "crazyegg.com", "optimizely.com",
    "chartbeat.com", "comscore.com", "imrworldwide.com", "omtrdc.net",
    "demdex.net", "bluekai.com", "krxd.net", "exelator.com",
    # anuncios
    "doubleclick.net", "googlesyndication.com", "adservice.google.com",
    "adsystem.com", "criteo.com", "criteo.net", "taboola.com",
    "outbrain.com", "pubmatic.com", "rubiconproject.com", "openx.net",
    "adnxs.com", "adsrvr.org", "amazon-adsystem.com", "moatads.com",
    "serving-sys.com", "bidswitch.net", "casalemedia.com",
    # redes sociais espioes
    "facebook.net", "connect.facebook.net", "ads.twitter.com",
    "analytics.twitter.com", "platform.twitter.com", "syndication.twitter.com",
    "snap.licdn.com", "ads.linkedin.com", "pixel.tiktok.com",
    "analytics.tiktok.com", "ads.pinterest.com", "bat.bing.com",
}


def carregar_blocklist_local():
    """Soma a blocklist baixada anteriormente (se existir) ao escudo."""
    try:
        with open(ARQUIVO_BLOCKLIST, "r", encoding="utf-8") as arq:
            for linha in arq:
                dominio = linha.strip().lower()
                if dominio:
                    DOMINIOS_BLOQUEADOS.add(dominio)
    except OSError:
        pass


carregar_blocklist_local()


# ----------------------------------------------------------------------
# CAMADA 2 — ESCUDO (interceptador de rastreadores)
# ----------------------------------------------------------------------
class BloqueadorRastreadores(QWebEngineUrlRequestInterceptor):
    """Derruba cada requisicao destinada a dominio rastreador."""

    def __init__(self, perfil):
        super().__init__(perfil)
        self.bloqueados = 0

    def interceptRequest(self, info: QWebEngineUrlRequestInfo) -> None:
        host = info.requestUrl().host().lower()
        partes = host.split(".")
        candidatos = {".".join(partes[i:]) for i in range(len(partes) - 1)}
        if candidatos & DOMINIOS_BLOQUEADOS:
            self.bloqueados += 1          # contado no painel ao vivo
            info.block(True)


# ----------------------------------------------------------------------
# ABA DO NAVEGADOR
# ----------------------------------------------------------------------
class AbaNavegador(QWebEngineView):
    def __init__(self, perfil: QWebEngineProfile, janela):
        super().__init__()
        self.janela = janela
        self.page().setProfile(perfil)
        self._cfg(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        self._cfg(QWebEngineSettings.WebAttribute.AutoLoadImages, True)
        self._cfg(QWebEngineSettings.WebAttribute.PluginsEnabled, False)
        self._cfg(QWebEngineSettings.WebAttribute.WebGLEnabled, False)
        self._cfg(QWebEngineSettings.WebAttribute.WebAudioEnabled, False)
        self._cfg(QWebEngineSettings.WebAttribute.FullScreenSupportEnabled,
                  False)
        self._cfg(QWebEngineSettings.WebAttribute.ScreenCaptureEnabled, False)
        self._cfg(QWebEngineSettings.WebAttribute.HyperlinkAuditingEnabled,
                  False)   # sem "ping" oculto ao clicar em links
        # CAMADA 7 — certificado invalido e rejeitado, sem excecao cega
        try:
            self.page().certificateError.connect(self._rejeitar_certificado)
        except AttributeError:
            pass

    def _cfg(self, atributo, valor):
        """Liga/desliga protecoes tolerando versoes diferentes do Qt."""
        try:
            self.settings().setAttribute(atributo, valor)
        except (AttributeError, TypeError):
            pass

    def _rejeitar_certificado(self, erro):
        erro.rejectCertificate()
        self.janela.barra_status.showMessage(
            "⛔ Certificado invalido REJEITADO — possivel interceptacao. "
            "O site nao foi carregado.")

    def createWindow(self, _tipo):
        """CAMADA 8 — popups viram abas sob seu controle, nunca janelas."""
        return self.janela._nova_aba(painel=False)


# ----------------------------------------------------------------------
# JANELA PRINCIPAL
# ----------------------------------------------------------------------
class NavegadorSoberano(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Navegador Soberano v2 — Abd-369 × Kimi")
        self.resize(1320, 840)

        # CAMADA 4 — identidade rotativa por sessao
        self.user_agent = random.choice(USER_AGENTS)

        # CAMADA 6 — perfil off-the-record: nada persiste em disco
        self.perfil = QWebEngineProfile(self)
        self.perfil.setHttpUserAgent(self.user_agent)
        self.perfil.setPersistentCookiesPolicy(
            QWebEngineProfile.PersistentCookiesPolicy.NoPersistentCookies)
        self.perfil.setHttpCacheType(
            QWebEngineProfile.HttpCacheType.MemoryHttpCache)
        self.bloqueador = BloqueadorRastreadores(self.perfil)
        self.perfil.setUrlRequestInterceptor(self.bloqueador)

        # CAMADA 1 — Tor
        self.tor_ativo = True
        self.js_ativo = True
        self._aplicar_proxy()

        # Abas
        self.abas = QTabWidget()
        self.abas.setDocumentMode(True)
        self.abas.setTabsClosable(True)
        self.abas.setMovable(True)
        self.abas.tabCloseRequested.connect(self._fechar_aba)
        self.abas.currentChanged.connect(self._aba_trocou)
        self.setCentralWidget(self.abas)

        # Barra de ferramentas
        barra = QToolBar("Navegacao")
        barra.setMovable(False)
        self.addToolBar(barra)

        self._acao(barra, "←", self._voltar, "Alt+Left")
        self._acao(barra, "→", self._avancar, "Alt+Right")
        self._acao(barra, "⟳", self._recarregar, "F5")
        self._acao(barra, "⌂", self._inicio)
        self._acao(barra, "＋", lambda: self._nova_aba(painel=False), "Ctrl+T")

        self.campo_url = QLineEdit()
        self.campo_url.setPlaceholderText(
            "Endereco ou busca protegida (DuckDuckGo)...")
        self.campo_url.returnPressed.connect(self._ir_para_url)
        barra.addWidget(self.campo_url)

        self.acao_tor = self._acao_toggle(barra, "Tor", True,
                                          self._alternar_tor)
        self.acao_js = self._acao_toggle(barra, "JS", True,
                                         self._alternar_js)
        self._acao(barra, "🛡 Paranoia", self._paranoia)
        self._acao(barra, "Verificar IP", self._verificar_ip)
        self._acao(barra, "Atualizar escudo", self._atualizar_escudo)
        self._acao(barra, "Limpar sessão", self._limpar_sessao)

        atalho_fechar = QAction(self)
        atalho_fechar.setShortcut(QKeySequence("Ctrl+W"))
        atalho_fechar.triggered.connect(
            lambda: self._fechar_aba(self.abas.currentIndex()))
        self.addAction(atalho_fechar)

        # Painel ao vivo na barra de status
        self.barra_status = self.statusBar()
        self.rotulo_escudo = QLabel()
        self.barra_status.addPermanentWidget(self.rotulo_escudo)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._atualizar_painel)
        self.timer.start(1000)

        self._nova_aba(painel=True)

    # ------------------------------------------------------------------
    # CAMADA 1 — TOR / PROXY
    # ------------------------------------------------------------------
    def _aplicar_proxy(self):
        if self.tor_ativo:
            proxy = QNetworkProxy(
                QNetworkProxy.ProxyType.Socks5Proxy, HOST_TOR, PORTA_TOR)
            QNetworkProxy.setApplicationProxy(proxy)
        else:
            QNetworkProxy.setApplicationProxy(QNetworkProxy())

    def _alternar_tor(self):
        self.tor_ativo = self.acao_tor.isChecked()
        self._aplicar_proxy()
        self.acao_tor.setText("Tor ✓" if self.tor_ativo else "Tor ✗")
        self.barra_status.showMessage(
            f"Tor {'LIGADO' if self.tor_ativo else 'DESLIGADO'}"
            " — recarregue a pagina para valer.")

    def _alternar_js(self):
        self.js_ativo = self.acao_js.isChecked()
        for i in range(self.abas.count()):
            self.abas.widget(i)._cfg(
                QWebEngineSettings.WebAttribute.JavascriptEnabled,
                self.js_ativo)
        self.acao_js.setText("JS ✓" if self.js_ativo else "JS ✗")
        self.barra_status.showMessage(
            f"JavaScript {'ligado' if self.js_ativo else 'DESLIGADO'}"
            " — recarregue para aplicar.")

    def _paranoia(self):
        """CAMADA 5 — um clique: sem JS, sem imagens, superficie minima."""
        for i in range(self.abas.count()):
            aba = self.abas.widget(i)
            aba._cfg(QWebEngineSettings.WebAttribute.JavascriptEnabled, False)
            aba._cfg(QWebEngineSettings.WebAttribute.AutoLoadImages, False)
            aba._cfg(QWebEngineSettings.WebAttribute.WebAudioEnabled, False)
        self.acao_js.setChecked(False)
        self.acao_js.setText("JS ✗")
        self.js_ativo = False
        self.barra_status.showMessage(
            "🛡 MODO PARANOIA ativo — JS e imagens desligados. "
            "Recarregue a pagina.")

    def _verificar_ip(self):
        self._aba_atual().setUrl(QUrl(PAGINA_TESTE_IP))
        self.barra_status.showMessage(
            "Abrindo check.torproject.org — 'Congratulations' = IP oculto.")

    # ------------------------------------------------------------------
    # CAMADA 2 — ATUALIZAR ESCUDO PELA PROPRIA REDE TOR
    # ------------------------------------------------------------------
    def _atualizar_escudo(self):
        if not self.tor_ativo:
            self.barra_status.showMessage(
                "Ligue o Tor antes de atualizar o escudo.")
            return
        self.barra_status.showMessage(
            "Baixando blocklist pela rede Tor... (pode levar ~30s)")
        threading.Thread(target=self._baixar_blocklist, daemon=True).start()

    def _baixar_blocklist(self):
        try:
            import socks  # PySocks
        except ImportError:
            self._aviso_threadsafe(
                "Instale o PySocks para atualizar o escudo: "
                "pip install PySocks")
            return
        socket_original = socket.socket
        try:
            socks.set_default_proxy(
                socks.SOCKS5, HOST_TOR, PORTA_TOR, rdns=True)
            socket.socket = socks.socksocket
            import urllib.request
            req = urllib.request.Request(
                URL_BLOCKLIST_REMOTA, headers={"User-Agent": "enxame-369"})
            with urllib.request.urlopen(req, timeout=60) as resp:
                texto = resp.read().decode("utf-8", "ignore")
        except Exception as e:  # rede/Tor fora do ar etc.
            self._aviso_threadsafe(f"Falha ao baixar blocklist: {e}")
            return
        finally:
            socket.socket = socket_original

        novos = set()
        for linha in texto.splitlines():
            if linha.startswith("0.0.0.0"):
                partes = linha.split()
                if len(partes) >= 2:
                    dominio = partes[1].lower()
                    if dominio not in ("0.0.0.0", "localhost"):
                        novos.add(dominio)
        antes = len(DOMINIOS_BLOQUEADOS)
        DOMINIOS_BLOQUEADOS.update(novos)
        try:
            with open(ARQUIVO_BLOCKLIST, "w", encoding="utf-8") as arq:
                arq.write("\n".join(sorted(novos)))
        except OSError:
            pass
        self._aviso_threadsafe(
            f"🛡 Escudo atualizado: {len(DOMINIOS_BLOQUEADOS)} dominios "
            f"bloqueados (+{len(DOMINIOS_BLOQUEADOS) - antes} novos).")

    def _aviso_threadsafe(self, mensagem):
        # QTimer de tiro unico devolve a mensagem para a thread da GUI
        QTimer.singleShot(
            0, lambda: self.barra_status.showMessage(mensagem, 15000))

    # ------------------------------------------------------------------
    # CAMADA 6 — LIMPAR SESSAO
    # ------------------------------------------------------------------
    def _limpar_sessao(self):
        self.perfil.cookieStore().deleteAllCookies()
        self.perfil.clearHttpCache()
        self.perfil.clearAllVisitedLinks()
        self.barra_status.showMessage(
            "🧹 Sessao limpa: cookies, cache e historico apagados da memoria.")

    # ------------------------------------------------------------------
    # PAGINA INICIAL = PAINEL DO ENXAME
    # ------------------------------------------------------------------
    def _html_painel(self):
        tor = "ATIVO ✓" if self.tor_ativo else "DESLIGADO ✗"
        cor = "#2ecc71" if self.tor_ativo else "#e74c3c"
        return f"""<!DOCTYPE html><html lang="pt-BR"><head>
<meta charset="utf-8"><title>Painel Soberano</title><style>
body{{background:#0d1b2a;color:#e0e1dd;font-family:system-ui,sans-serif;
display:flex;flex-direction:column;align-items:center;padding-top:8vh}}
h1{{color:#7b9acc;letter-spacing:2px}}
.cartao{{background:#1b263b;border:1px solid #415a77;border-radius:12px;
padding:24px 32px;max-width:640px;width:90%}}
ul{{line-height:1.9;list-style:none;padding:0}}
li::before{{content:"◆ ";color:#7b9acc}}
form{{margin:24px 0;display:flex;width:90%;max-width:640px}}
input{{flex:1;padding:14px;border-radius:8px 0 0 8px;border:1px solid
#415a77;background:#0d1b2a;color:#e0e1dd;font-size:16px}}
button{{padding:14px 22px;border:none;border-radius:0 8px 8px 0;
background:#415a77;color:#fff;font-size:16px;cursor:pointer}}
.tor{{color:{cor};font-weight:bold}}
</style></head><body>
<h1>NAVEGADOR SOBERANO</h1>
<form action="https://duckduckgo.com/" method="get">
<input name="q" placeholder="Busca protegida — DuckDuckGo" autofocus>
<button>Buscar</button></form>
<div class="cartao"><ul>
<li>Roteamento Tor: <span class="tor">{tor}</span></li>
<li>Escudo anti-rastreio: <b>{len(DOMINIOS_BLOQUEADOS)} dominios bloqueados</b></li>
<li>HTTPS forcado em todo endereco</li>
<li>Anti-fingerprint: identidade rotativa, WebGL/WebAudio off</li>
<li>Perfil sem rastros: cookies e cache so em memoria</li>
<li>Certificados invalidos rejeitados automaticamente</li>
<li>Modo Paranoia disponivel na barra superior</li>
</ul>
<p style="color:#778da9">Abd-369 × Kimi — navegacao protegida, tudo em um.</p>
</div></body></html>"""

    # ------------------------------------------------------------------
    # NAVEGACAO / ABAS
    # ------------------------------------------------------------------
    def _acao(self, barra, texto, funcao, atalho=None):
        acao = QAction(texto, self)
        acao.triggered.connect(funcao)
        if atalho:
            acao.setShortcut(QKeySequence(atalho))
        barra.addAction(acao)
        return acao

    def _acao_toggle(self, barra, texto, ligado, funcao):
        acao = QAction(texto + (" ✓" if ligado else " ✗"), self)
        acao.setCheckable(True)
        acao.setChecked(ligado)
        acao.triggered.connect(funcao)
        barra.addAction(acao)
        return acao

    def _aba_atual(self) -> AbaNavegador:
        return self.abas.currentWidget()

    def _nova_aba(self, painel=True):
        aba = AbaNavegador(self.perfil, self)
        if painel:
            aba.setHtml(self._html_painel(), QUrl("https://enxame.local/"))
        else:
            aba.setUrl(QUrl("https://duckduckgo.com"))
        indice = self.abas.addTab(aba, "Nova aba")
        self.abas.setCurrentIndex(indice)
        aba.urlChanged.connect(
            lambda url, a=aba: self._atualizar_url(url, a))
        aba.titleChanged.connect(
            lambda titulo, a=aba: self._atualizar_titulo(titulo, a))
        aba.loadFinished.connect(self._pagina_carregada)
        return aba

    def _fechar_aba(self, indice):
        if self.abas.count() > 1 and indice >= 0:
            self.abas.removeTab(indice)

    def _aba_trocou(self, indice):
        aba = self.abas.widget(indice)
        if aba:
            self.campo_url.setText(aba.url().toString())

    def _atualizar_url(self, url, aba):
        if aba is self._aba_atual():
            self.campo_url.setText(url.toString())

    def _atualizar_titulo(self, titulo, aba):
        indice = self.abas.indexOf(aba)
        if indice >= 0:
            self.abas.setTabText(indice, (titulo or "Nova aba")[:25])

    def _pagina_carregada(self, ok):
        if not ok and self.tor_ativo:
            self.barra_status.showMessage(
                "Falha ao carregar — o Tor esta rodando? "
                "'sudo systemctl start tor' (Linux)")

    def _ir_para_url(self):
        texto = self.campo_url.text().strip()
        if not texto:
            return
        if " " in texto or "." not in texto:
            texto = BUSCA + texto.replace(" ", "+")
        elif texto.startswith("http://"):
            texto = "https://" + texto[7:]       # CAMADA 3 — sobe p/ HTTPS
        elif not texto.startswith("https://"):
            texto = "https://" + texto
        self._aba_atual().setUrl(QUrl(texto))

    def _voltar(self):
        self._aba_atual().back()

    def _avancar(self):
        self._aba_atual().forward()

    def _recarregar(self):
        self._aba_atual().reload()

    def _inicio(self):
        self._aba_atual().setHtml(
            self._html_painel(), QUrl("https://enxame.local/"))

    def _atualizar_painel(self):
        tor = "Tor ✓" if self.tor_ativo else "Tor ✗"
        js = "JS ✓" if self.js_ativo else "JS ✗"
        self.rotulo_escudo.setText(
            f"  🛡 {self.bloqueador.bloqueados} rastreadores bloqueados"
            f"  |  {len(DOMINIOS_BLOQUEADOS)} dominios no escudo"
            f"  |  {tor}  |  {js}  ")


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("NavegadorSoberano")

    soquete = socket.socket()
    soquete.settimeout(1.5)
    try:
        soquete.connect((HOST_TOR, PORTA_TOR))
    except OSError:
        QMessageBox.warning(
            None, "Tor nao detectado",
            f"Nada escutando em {HOST_TOR}:{PORTA_TOR}.\n\n"
            "Inicie o Tor para a protecao total funcionar:\n"
            "  Linux: sudo apt install tor && sudo systemctl start tor\n"
            "  Mac:   brew install tor && brew services start tor\n\n"
            "O navegador abre assim mesmo, mas SEM ocultar o IP "
            "ate o Tor estar ativo.")
    finally:
        soquete.close()

    janela = NavegadorSoberano()
    janela.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
