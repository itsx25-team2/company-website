# Produktbacklog - Company Website

Senast uppdaterad: 2026-10-08

| ID | Prioritet | Status | Uppgift | Klart när |
| --- | --- | --- | --- | --- |
| APP-01 | Hög | Done | Etablera publikt GitHub-repo med branch protection | Repot är publikt, teamet har åtkomst och `main` kräver två godkännanden |
| APP-02 | Hög | Done | Driftsätt applikationen till K3s via GitHub Actions | En fullständig workflow-körning är grön och podden är `Running` |
| APP-03 | Hög | Done | Konfigurera Headscale-åtkomst för CI | Ephemeral runner skapas med rätt tagg och når K3s API på TCP 6443 |
| APP-04 | Hög | Done | Gör GHCR-imagen tillgänglig för K3s | Paketet är publikt och imagen kan hämtas utan registry-credential |
| APP-05 | Hög | To do | Analysera placeholder-flaggor i den egna kursmiljön | Observationer är verifierade och dokumenterade utan att exponera flaggvärden |
| APP-06 | Hög | To do | Genomför defensiv analys av den skarpa kursmiljön | Endast godkända kursmål analyseras och resultatet dokumenteras |
| APP-07 | Medel | Done | Dokumentera fynd, risk och rekommenderad åtgärd | Varje fynd har bevis, konsekvens, osäkerhet och defensivt åtgärdsförslag |
| APP-08 | Medel | Done | Gör image-deployment reproducerbar med unik image-tagg | Varje commit deployar en identifierbar image och rollback är dokumenterad och verifierad |
| APP-09 | Medel | Done | Ersätt `hostPort` med Kubernetes Ingress | En ny signerad version har rullats ut utan portkonflikt och ger HTTP `200` via Ingress |
| APP-10 | Medel | Done | Gör Headscale-policyinstallationen reproducerbar | Policyfilen installeras med `root:headscale`, läge `640`, valideras och laddas om |
| APP-11 | Låg | In progress | Följ upp varningar från GitHub Actions | Node-runtime och authkey-varning är bedömda och dokumenterade |
| APP-12 | Låg | Done | Dokumentera rutin för rotation av Headscale API-nyckel | Ägare, giltighetstid, rotation och återkallning framgår utan hemliga värden |
| APP-13 | Hög | Done | Signera och verifiera container-images | Pipelinen signerar med GitHub OIDC, policyn nekar osignerad image och godkänner Team 2:s signerade digest |

## Statusförklaring

- `To do`: inte påbörjad.
- `In progress`: arbete eller verifiering återstår.
- `Done`: mergad och verifierad.

Backlogfilen synkroniseras inte automatiskt med GitHub Issues.

## Öppna GitHub Issues

- APP-05: [Issue #6](https://github.com/itsx25-team2/company-website/issues/6)
- APP-06: [Issue #8](https://github.com/itsx25-team2/company-website/issues/8)
- APP-11: [Issue #7](https://github.com/itsx25-team2/company-website/issues/7)

## Slutförda GitHub Issues

- APP-08: [Issue #3](https://github.com/itsx25-team2/company-website/issues/3) är tekniskt slutförd genom verifierad rollback och återställning 2026-09-24.
- APP-09: [Issue #9](https://github.com/itsx25-team2/company-website/issues/9) är slutförd genom PR #16 och verifierad med HTTP `200` via Ingress.
- APP-07: [Issue #10](https://github.com/itsx25-team2/company-website/issues/10) stängdes automatiskt när PR #33 mergades 2026-10-07. Riskregistret beskriver bevis, påverkan, osäkerhet och defensiv riskreducering.
- APP-10: [Issue #4](https://github.com/itsx25-team2/company-website/issues/4) är dokumenterat och verifierat: Headscale-policyn använder `root:headscale`, läge `640`, validering och reload enligt [Workshop 3-status](workshop3_setup_status.md).
- APP-12: [Issue #5](https://github.com/itsx25-team2/company-website/issues/5) är dokumenterat i [rotationsguiden](headscale_api_key_rotation.md) med ansvar, giltighetstid, rotation, verifiering och återkallning utan nyckelvärden.

## Uppdatering 2026-10-08

- APP-07 är klar efter mergad och verifierad dokumentation i PR #33.
- APP-10 och APP-12 uppfyller sina klarkriterier enligt redan mergad
  projekt- och driftdokumentation.
- APP-05, APP-06 och APP-11 är fortsatt öppna eftersom deras respektive
  analys- eller uppföljningsarbete återstår.

## Verifiering 2026-09-28

- Workshop 4 är integrerad på `workshop4/instructor-sync` utan konflikt mot aktuell `main`.
- 19 tester, Docker-build, Bandit, `pip-audit`, YAML och Compose är verifierade.
- CycloneDX 1.5 genererades lokalt från imagen med 139 komponenter.
- `Application Checks`-körning 36404525054 lyckades.
- Flasks Kubernetes Secret är provisionerad utan att värdet lagrats i Git.
- PR #21 mergades som `3eeb631` efter två godkännanden.
- Första deploymentförsöket stoppades av en utgången Headscale API-nyckel.
- API-nyckeln roterades med 30 dagars giltighet och lagrades direkt som
  GitHub Secret utan att värdet visades eller sparades i Git.
- Deploymentkörning `36435042346`, försök 2, lyckades i samtliga steg.
- Kubernetes kör digest `sha256:469d57e...` med `1/1` redo repliker.
- `/healthz` gav `healthy`, databasen var ansluten och HTTP gav status `200`.
- Cosign-signaturen och CycloneDX-attesteringen verifierades externt mot
  Team 2:s `deploy.yml`, `main` och commit `3eeb631`.
- APP-11 förblir `In progress` för uppföljning av authkey-varningen och
  kommande Ubuntu 26-migrering.
- APP-12 är `In progress` tills rotationsguiden har granskats och mergats.

## Verifiering 2026-09-24

- Deploy-workflow `36001856279` byggde taggarna `latest` och `sha-9378fc7`.
- Kubernetes kör imagen med digest och pod-labeln matchar mergecommitten.
- `company-website.team2.arpa` gav HTTP `200` genom `ingress-nginx`.
- Cosign verifierade signaturen mot Team 2:s deploy-workflow på `main`.
- Policy-controller nekade en osignerad testimage och godkände den signerade
  Team 2-digesten med server-side dry-run.
- Rollback från digest `fd41c7c` till den tidigare signerade digesten
  `a8c98ac` lyckades. Applikationen var `Ready` och svarade med HTTP `200`.
- Deploymenten återställdes därefter till `fd41c7c`; även slutkontrollen gav
  `1/1` redo repliker och HTTP `200`.
- Deploy-workflow `36050751136` för senaste `main`-committen `f1bc921`
  lyckades. Rollouten slutfördes, testsviten gav `5 passed` och livekontrollen
  gav HTTP `200` med ansluten databas.
