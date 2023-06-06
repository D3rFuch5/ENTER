class Header extends HTMLElement {
  constructor() {
    super();
  }

  connectedCallback() {
    this.innerHTML = `
            <header>
                <a id="home_ENTER" href="index.html">
                    <img id="logo_ENTER" src="pictures/Logo_Enter.png" alt="Logo der Software ENTER">
                    <span id="schriftzug_ENTER">ENTER</span>
                </a>
                <nav id="navigation_bar">
                    <a id="current_tab" class="level_one_tab" href="index.html">Start</a>
                    <div class="dropdown">
                        <a class="other_tab level_one_tab" href="Anleitungen.html">Anleitungen
                            <i class="fa fa-caret-down"></i>
                        </a>
                        <div class="dropdown-content">
                            <a class="other_tab" href="Anleitungen.html#ENTER_Voraussetzungen">Voraussetzungen</a>
                            <a class="other_tab" href="Anleitungen.html#ENTER_Start">Starten</a>
                            <a class="other_tab" href="Anleitungen.html#ENTER_Funktionen">Funktionen</a>
                        </div>
                    </div>
                    <a class="other_tab level_one_tab" href="Downloads.html">Downloads</a>
                    <div class="dropdown">
                        <a class="other_tab level_one_tab" href="Weiteres.html">Weiteres
                            <i class="fa fa-caret-down"></i>
                        </a>
                        <div class="dropdown-content">
                            <a class="other_tab" href="Weiteres.html#Abschnitt_Perzeptron_Simulator">Perzeptron-Simulator</a>
                            <a class="other_tab" href="Weiteres.html#Abschnitt_kNN">k-nächster-Nachbar-Algorithmus</a>
                        </div>
                    </div>
                </nav>
                <img id="logo_entwickler" src="pictures/logo_fuchs_wolf.png" alt="Logo der Entwickler">
            </header>
    `;
  }
}

customElements.define('header-component', Header);