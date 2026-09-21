# Produktbacklog - Company Website

Senast uppdaterad: 2026-09-21

| ID | Prioritet | Status | Uppgift | Klart när |
| --- | --- | --- | --- | --- |
| APP-01 | Hög | Done | Etablera publikt GitHub-repo med branch protection | Repot är publikt, teamet har åtkomst och `main` kräver två godkännanden |
| APP-02 | Hög | Done | Driftsätt applikationen till K3s via GitHub Actions | En fullständig workflow-körning är grön och podden är `Running` |
| APP-03 | Hög | Done | Konfigurera Headscale-åtkomst för CI | Ephemeral runner skapas med rätt tagg och när K3s API på TCP 6443 |
| APP-04 | Hög | Done | Gör GHCR-imagen tillgänglig för K3s | Paketet är publikt och imagen kan hämtas utan registry-credential |
| APP-05 | Hög | To do | Analysera placeholder-flaggor i den egna kursmiljön | Observationer är verifierade och dokumenterade utan att exponera flaggvärden |
| APP-06 | Hög | To do | Genomför defensiv analys av den skarpa kursmiljön | Endast godkända kursmål analyseras och resultatet dokumenteras |
| APP-07 | Medel | To do | Dokumentera fynd, risk och rekommenderad åtgärd | Varje fynd har bevis, konsekvens, osäkerhet och defensivt åtgärdsförslag |
| APP-08 | Medel | To do | Gör image-deployment reproducerbar med unik image-tagg | Varje commit deployar en identifierbar image och kan återställas |
| APP-09 | Medel | To do | Anpassa rolloutstrategin för en nod med `hostPort` | Ny deployment kan ersätta gammal pod utan portkonflikt |
| APP-10 | Medel | In progress | Gör Headscale-policyinstallationen reproducerbar | Policyfilen installeras med `root:headscale`, läge `640`, valideras och laddas om |
| APP-11 | Låg | To do | Följ upp varningar från GitHub Actions | Node-runtime och authkey-varning är bedömda och dokumenterade |
| APP-12 | Låg | To do | Dokumentera rutin för rotation av Headscale API-nyckel | Ägare, giltighetstid, rotation och återkallning framgår utan hemliga värden |

## Statusförklaring

- `To do`: inte påbörjad.
- `In progress`: arbete eller verifiering återstår.
- `Done`: mergad och verifierad.

Backlogfilen synkroniseras inte automatiskt med GitHub Issues.

## Öppna GitHub Issues

- APP-05: [Issue #6](https://github.com/itsx25-team2/company-website/issues/6)
- APP-06: [Issue #8](https://github.com/itsx25-team2/company-website/issues/8)
- APP-07: [Issue #10](https://github.com/itsx25-team2/company-website/issues/10)
- APP-08: [Issue #3](https://github.com/itsx25-team2/company-website/issues/3)
- APP-09: [Issue #9](https://github.com/itsx25-team2/company-website/issues/9)
- APP-10: [Issue #4](https://github.com/itsx25-team2/company-website/issues/4)
- APP-11: [Issue #7](https://github.com/itsx25-team2/company-website/issues/7)
- APP-12: [Issue #5](https://github.com/itsx25-team2/company-website/issues/5)
