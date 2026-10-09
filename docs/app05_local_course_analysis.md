# APP-05 - Defensiv analys av lokal kursapplikation

**Datum:** 2026-10-09
**Klassificering:** TLP:CLEAR, sanerad för projektets publika repo
**Status:** Redo för teamgranskning. Issue APP-05 stängs först efter merge och
verifiering.

## Syfte och avgränsning

Detta dokument samlar redan verifierade observationer från Team 2:s godkända
lokala kursmiljö. Målet är att beskriva risk och försvar, inte att återge hur
en sårbarhet kan utnyttjas.

Följande ligger utanför denna analys:

- flaggvärden, credentials, tokens och nycklar,
- nya aktiva tester eller försök mot kursmiljön,
- Team 2:s produktions- eller K3s-miljö, och
- den skarpa kursmiljön som hanteras separat i APP-06.

## Underlag och arbetssätt

Analysen bygger på tidigare, godkända kursmoment och sanerade
arbetssammanfattningar. Inget nytt angreppsmoment har genomförts för detta
dokument. Observationerna har översatts till ett defensivt format med
spårbar evidens, risk, osäkerhet och rekommenderad kontroll.

## Sammanställning av observationer

| Fyndkategori | Sanerad observation och evidens | Risk | Osäkerhet | Defensiv rekommendation |
| --- | --- | --- | --- | --- |
| Känsliga artefakter i lokal infrastrukturdata | Tidigare kursanalys visade att state- eller backupmaterial kan innehålla värden som inte hör hemma i vanlig källkod. | En person som får åtkomst till artefakten kan få information som underlättar vidare obehörig åtkomst. | Underlaget visar labbets riskbild, inte att Team 2:s driftmiljö har exponerats. | Skydda state i remote backend, använd strikt IAM, ignorera lokala statefiler i Git och rotera exponerade värden. |
| Historik och extra Git-referenser | Tidigare kursanalys visade att raderat innehåll kan finnas kvar i äldre commits eller avvikande referenser. | Hemligheter eller olämpligt innehåll kan vara åtkomligt trots att det saknas på huvudbranchen. | Resultatet gäller kursmaterialets historik och ska inte tolkas som en incident i Team 2:s repo. | Skanna hela historiken, branches, tags och pull request-referenser. Rotera exponerade värden; enbart radering räcker inte. |
| Bristande objektbehörighet | Kursunderlaget visade att inloggning inte automatiskt innebär behörighet till varje enskild resurs. | En användare kan annars få läsa eller ändra en annan användares data. | Observationen är ett kontrollerat labbfynd, inte bevis på missbruk i drift. | Kontrollera ägarskap eller explicit behörighet på serversidan för varje resurs och testa nekade scenarier. |
| Otillräcklig indatahantering i tjänster | Kursmaterialet visade att användarstyrd indata kan nå känsliga funktioner om den inte valideras och avgränsas. | Felaktig indatahantering kan ge oavsiktlig åtkomst till tjänstens resurser. | Detta dokument beskriver mönstret på defensiv nivå och innehåller inga reproduktionssteg. | Använd strikt allowlist-validering, separera data från kommando- eller frågetolkning och kör tjänster med minsta privilegium. |
| Osäkra databasfrågor i labbapplikation | Tidigare godkänt kursmoment bekräftade att felaktigt byggda databasfrågor kan påverka autentiserings- och dataskydd. | En brist kan ge obehörig åtkomst eller felaktiga databasresultat. | Analysen gäller kurslabbets tidigare beteende och är inte en aktuell bedömning av Team 2:s hardened applikation. | Använd parametriserade frågor, modern lösenordshantering, begränsade databasbehörigheter och negativa regressionstester. |

## MITRE ATT&CK-koppling

MITRE-kopplingarna beskriver relevanta angriparbeteenden och används inte som
bevis för ett intrång:

- [T1552.001 - Credentials In Files](https://attack.mitre.org/techniques/T1552/001/)
  är relevant för statefiler, historik och andra artefakter som kan innehålla
  känsliga värden.
- [T1190 - Exploit Public-Facing Application](https://attack.mitre.org/techniques/T1190/)
  är relevant när ett webb- eller tjänstegränssnitt har brister i indatahantering
  eller åtkomstkontroll.

## Definition of Done för APP-05

| Klarkriterium från Issue #6 | Bedömning |
| --- | --- |
| Observationerna är verifierade | Ja. Sammanställningen hänvisar till tidigare godkända och dokumenterade kursmoment. |
| Risk och defensiv rekommendation är dokumenterade | Ja. Varje rad beskriver risk, osäkerhet och rekommenderad kontroll. |
| Inga flaggvärden eller hemligheter publiceras | Ja. Dokumentet innehåller endast sanerade observationer och länkar till sanerade källor. |

## Källor

- [Jonnys sanerade flaggsammanfattning i infra-repot](https://github.com/itsx25-team2/kurs6-team2-infra/blob/main/members/itzmejonny92/flaggar_individuell_sammanfattning_2026-09-24.md)
- [Teamets arbetssammanfattning 2026-09-24 i infra-repot](https://github.com/itsx25-team2/kurs6-team2-infra/blob/main/docs/team_work_summary_2026-09-24.md)
- [MITRE ATT&CK, Threat Intelligence och TLP](mitre_ti_tlp_summary_2026-10-05.md)

## Nästa steg

Låt teamet granska att avgränsningen stämmer med kursens lokala miljö. Efter
review kan APP-05 uppdateras till `Done` i backloggen och Issue #6 stängas via
en separat pull request. APP-06 ska däremot ligga kvar tills utbildarens
godkända scope för skarp miljö är dokumenterat.
