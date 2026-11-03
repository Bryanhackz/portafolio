document.addEventListener("DOMContentLoaded", () => {
  // ==========================================
  // 1. GESTIÓN DE COOKIES Y GOOGLE ANALYTICS
  // ==========================================
  const cookieBanner = document.getElementById("cookie-banner");
  const acceptBtn = document.getElementById("accept-cookies");
  const rejectBtn = document.getElementById("reject-cookies");

  const GA_MEASUREMENT_ID = "G-XXXXXXXXXX";

  function loadGA() {
    if (
      window.location.hostname === "localhost" ||
      window.location.hostname === "127.0.0.1"
    )
      return;
    if (window.__gaLoaded) return;
    window.__gaLoaded = true;

    const script = document.createElement("script");
    script.async = true;
    script.src = `https://www.googletagmanager.com/gtag/js?id=${GA_MEASUREMENT_ID}`;
    document.head.appendChild(script);

    window.dataLayer = window.dataLayer || [];
    function gtag() {
      window.dataLayer.push(arguments);
    }
    gtag("js", new Date());
    gtag("config", GA_MEASUREMENT_ID);
  }

  const cookieConsent = localStorage.getItem("cookie-consent");

  if (cookieConsent === "accepted") {
    loadGA();
  } else if (cookieConsent === "rejected") {
    if (cookieBanner) cookieBanner.style.display = "none";
  } else {
    if (cookieBanner) cookieBanner.style.display = "flex";
  }

  if (acceptBtn) {
    acceptBtn.addEventListener("click", () => {
      localStorage.setItem("cookie-consent", "accepted");
      if (cookieBanner) cookieBanner.style.display = "none";
      loadGA();
    });
  }

  if (rejectBtn) {
    rejectBtn.addEventListener("click", () => {
      localStorage.setItem("cookie-consent", "rejected");
      if (cookieBanner) cookieBanner.style.display = "none";
    });
  }

  // ==========================================
  // 2. GESTIÓN DEL TEMA (Claro / Oscuro)
  // ==========================================
  const themeBtn = document.getElementById("theme-btn");
  const iconSun = document.getElementById("icon-sun");
  const iconMoon = document.getElementById("icon-moon");
  const htmlElement = document.documentElement;
  const prefersReducedMotion = window.matchMedia(
    "(prefers-reduced-motion: reduce)"
  ).matches;

  const savedTheme = localStorage.getItem("bzg-theme") || "dark";
  htmlElement.setAttribute("data-theme", savedTheme);
  updateThemeIcon(savedTheme);

  if (themeBtn) {
    themeBtn.addEventListener("click", () => {
      const currentTheme = htmlElement.getAttribute("data-theme");
      const newTheme = currentTheme === "dark" ? "light" : "dark";
      htmlElement.setAttribute("data-theme", newTheme);
      localStorage.setItem("bzg-theme", newTheme);
      updateThemeIcon(newTheme);
    });
  }

  function updateThemeIcon(theme) {
    if (theme === "light") {
      if (iconSun) iconSun.style.display = "block";
      if (iconMoon) iconMoon.style.display = "none";
    } else {
      if (iconSun) iconSun.style.display = "none";
      if (iconMoon) iconMoon.style.display = "block";
    }
  }

  // ==========================================
  // 3. GESTIÓN DE IDIOMAS (i18n)
  // ==========================================
  const langBtn = document.getElementById("lang-btn");
  const langMenu = document.getElementById("lang-menu");

  if (langBtn && langMenu) {
    langBtn.addEventListener("click", (e) => {
      e.stopPropagation();
      langMenu.classList.toggle("active");
    });

    document.addEventListener("click", (e) => {
      if (!langMenu.contains(e.target) && e.target !== langBtn) {
        langMenu.classList.remove("active");
      }
    });
  }

  const translations = {
    en: {
      nav_main: "MAIN SCREEN",
      nav_works: "MY WORKS",
      nav_vision: "VISION & REASON",
      nav_security: "WHAT I DO DIFFERENTLY?",
      nav_socials: "SOCIAL NETWORKS",
      nav_contact: "CONTACT",
      hero_p:
        "Web designer and developer. I build secure, fast, and results-oriented architectures.",
      works_h2: "MY WORKS",
      works_p: "Projects and design scenarios will be listed here once published.",
      works_empty:
        "[ SYSTEM EMPTY ]<br>I will link my GitHub repositories and case studies here soon.",
      vision_h2: "VISION & REASON",
      vision_p1:
        'I started <span class="neon-word">building</span> <span class="neon-word pink">tools</span> for businesses that couldn\'t afford a dev team. Over time I understood the problem wasn\'t <span class="neon-word">design</span> or <span class="neon-word pink">code</span>, but the lack of a clear and honest <span class="neon-word">structure</span>.',
      vision_p2:
        'That\'s why I work with my own code, without templates or unnecessary layers. I want every business owner to understand what is under their website and have real <span class="neon-word pink">control</span>.',
      security_h2: "WHAT I DO DIFFERENTLY?",
      security_p:
        'Most freelancers leave <span class="neon-word">security</span> for the end. I put it first, from the first line of <span class="neon-word pink">clean code</span>.',
      security_li1:
        'I validate everything on the server. I never trust what the browser sends (<span class="neon-word">real protection</span>).',
      security_li2:
        "I use strict headers (CSP, HSTS) to block common attacks like XSS.",
      security_li3: "I protect every form against CSRF.",
      security_li4:
        "I keep the architecture clean and without external dependencies that could become a risk.",
      socials_h2: "SOCIAL NETWORKS",
      socials_p: "Connect with me on the platforms where I publish my work.",
      contact_h2: "CONTACT",
      contact_p:
        "Ready to start? Write to me and I'll reply with a concrete proposal in less than 24 hours.",
      contact_btn: "SEND MESSAGE",
    },
    es: {
      nav_main: "MAIN SCREEN",
      nav_works: "MIS TRABAJOS",
      nav_vision: "VISIÓN Y RAZÓN",
      nav_security: "¿QUÉ HAGO DIFERENTE?",
      nav_socials: "REDES SOCIALES",
      nav_contact: "CONTACTO",
      hero_p:
        "Diseñador y desarrollador web. Construyo arquitecturas seguras, rápidas y orientadas a resultados.",
      works_h2: "MIS TRABAJOS",
      works_p:
        "Aquí se listarán los proyectos y escenarios de diseño una vez estén publicados.",
      works_empty:
        "[ SYSTEM EMPTY ]<br>Próximamente enlazaré mis repositorios de GitHub y casos de estudio aquí.",
      vision_h2: "VISIÓN Y RAZÓN",
      vision_p1:
        'Empecé <span class="neon-word">construyendo</span> <span class="neon-word pink">herramientas</span> para negocios que no podían permitirse un equipo de desarrollo. Con el tiempo entendí que el problema no era el <span class="neon-word">diseño</span> ni el <span class="neon-word pink">código</span>, sino la falta de una <span class="neon-word">estructura</span> clara y honesta.',
      vision_p2:
        'Por eso trabajo con código propio, sin plantillas ni capas innecesarias. Quiero que cada dueño de negocio entienda qué hay debajo de su sitio web y tenga el <span class="neon-word pink">control</span> real.',
      security_h2: "¿QUÉ HAGO DIFERENTE?",
      security_p:
        'La mayoría de los freelancers dejan la <span class="neon-word">seguridad</span> para el final. Yo la pongo primero, desde la primera línea de <span class="neon-word pink">código limpio</span>.',
      security_li1:
        'Valido todo en el servidor. Nunca confío en lo que envía el navegador (<span class="neon-word">protección</span> real).',
      security_li2:
        "Uso cabeceras estrictas (CSP, HSTS) para bloquear ataques comunes como XSS.",
      security_li3: "Protejo cada formulario contra CSRF.",
      security_li4:
        "Mantengo la arquitectura limpia y sin dependencias externas que puedan volverse un riesgo.",
      socials_h2: "REDES SOCIALES",
      socials_p:
        "Conecta conmigo en las plataformas donde publico mi trabajo.",
      contact_h2: "CONTACTO",
      contact_p:
        "¿Listo para empezar? Escríbeme y te respondo con una propuesta concreta en menos de 24 horas.",
      contact_btn: "ENVIAR MENSAJE",
    },
    it: {
      nav_main: "SCHERMATA PRINCIPALE",
      nav_works: "I MIEI LAVORI",
      nav_vision: "VISIONE E RAGIONE",
      nav_security: "COSA FACCIO DI DIVERSO?",
      nav_socials: "SOCIAL NETWORK",
      nav_contact: "CONTATTO",
      hero_p:
        "Web designer e sviluppatore. Costruisco architetture sicure, veloci e orientate ai risultati.",
      works_h2: "I MIEI LAVORI",
      works_p:
        "Progetti e scenari di design saranno elencati qui una volta pubblicati.",
      works_empty:
        "[ SISTEMA VUOTO ]<br>Collegherò qui i miei repository GitHub e i casi di studio a breve.",
      vision_h2: "VISIONE E RAGIONE",
      vision_p1:
        'Ho iniziato <span class="neon-word">costruendo</span> <span class="neon-word pink">strumenti</span> per aziende che non potevano permettersi un team di sviluppo. Col tempo ho capito che il problema non era il <span class="neon-word">design</span> o il <span class="neon-word pink">codice</span>, ma la mancanza di una <span class="neon-word">struttura</span> chiara e onesta.',
      vision_p2:
        'Ecco perché lavoro con il mio codice, senza modelli o livelli non necessari. Voglio che ogni imprenditore capisca cosa c\'è sotto il suo sito web e abbia il vero <span class="neon-word pink">controllo</span>.',
      security_h2: "COSA FACCIO DI DIVERSO?",
      security_p:
        'La maggior parte dei freelance lascia la <span class="neon-word">sicurezza</span> alla fine. Io la metto al primo posto, dalla prima riga di <span class="neon-word pink">codice pulito</span>.',
      security_li1:
        'Valido tutto sul server. Non mi fido mai di ciò che invia il browser (<span class="neon-word">vera protezione</span>).',
      security_li2:
        "Uso intestazioni rigorose (CSP, HSTS) per bloccare attacchi comuni come XSS.",
      security_li3: "Proteggo ogni modulo contro CSRF.",
      security_li4:
        "Mantengo l'architettura pulita e senza dipendenze esterne che potrebbero diventare un rischio.",
      socials_h2: "SOCIAL NETWORK",
      socials_p:
        "Connettiti con me sulle piattaforme dove pubblico il mio lavoro.",
      contact_h2: "CONTATTO",
      contact_p:
        "Pronto per iniziare? Scrivimi e ti risponderò con una proposta concreta in meno di 24 ore.",
      contact_btn: "INVIA MESSAGGIO",
    },
    pt: {
      nav_main: "TELA PRINCIPAL",
      nav_works: "MEUS TRABALHOS",
      nav_vision: "VISÃO E RAZÃO",
      nav_security: "O QUE FAÇO DIFERENTE?",
      nav_socials: "REDES SOCIAIS",
      nav_contact: "CONTATO",
      hero_p:
        "Designer e desenvolvedor web. Construo arquiteturas seguras, rápidas e orientadas a resultados.",
      works_h2: "MEUS TRABALHOS",
      works_p:
        "Projetos e cenários de design serão listados aqui quando publicados.",
      works_empty:
        "[ SISTEMA VAZIO ]<br>Em breve, vincularei meus repositórios do GitHub e estudos de caso aqui.",
      vision_h2: "VISÃO E RAZÃO",
      vision_p1:
        'Comecei <span class="neon-word">construindo</span> <span class="neon-word pink">ferramentas</span> para negócios que não podiam pagar uma equipe de desenvolvimento. Com o tempo entendi que o problema não era o <span class="neon-word">design</span> ou o <span class="neon-word pink">código</span>, mas a falta de uma <span class="neon-word">estrutura</span> clara e honesta.',
      vision_p2:
        'É por isso que trabalho com código próprio, sem modelos ou camadas desnecessárias. Quero que cada dono de negócio entenda o que está por trás do seu site e tenha o <span class="neon-word pink">controle</span> real.',
      security_h2: "O QUE FAÇO DIFERENTE?",
      security_p:
        'A maioria dos freelancers deixa a <span class="neon-word">segurança</span> para o final. Eu coloco em primeiro lugar, desde a primeira linha de <span class="neon-word pink">código limpo</span>.',
      security_li1:
        'Eu valido tudo no servidor. Nunca confio no que o navegador envia (<span class="neon-word">proteção real</span>).',
      security_li2:
        "Uso cabeçalhos estritos (CSP, HSTS) para bloquear ataques comuns como XSS.",
      security_li3: "Protejo cada formulário contra CSRF.",
      security_li4:
        "Mantenho a arquitetura limpa e sem dependências externas que possam se tornar um risco.",
      socials_h2: "REDES SOCIAIS",
      socials_p:
        "Conecte-se comigo nas plataformas onde publico meu trabalho.",
      contact_h2: "CONTATO",
      contact_p:
        "Pronto para começar? Escreva para mim e responderei com uma proposta concreta em menos de 24 horas.",
      contact_btn: "ENVIAR MENSAGEM",
    },
    fr: {
      nav_main: "ÉCRAN PRINCIPAL",
      nav_works: "MES TRAVAUX",
      nav_vision: "VISION & RAISON",
      nav_security: "QUE FAIS-JE DIFFÉREMMENT ?",
      nav_socials: "RÉSEAUX SOCIAUX",
      nav_contact: "CONTACT",
      hero_p:
        "Web designer et développeur. Je construis des architectures sécurisées, rapides et orientées vers les résultats.",
      works_h2: "MES TRAVAUX",
      works_p:
        "Les projets et scénarios de conception seront listés ici une fois publiés.",
      works_empty:
        "[ SYSTÈME VIDE ]<br>Je lierai bientôt mes dépôts GitHub et mes études de cas ici.",
      vision_h2: "VISION & RAISON",
      vision_p1:
        'J\'ai commencé à <span class="neon-word">construire</span> des <span class="neon-word pink">outils</span> pour les entreprises qui ne pouvaient pas se permettre une équipe de développement. Avec le temps, j\'ai compris que le problème n\'était pas le <span class="neon-word">design</span> ou le <span class="neon-word pink">code</span>, mais le manque d\'une <span class="neon-word">structure</span> claire et honnête.',
      vision_p2:
        'C\'est pourquoi je travaille avec mon propre code, sans modèles ni couches inutiles. Je veux que chaque propriétaire d\'entreprise comprenne ce qu\'il y a sous son site web et ait le vrai <span class="neon-word pink">contrôle</span>.',
      security_h2: "QUE FAIS-JE DIFFÉREMMENT ?",
      security_p:
        'La plupart des freelances laissent la <span class="neon-word">sécurité</span> pour la fin. Je la mets en premier, dès la première ligne de <span class="neon-word pink">code propre</span>.',
      security_li1:
        'Je valide tout sur le serveur. Je ne fais jamais confiance à ce que le navigateur envoie (<span class="neon-word">vraie protection</span>).',
      security_li2:
        "J'utilise des en-têtes stricts (CSP, HSTS) pour bloquer les attaques courantes comme XSS.",
      security_li3: "Je protège chaque formulaire contre CSRF.",
      security_li4:
        "Je garde l'architecture propre et sans dépendances externes qui pourraient devenir un risque.",
      socials_h2: "RÉSEAUX SOCIAUX",
      socials_p:
        "Connectez-vous avec moi sur les plateformes où je publie mon travail.",
      contact_h2: "CONTACT",
      contact_p:
        "Prêt à commencer ? Écrivez-moi et je vous répondrai avec une proposition concrète en moins de 24 heures.",
      contact_btn: "ENVOYER LE MESSAGE",
    },
    zh: {
      nav_main: "主屏幕",
      nav_works: "我的作品",
      nav_vision: "愿景与理由",
      nav_security: "我有什么不同？",
      nav_socials: "社交网络",
      nav_contact: "联系方式",
      hero_p: "网页设计师和开发者。我构建安全、快速且以结果为导向的架构。",
      works_h2: "我的作品",
      works_p: "项目与设计场景将在发布后在此列出。",
      works_empty:
        "[ 系统为空 ]<br>我很快会将我的 GitHub 仓库和案例研究链接到这里。",
      vision_h2: "愿景与理由",
      vision_p1:
        '我开始为无法负担开发团队的企业<span class="neon-word">构建</span><span class="neon-word pink">工具</span>。随着时间的推移，我明白问题不在于<span class="neon-word">设计</span>或<span class="neon-word pink">代码</span>，而在于缺乏清晰诚实的<span class="neon-word">结构</span>。',
      vision_p2:
        '这就是为什么我用原创代码工作，没有模板或不必要的层。我希望每个企业主都能了解他们网站底层是什么，并拥有真正的<span class="neon-word pink">控制权</span>。',
      security_h2: "我有什么不同？",
      security_p:
        '大多数自由职业者将<span class="neon-word">安全</span>留到最后。我从第一行<span class="neon-word pink">干净代码</span>起就将其置于首位。',
      security_li1:
        '我在服务端验证一切。我从不信任浏览器发送的内容（<span class="neon-word">真正的保护</span>）。',
      security_li2:
        "我使用严格的标头 (CSP, HSTS) 来阻止如 XSS 等常见攻击。",
      security_li3: "我保护每个表单免受 CSRF 攻击。",
      security_li4:
        "我保持架构整洁，不依赖可能成为风险的外部依赖项。",
      socials_h2: "社交网络",
      socials_p: "在我发布作品的平台上与我联系。",
      contact_h2: "联系方式",
      contact_p:
        "准备好开始了吗？写信给我，我会在 24 小时内回复具体的提案。",
      contact_btn: "发送消息",
    },
    ja: {
      nav_main: "メイン画面",
      nav_works: "私の作品",
      nav_vision: "ビジョンと理由",
      nav_security: "私の違いは何ですか？",
      nav_socials: "ソーシャルネットワーク",
      nav_contact: "連絡先",
      hero_p:
        "ウェブデザイナー兼開発者。安全で高速、結果重視のアーキテクチャを構築します。",
      works_h2: "私の作品",
      works_p:
        "プロジェクトとデザインシナリオは公開され次第ここに掲載されます。",
      works_empty:
        "[ システムは空です ]<br>GitHubリポジトリとケーススタディをここにリンクする予定です。",
      vision_h2: "ビジョンと理由",
      vision_p1:
        '開発チームを雇う余裕のない企業のために<span class="neon-word">ツールを構築</span>することから始めました。時間が経つにつれ、問題は<span class="neon-word">デザイン</span>や<span class="neon-word pink">コード</span>ではなく、明確で正直な<span class="neon-word">構造</span>の欠如にあると理解しました。',
      vision_p2:
        'だからこそ、テンプレートや不要なレイヤーを使わず、独自のコードで作業しています。すべての事業主がウェブサイトの下にあるものを理解し、本当の<span class="neon-word pink">コントロール</span>を持てるようにしたいと考えています。',
      security_h2: "私の違いは何ですか？",
      security_p:
        'ほとんどのフリーランサーは<span class="neon-word">セキュリティ</span>を最後に回します。私は最初の<span class="neon-word pink">クリーンなコード</span>からそれを優先します。',
      security_li1:
        'すべてをサーバー側で検証します。ブラウザが送信するものを決して信頼しません（<span class="neon-word">真の保護</span>）。',
      security_li2:
        "XSSなどの一般的な攻撃をブロックするために、厳格なヘッダー（CSP、HSTS）を使用します。",
      security_li3: "すべてのフォームをCSRFから保護します。",
      security_li4:
        "リスクとなる可能性のある外部依存関係のないクリーンなアーキテクチャを維持します。",
      socials_h2: "ソーシャルネットワーク",
      socials_p: "作品を公開しているプラットフォームで私とつながりましょう。",
      contact_h2: "連絡先",
      contact_p:
        "始める準備はできましたか？メッセージを送っていただければ、24時間以内に具体的な提案をお返しします。",
      contact_btn: "メッセージを送信",
    },
    ko: {
      nav_main: "메인 화면",
      nav_works: "내 작품",
      nav_vision: "비전과 이유",
      nav_security: "내가 다르게 하는 것?",
      nav_socials: "소셜 네트워크",
      nav_contact: "연락처",
      hero_p:
        "웹 디자이너 및 개발자. 안전하고 빠르며 결과 지향적인 아키텍처를 구축합니다.",
      works_h2: "내 작품",
      works_p: "프로젝트 및 디자인 시나리오는 게시되면 여기에 나열됩니다.",
      works_empty:
        "[ 시스템 비어 있음 ]<br>곧 GitHub 리포지토리와 사례 연구를 여기에 연결하겠습니다.",
      vision_h2: "비전과 이유",
      vision_p1:
        '개발 팀을 고용할 여유가 없는 기업을 위해 <span class="neon-word">도구를 구축</span>하는 것으로 시작했습니다. 시간이 지나면서 문제는 <span class="neon-word">디자인</span>이나 <span class="neon-word pink">코드</span>가 아니라 명확하고 정직한 <span class="neon-word">구조</span>의 부족이라는 것을 깨달았습니다.',
      vision_p2:
        '그래서 템플릿이나 불필요한 계층 없이 자체 코드로 작업합니다. 모든 비즈니스 소유자가 웹사이트 아래에 무엇이 있는지 이해하고 진정한 <span class="neon-word pink">통제권</span>을 갖기를 바랍니다.',
      security_h2: "내가 다르게 하는 것?",
      security_p:
        '대부분의 프리랜서는 <span class="neon-word">보안</span>을 마지막에 둡니다. 저는 첫 번째 <span class="neon-word pink">깨끗한 코드</span>부터 보안을 최우선으로 합니다.',
      security_li1:
        '서버에서 모든 것을 검증합니다. 브라우저가 보내는 것을 절대 신뢰하지 않습니다 (<span class="neon-word">진정한 보호</span>).',
      security_li2:
        "XSS와 같은 일반적인 공격을 차단하기 위해 엄격한 헤더(CSP, HSTS)를 사용합니다.",
      security_li3: "모든 양식을 CSRF로부터 보호합니다.",
      security_li4:
        "위험이 될 수 있는 외부 종속성 없이 깨끗한 아키텍처를 유지합니다.",
      socials_h2: "소셜 네트워크",
      socials_p: "내 작업을 게시하는 플랫폼에서 나와 연결하세요.",
      contact_h2: "연락처",
      contact_p:
        "시작할 준비가 되셨나요? 메시지를 보내주시면 24시간 이내에 구체적인 제안으로 답변해 드리겠습니다.",
      contact_btn: "메시지 보내기",
    },
  };

  function changeLanguage(langCode) {
    const dict = translations[langCode] || translations.en;
    if (!dict) return;

    document.querySelectorAll("[data-i18n]").forEach((el) => {
      const key = el.getAttribute("data-i18n");
      if (dict[key]) el.textContent = dict[key];
    });

    document.querySelectorAll("[data-i18n-html]").forEach((el) => {
      const key = el.getAttribute("data-i18n-html");
      if (dict[key]) el.innerHTML = dict[key];
    });

    localStorage.setItem("bzg-lang", langCode);
    if (langMenu) langMenu.classList.remove("active");
  }

  if (langMenu) {
    document.querySelectorAll("#lang-menu button").forEach((btn) => {
      btn.addEventListener("click", () => {
        changeLanguage(btn.getAttribute("data-lang"));
      });
    });
  }

  const detectedLang =
    document.documentElement.getAttribute("data-detected-lang") || "en";
  const savedLang = localStorage.getItem("bzg-lang") || detectedLang;
  changeLanguage(savedLang);

  // ==========================================
  // 4. TYPEWRITER & SCROLL SPY
  // ==========================================
  const textElement = document.getElementById("typewriter-text");
  if (textElement) {
    if (prefersReducedMotion) {
      textElement.textContent = "< WEB_DEVELOPER />";
    } else {
      const phrases = [
        "&lt; WEB_DEVELOPER /&gt;",
        "&lt; SYSTEM ARCHITECT /&gt;",
        "&lt; SECURITY ENTHUSIAST /&gt;",
      ];
      let phraseIndex = 0,
        charIndex = 0,
        isDeleting = false;

      function type() {
        const currentPhrase = phrases[phraseIndex];
        if (isDeleting) {
          textElement.innerHTML = currentPhrase.substring(0, charIndex - 1);
          charIndex--;
        } else {
          textElement.innerHTML = currentPhrase.substring(0, charIndex + 1);
          charIndex++;
        }
        let typeSpeed = isDeleting ? 50 : 100;
        if (!isDeleting && charIndex === currentPhrase.length) {
          typeSpeed = 2000;
          isDeleting = true;
        } else if (isDeleting && charIndex === 0) {
          isDeleting = false;
          phraseIndex = (phraseIndex + 1) % phrases.length;
          typeSpeed = 500;
        }
        setTimeout(type, typeSpeed);
      }
      setTimeout(type, 1000);
    }
  }

  const sections = document.querySelectorAll(".content-section");
  const navNodes = document.querySelectorAll(".node[data-target]");
  const scrollContainer = document.getElementById("scroll-container");

  if (scrollContainer && sections.length > 0) {
    scrollContainer.addEventListener("scroll", () => {
      let current = "";
      sections.forEach((section) => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.clientHeight;
        if (scrollContainer.scrollTop >= sectionTop - sectionHeight / 3) {
          current = section.getAttribute("id");
        }
      });

      navNodes.forEach((node) => {
        node.classList.remove("active");
        if (node.getAttribute("data-target") === current) {
          node.classList.add("active");
        }
      });
    });

    navNodes.forEach((node) => {
      node.addEventListener("click", function (e) {
        e.preventDefault();
        const targetId = this.getAttribute("href");
        const targetSection = document.querySelector(targetId);
        if (targetSection) {
          scrollContainer.scrollTo({
            top: targetSection.offsetTop,
            behavior: "smooth",
          });
        }
      });
    });
  }
});