# MITRE ATT&CK, Threat Intelligence och TLP - company-website

**Datum:** 2026-10-05
**Klassificering:** TLP:CLEAR (sanerad för publicering i projektets publika repo)
**Omfattning:** Team 2:s company-website-repo, dokumentation, mergehistorik,
tester och verifierad driftstatus från vecka 4-7.

## Syfte och avgränsning

Detta dokument sammanfattar verifierade applikationsrisker, deras aktuella
åtgärdsstatus och kvarvarande kontrollbehov. En MITRE ATT&CK-koppling beskriver
ett möjligt angriparbeteende; den betyder inte att ett intrång har skett.

Kurslabbets flaggor är separerade från Team 2:s applikation och driftmiljö. De
används som underlag för hotanalys och defensiva kontroller, inte som
incidentbevis.

## Så läser du dokumentet

Varje tabellrad svarar på fem enkla frågor:

1. **Vad hittades eller infördes?**
2. **Vilket underlag visar att det stämmer?**
3. **Vilket angriparbeteende hjälper MITRE ATT&CK oss att beskriva?**
4. **Är risken kvar, åtgärdad eller bara observerad i kurslabbet?**
5. **Hur kan informationen delas utan att exponera hemligheter?**

MITRE ATT&CK används här som ett gemensamt språk för analys. En koppling till en
teknik betyder inte att Team 2 har utsatts för ett verkligt angrepp.

## Lägesbild just nu

- **Verifierat klart:** Workshop 4-hardening, signerade container-images, SBOM
  och policy som nekar osignerade images. Profilflöde och runtime-hardening
  verifierades dessutom i drift 2026-10-06.
- **Historiska fynd:** SQL injection, IDOR, hårdkodad hemlighet, CSRF/cookies
  och Jinja-injektion är dokumenterade från äldre kod men åtgärdade i den
  aktuella versionen.
- **Nästa fokus:** Gör den verifierade Trivy/Discord-kontrollen reproducerbar
  och håll de äldre säkerhetsrapporterna tydligt märkta som historiska.

## Verifiering 2026-10-06 - profilflöde och runtime-hardening

Efter hardeningen i [PR #32](https://github.com/itsx25-team2/company-website/pull/32)
verifierades följande utan att använda eller publicera hemligheter:

| Kontroll | Resultat | Vad resultatet visar |
| --- | --- | --- |
| Driftstatus | `/healthz` svarade `200` med databasen ansluten och startsidan svarade `200`. | Den nya podden kan nå applikationen och SQLite-databasen. |
| Manuell profilkontroll | Ett tilldelat testkonto i utbildarens kursmiljö sparade ett ofarligt profilvärde, laddade om sidan och loggade sedan ut och in igen. Värdet låg kvar och återställdes därefter. | SQLite-volymen är skrivbar för den rootlösa applikationsprocessen och en vanlig användarsession fungerar efter hardeningen. |
| Gränssnitt | Profilformuläret visade endast vanliga profilfält, inte `role` eller `internal_notes`. `Internal Notes` visas skrivskyddat för ägaren i profilvyn, men skickas inte med när en annan användares profil visas. | Serverstyrda uppgifter exponeras inte som redigerbara fält. Teamet behöver besluta om anteckningar även fortsättningsvis ska vara synliga för profilägaren eller enbart för administratörer. |
| Riktade säkerhetstester | Fyra relevanta tester passerade lokalt: ägarkontroll vid profilredigering, ignorerade serverstyrda fält samt dolda och avvisade avstängda konton. | Skyddet kontrolleras både i kod och med automatiska regressionstester. |
| Kubernetes-rollout | Deploymenten var `Ready` med noll omstarter. Initcontainern för data-rättigheter avslutades med exitkod `0`. | Data-volymens rättigheter förbereds innan appen startar som användare `10001`. |

Den aktuella lösningen använder `Recreate` för deploymenten eftersom SQLite körs
med en `ReadWriteOnce`-volym. Det undviker att två poddar samtidigt försöker
använda samma databasvolym, men innebär ett kort planerat avbrott vid rollout.
En extern databas är därför ett långsiktigt förbättringsspår om applikationen
senare behöver flera repliker eller avbrottsfria deploymenter.

### Exempel: så tolkas en rad

Raden om SQL injection gäller äldre login-kod. MITRE-kopplingen hjälper oss att
förklara varför en sårbar webbapplikation kan vara en ingång till ett angrepp.
Den aktuella koden använder däremot parametriserade frågor och testsviten
kontrollerar skyddet. Därför står raden som **historiskt fynd, åtgärdat i
aktuell kod** - inte som en aktiv incident.

## Sammanfattande tabell

| Fynd eller kontroll | Evidens | MITRE ATT&CK-koppling | Status och defensiv uppföljning | Tilltro | TLP |
| --- | --- | --- | --- | --- | --- |
| SQL injection och felaktigt lösenordsflöde i äldre login-kod | Historisk säkerhetsrapport; aktuell kod och testsvit har hardening från Workshop 4 | [T1190 Exploit Public-Facing Application](https://attack.mitre.org/techniques/T1190/) | **Historiskt fynd, åtgärdat i aktuell kod.** Behåll parametriserade frågor, modern hashverifiering och negativa autentiseringstester. Den äldre rapportens status "Öppen" är inte aktuell driftbedömning. | Hög | CLEAR |
| IDOR/bristande ägarkontroll vid profilåtkomst | Historisk rapport; `routes.py` kontrollerar nu användare mot profil för ändring och e-postförhandsvisning | Ingen entydig ATT&CK-teknik; applikationsauktorisationsbrist | **Historiskt fynd, åtgärdat i aktuell kod.** Behåll negativa tester för andra användares resurser och logga upprepade nekade försök. | Hög | CLEAR |
| Hårdkodad `SECRET_KEY`, seed-data och risk för hemligheter i kod/historik | Historisk rapport samt kurslabb om Git-historik och remote-branches | [T1552.001 Credentials In Files](https://attack.mitre.org/techniques/T1552/001/) | **Åtgärdat i nuvarande konfiguration, men förebyggande kontroll behövs fortsatt.** Använd GitHub/Kubernetes-secrets, secret scanning och rotation om ett värde har exponerats. | Medel till hög | CLEAR; verkliga hemligheter är RED |
| CSRF- och cookiehardening | Historisk rapport; Workshop 4 beskriver CSRF-skydd samt säkrare sessions- och cookie-inställningar | Ingen direkt ATT&CK-teknik; skydd mot webbförsök snarare än en teknik | **Åtgärdat i aktuell Workshop 4-version.** Verifiera skyddet i regressionssviten och vid framtida formulär. | Hög | CLEAR |
| Jinja-injektion i e-postsignaturens förhandsvisning | Säkerhetsrapportens tillägg och aktuell `routes.py`: endast fem tillåtna variabler ersätts utan dynamisk Jinja-rendering | [T1059.004 Unix Shell](https://attack.mitre.org/techniques/T1059/004/) är endast en möjlig följd om template-injektion leder till kommandokörning; sådant är inte visat här | **Historiskt fynd, åtgärdat i aktuell kod.** Behåll en allowlist, längdgräns och tester som avvisar övrig mallsyntax. De äldre rapporternas status och brutna kodlänkar bör rättas i en separat review. | Hög för åtgärdsstatus; medel för hypotetisk ATT&CK-följd | CLEAR |
| Signerade images, SBOM och policykontroll minskar supply-chain-risk | Workshop 4-verifiering: Cosign-signatur och CycloneDX-attestering är kontrollerade; policyn nekar osignerad image | [T1195.002 Compromise Software Supply Chain](https://attack.mitre.org/techniques/T1195/002/) | **Åtgärdad och verifierad.** Fortsätt kontrollera image-digest, attestering och policy vid varje rollout. | Hög | CLEAR |
| Trivy CronJob och Discord-rapportering i Kubernetes | Fajks Discord-uppdatering och infra-repots arbetssammanfattning 2026-10-01 bekräftar Secret, RBAC, CronJob och testat larmflöde. PR #25 innehåller dock endast dokumentation, inte Kubernetes-manifest. | [T1195.002 Compromise Software Supply Chain](https://attack.mitre.org/techniques/T1195/002/) | **Driftverifierad men ej reproducerbar från Git.** Dokumentera ägare, schema, image/digest-policy, alertkriterier och återställning utan webhook eller andra hemligheter. Detta är en dokumentations- och driftlucka, inte bevis för att kontrollen saknas. | Medel | CLEAR; manifest och webhookdetaljer är AMBER+STRICT |
| Kurslabb: Git-historik, branches, IDOR och SQL injection | Individuella och gemensamma flaggsammanfattningar | [T1552.001 Credentials In Files](https://attack.mitre.org/techniques/T1552/001/) samt [T1190 Exploit Public-Facing Application](https://attack.mitre.org/techniques/T1190/) | **Labbfynd, inte Team 2-incident.** Lärande: skanna all Git-historik och referenser, kontrollera objektägarskap server-side och använd parametriserad SQL. | Hög för labbet | CLEAR; flaggvärden och accessdata är RED |

## APP-07 - Riskregister för säkerhetsfynd

Detta riskregister gör APP-07:s bedömningsgrund tydlig. Det bygger endast på
sanerade rapporter, kod, tester och verifierad driftstatus. En rad visar inte
att ett intrång har skett. Den visar vad teamet har observerat, varför det är
relevant och hur risken ska hanteras defensivt.

| Fynd | Observation och bevis | Möjlig påverkan | Osäkerhet och begränsning | Rekommenderad riskreducering | Status |
| --- | --- | --- | --- | --- | --- |
| Historisk SQL injection och felaktigt lösenordsflöde | Äldre säkerhetsrapport beskriver bristen. Aktuell kod och testsvit har hardening från Workshop 4. | En sårbar variant skulle kunna ge obehörig åtkomst eller påverka data. | Det historiska beteendet ska inte likställas med ett intrång. Den aktuella koden är verifierad i projektet, men någon extern penetrationstestning av skarp miljö har inte gjorts inom detta underlag. | Behåll parametriserade frågor, modern hashverifiering och negativa autentiseringstester vid varje relevant ändring. | Historiskt fynd, åtgärdat i aktuell kod. |
| Historisk IDOR vid profilåtkomst | Historisk rapport samt aktuell `routes.py`, där åtkomst kontrolleras mot rätt användare vid profiländring och e-postförhandsvisning. | En brist skulle kunna ge åtkomst till eller ändring av en annan användares uppgifter. | Bedömningen utgår från aktuell kod och tester, inte från observation av missbruk i drift. | Behåll negativa tester för andra användares resurser och följ upp upprepade nekade åtkomstförsök i loggar. | Historiskt fynd, åtgärdat i aktuell kod. |
| Historiska hemligheter i kod eller Git-historik | Historisk rapport och kurslabb visar riskbilden. Aktuell lösning använder GitHub- och Kubernetes-secrets. | Exponerade värden kan missbrukas för obehörig åtkomst tills de återkallas eller roteras. | Detta underlag fastställer inte om ett historiskt värde någonsin användes i skarp drift. Råa hemligheter ska inte granskas i det publika repot. | Fortsätt med secret scanning, säker Secret-hantering och rotation eller återkallning om exponering misstänks. | Åtgärdat i aktuell konfiguration; förebyggande kontroll behövs fortsatt. |
| Signerade images, SBOM och policykontroll | Workshop 4-verifiering visar Cosign-signatur, CycloneDX-attestering och en policy som nekar osignerade images. | Utan dessa kontroller ökar risken att en felaktig eller manipulerad container-image driftsätts. | Kontrollen var verifierad vid testet; policyidentitet och CI-flöde behöver följas när workflow eller releaseprocess ändras. | Kontrollera digest, attestering och policybeslut vid varje rollout och uppdatera policyn kontrollerat vid ändrat CI-flöde. | Åtgärdad och verifierad. |
| Trivy CronJob och Discord-rapportering är inte reproducerbara från Git | Fajks driftbekräftelse och infra-repots arbetssammanfattning 2026-10-01 bekräftar Secret, RBAC, CronJob och testat larmflöde. PR #25 innehåller endast dokumentation. | Om kontrollen behöver återställas eller granskas saknas ett versionshanterat underlag för hela installationen. Det kan försvåra upptäckt och uppföljning av supply-chain-risker. | Kontrollen är driftverifierad, men publikt repo saknar manifest och råa skannerrapporter. Detta är en dokumentations- och driftlucka, inte bevis för att kontrollen saknas. | Dokumentera ägare, schema, skanningsomfattning, larmkriterier och återställning. Versionshantera icke-hemliga manifest eller IaC efter review. | Öppet uppföljningsbehov. |
| Äldre rapporter kan ge en missvisande nulägesbild | Äldre rapporter har öppna statusmarkeringar eller kodlänkar som inte alltid speglar den aktuella versionen. | Teamet kan prioritera en redan åtgärdad brist fel eller missa vad som faktiskt behöver följas upp. | En separat dokumentgranskning krävs för att avgöra vilka äldre länkar och statusrader som ska ändras. | Märk historiska fynd tydligt, länka till verifierad aktuell kod och rätta brutna länkar efter review. | Öppet dokumentationsbehov. |

Alla rader i registret är **TLP:CLEAR** i sanerad form. Råa skannerrapporter,
runtime-detaljer, webhookar, tokens och andra autentiseringsuppgifter ska
fortsätta hanteras utanför publikt Git enligt TLP-rutinen nedan.

## Vad betyder statusen i praktiken?

| Status | Praktisk betydelse |
| --- | --- |
| **Historiskt fynd, åtgärdat i aktuell kod** | Bristen fanns i tidigare kod och är viktig att förstå, men den verifierade aktuella koden har en kontroll som motverkar den. |
| **Åtgärdad och verifierad** | Kontrollen finns, är mergad och har verifierats med exempelvis CI, policykontroll eller livekontroll. |
| **Driftverifierad men ej reproducerbar från Git** | Kontrollen fungerar i Kubernetes, men teamet behöver dokumentera eller versionshantera installationen så att den kan granskas och återställas. |
| **Labbfynd** | Fyndet kommer från kursmiljön och ska inte beskrivas som en incident i Team 2:s applikation. |

## Vad menar vi med Threat Intelligence?

I den här kursen betyder Threat Intelligence att teamet förvandlar observationer
till ett tydligt beslutsunderlag. Vi frågar inte bara "finns en brist?", utan
också:

- vilket angriparbeteende är relevant,
- vilken kontroll begränsar risken,
- hur verifierar vi att kontrollen fungerar, och
- vilken information kan delas utan att skapa ny risk?

Det finns ingen hotaktörsattribution i dokumentet. MITRE ATT&CK används som ett
gemensamt språk för beteenden och försvar, inte som bevis för ett intrång.

## Threat intelligence-bedömning

| Källtyp | Bidrag | Bedömning |
| --- | --- | --- |
| Aktuell applikationskod och tester | Visar skydd som finns i mergad version | Primärkälla med hög tilltro |
| Pull requests, Actions och driftkontroller | Visar att ändringar byggts, deployats och testats | Hög tilltro när kod, CI och livekontroll stämmer |
| Äldre säkerhetsrapporter | Beskriver ursprungliga fynd och prioritering | Medel till hög tilltro; status måste jämföras med aktuell kod |
| Kurslabb | Ger kontrollerade exempel på upptäckt, angreppsyta och åtgärdsbehov | Hög tilltro för labbresultat, inte för verklig attribution |
| MITRE ATT&CK och TLP | Gemensamt språk för teknik respektive delning | Ramverk, inte incidentbevis |

Ingen hotaktörsattribution görs i detta underlag. Arbetet bygger i stället på
kontext: vilket beteende är relevant, vilken kontroll begränsar risken och
vilken signal behöver teamet följa upp?

## TLP-rutin

Eftersom repot är publikt måste innehåll som läggs här vara sanerat.

Rapporten är därför märkt **TLP:CLEAR**. Det innebär inte att all
säkerhetsinformation kan delas öppet: råa skannerrapporter, runtime-detaljer och
autentiseringsuppgifter hanteras enligt de striktare nivåerna i tabellen nedan.

| Nivå | Användning i Team 2 |
| --- | --- |
| **TLP:CLEAR** | Sanerade risk- och statusdokument som denna tabell. Kan delas med utbildaren och lagras publikt. |
| **TLP:AMBER** | Detaljerade interna granskningsunderlag, exempelvis skannerresultat eller loggutdrag. Dela bara med Team 2 och utbildaren. |
| **TLP:AMBER+STRICT** | Källmaterial som inte ska spridas utanför mottagargruppen, exempelvis runtime-specifika CronJob- och åtkomstuppgifter. |
| **TLP:RED** | Webhooks, nycklar, tokens, flaggvärden och andra autentiseringsuppgifter. Aldrig i Git, issues eller Discord. |

## Rekommenderad fortsättning

1. Komplettera APP-07 med ett sanerat riskregister: evidens, status, ATT&CK-koppling, osäkerhet och ansvarig kontroll.
2. Dokumentera Trivy/Discord-installationen som driftbevis utan hemligheter och gör den reproducerbar som manifest eller IaC när teamet är redo.
3. Markera de äldre säkerhetsrapporterna som historiska eller uppdatera deras status och kodlänkar efter en separat granskning.
4. Fortsätt kontrollera att nya images är signerade, har SBOM/attestering och att policykontrollen nekar osignerade images.

## Referenser

- [MITRE ATT&CK Enterprise](https://attack.mitre.org/)
- [MITRE: Exploit Public-Facing Application](https://attack.mitre.org/techniques/T1190/)
- [MITRE: Credentials In Files](https://attack.mitre.org/techniques/T1552/001/)
- [MITRE: Compromise Software Supply Chain](https://attack.mitre.org/techniques/T1195/002/)
- [FIRST: Traffic Light Protocol 2.0](https://www.first.org/tlp/)
- [Sakerhetsrapport](security-report.md)
- [Sakerhetsrapport - tillagg](security-report-addendum.md)
- [Supply-chain-skanner](workshop4_supply_chain_scanner.md)
- [Produktbacklog](product_backlog.md)
