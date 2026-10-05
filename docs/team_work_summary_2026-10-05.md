# Team 2 - arbetssammanfattning 2026-10-05

## Närvaro

- Närvarande: Jonny Nguyen, Fajk Zhupa, Lars Torngren och Wilibroad Ngebi.
- Frånvarande: Tim Rundquist och Amin Mahamoud.

## Dagens mål

Dagens arbete fokuserade på Workshop: MITRE ATT&CK-mappning av fynd från
vecka 4-7, Threat Intelligence-analys och TLP-klassificering. Målet var att
sammanställa applikationens historiska fynd, nuvarande skydd och nästa
förbättringssteg på ett pedagogiskt och säkert sätt.

## Genomfört arbete

1. Company-website-repots säkerhetsrapporter, kod, tester, backlog,
   mergehistorik och tidigare verifieringar gick igenom.
2. Historiska webbbrister jämfördes med den aktuella koden för att skilja
   gamla fynd från nuvarande status.
3. En ny pedagogisk MITRE/TI/TLP-sammanställning skapades med förklaring av
   ATT&CK, status, tilltro och informationsklassning.
4. SQL injection, IDOR, hemlighetshantering, CSRF/cookies, Jinja-injektion,
   SBOM, image-signering och supply-chain-kontroller analyserades defensivt.
5. Fajks Discord-uppdatering bekräftade att Discord-webhook, Secret, RBAC,
   Trivy CronJob och en testad engångskörning finns i K3s. Inga hemliga värden
   dokumenterades.
6. Infra-repots PR #78 granskades som kompletterande evidens. Den
   arbetssammanfattningen bekräftar att Trivy/Discord-flödet testats i K3s.
   PR #25 innehåller däremot bara dokumentation och inte de manifest som
   behövs för att återskapa kontrollen från Git.

## Resultat

- Den nya sammanställningen finns i
  [MITRE ATT&CK, Threat Intelligence och TLP - company-website](mitre_ti_tlp_summary_2026-10-05.md).
- Äldre säkerhetsrapporter behandlas som historiska källor. Aktuell kod och
  verifieringar visar att de centrala Workshop 4-kontrollerna är införda.
- Signerade images, SBOM/attestering och policykontroll är dokumenterade som
  verifierade skydd mot supply-chain-risk.
- Trivy/Discord är verifierad i drift, men icke-hemliga manifest och en
  återställningsrutin behöver versionshanteras för att kontrollen ska kunna
  granskas och återskapas utan att hemligheter hamnar i Git.
- Ingen applikationskod, Kubernetes-konfiguration eller live-data ändrades
  under dagens dokumentationsarbete.

## Nästa steg

- Låt gruppen granska MITRE/TI/TLP-sammanställningen innan den commitas.
- Följ upp APP-07 med det sanerade riskregistret och koppla nya fynd till
  evidens, status, ATT&CK, tilltro och TLP.
- Planera en säker, reproducerbar dokumentation av Trivy/Discord utan
  webhook, tokens eller andra autentiseringsuppgifter.
- Rätta de äldre säkerhetsrapporternas status och brutna kodlänkar i en
  separat, granskad ändring.

## Säkerhet

Inga flaggvärden, lösenord, tokens, nycklar, Discord-webhooks eller
känsliga runtime-detaljer har lagts i dokumentationen.
