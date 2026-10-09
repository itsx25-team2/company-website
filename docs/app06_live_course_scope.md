# APP-06 - Scope och arbetssätt för skarp kursmiljö

**Datum:** 2026-10-09
**Klassificering:** TLP:CLEAR, sanerad för projektets publika repo
**Status:** Scope behöver bekräftas innan nya moment genomförs. APP-06 är
fortsatt öppen.

## Syfte

APP-06 omfattar endast analysmoment som utbildaren uttryckligen har godkänt
för kursens skarpa miljö. Dokumentet ska förhindra att gruppen blandar ihop
lokal analys, tidigare kurslabb och aktiva moment mot en körande tjänst.

## Nuvarande bedömning

Tidigare arbetssammanfattningar visar att Team 2 har genomfört godkända
kursmoment i flera labbmiljöer. De utgör värdefullt historiskt underlag, men
de räcker inte ensamma som godkännande för nya kontroller i en aktiv miljö.

Inga nya aktiva analyser, flagginskick eller förändringar av kursmiljön har
gjorts för APP-06 under denna uppföljning.

## Scope som ska bekräftas före arbete

| Fråga | Krävs före start | Status |
| --- | --- | --- |
| Vilken miljö, tjänst eller uppgift omfattas? | Namn och avgränsning från utbildaren eller aktuellt kursmaterial. | Ej dokumenterat här ännu |
| Vad är målet? | Defensiv frågeställning, exempelvis verifiera ett tidigare fynd eller bedöma en kontroll. | Ej dokumenterat här ännu |
| Vilka åtgärder är tillåtna? | Tydliga gränser för läsande kontroller, kontoanvändning och eventuella verktyg. | Ej dokumenterat här ännu |
| Vad är förbjudet? | Exempelvis ändringar, massförfrågningar, åtkomst till andra deltagares data eller publicering av resultat. | Grundregel dokumenterad; specifik scope saknas |
| När avbryter vi? | Avvikande svar, osäker behörighet, oväntad påverkan eller moment utanför instruktionen. | Gäller alltid |
| Var dokumenteras resultatet? | Sanerad sammanfattning med evidens, risk, osäkerhet och defensiv rekommendation. | Definierat |

## Säker arbetsrutin efter scope-bekräftelse

1. Dokumentera den godkända uppgiften och stoppgränserna innan första
   kontrollen.
2. Börja med den minst ingripande observation som kan besvara frågan.
3. Avbryt om resultatet kräver en åtgärd som inte uttryckligen ingår i scope.
4. Hantera flaggor, tokens, credentials och råa svar som känsligt underlag;
   publicera dem inte i Git, Issues, Discord eller sammanfattningar.
5. Dokumentera endast vad observationen betyder för risk, upptäckt,
   riskreducering eller uppföljning.
6. Låt gruppen granska resultatet innan ett eventuellt inlämnings- eller
   rapporteringssteg.

## Definition of Done för APP-06

APP-06 kan stängas först när:

- utbildarens scope är dokumenterat,
- analysen är genomförd inom den scope som bekräftats,
- resultat och osäkerheter är sanerat dokumenterade, och
- inga flaggvärden eller hemligheter har publicerats.

## Referenser

- [APP-05 - Defensiv analys av lokal kursapplikation](app05_local_course_analysis.md)
- [MITRE ATT&CK, Threat Intelligence och TLP](mitre_ti_tlp_summary_2026-10-05.md)
- [Teamets arbetssammanfattning 2026-09-24 i infra-repot](https://github.com/itsx25-team2/kurs6-team2-infra/blob/main/docs/team_work_summary_2026-09-24.md)
