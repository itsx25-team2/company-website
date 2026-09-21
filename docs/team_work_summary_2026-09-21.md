# Teamsammanfattning - 2026-09-21

## Fokus

Dagens arbete fokuserade på att slutföra Workshop 3:s tekniska setup och skapa
en fungerande CI/CD-kedja från GitHub till K3s via Headscale.

## Genomfört arbete

- Skapade GitHub-organisationen `itsx25-team2` och applikationsrepot.
- Konfigurerade teamatkomst och branch protection med två approvals.
- Verifierade primary-instansens resurser, internetatkomst och K3s.
- Applicerade RBAC för GitHub-deployern och skapade begränsad kubeconfig.
- Skapade Headscale-användaren `github-ci` och konfigurerade CI-taggen.
- Lade in GitHub Secrets och Variables utan att exponera deras värden.
- Publicerade applikationskoden och containerimagen.
- Felsökte Headscale API-nyckelns radbrytning och återkallade den felaktiga
  nyckeln.
- Identifierade att policyfilen var `root:root` med läge `640`, vilket hindrade
  Headscale från att läsa den.
- Korrigerade filen till `root:headscale`, validerade policyn och laddade om
  Headscale utan omstart.
- Verifierade subnet-route och TCP 6443 från GitHub-runnern till K3s.
- Åtgärdade ett privat GHCR-paket och en fastnad `ImagePullBackOff`-podd.
- Verifierade `Running` podd, bunden PVC och fungerande `/healthz`.
- Genomförde en helt godkänd GitHub Actions-deployment.

## Verifierat slutläge

- GitHub Actions: godkänd.
- Headscale CI-anslutning: godkänd.
- K3s API-åtkomst: godkänd.
- Deployment: godkänd.
- Podd: `1/1 Running`.
- Databas: ansluten enligt health check.

## Nästa steg

- Börja med Git-historik och remote branches i den lokala kursmiljön.
- Fortsätt med defensiv analys av webbapplikationen.
- Dokumentera fynd utan hemligheter eller flaggvärden.
- Synkronisera GitHub Issues med produktbackloggen.
