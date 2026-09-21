# Individuell Arbetssammanfattning - Jonny Nguyen - 2026-09-21

## Mitt fokus

Jag arbetade med att etablera Team 2:s applikationsrepo och få hela kedjan från
GitHub Actions till K3s att fungera via Headscale.

## Mitt arbete

- Deltog i skapandet av GitHub-organisationen och det publika applikationsrepot.
- Konfigurerade teamatkomst, branch protection, Secrets och Variables.
- Verifierade K3s-installationen och applicerade CI/CD-behörigheter.
- Felsökte Headscale API-anrop, subnet-route och ACL-policy.
- Identifierade att policyfilens ägare hindrade Headscale från att läsa den.
- Korrigerade rättigheterna, validerade policyn och verifierade omladdningen.
- Felsökte `ImagePullBackOff` och gjorde GHCR-paketet publikt.
- Verifierade podd, PVC, health check och en grön end-to-end-deployment.
- Skapade gemensam dokumentationsstruktur, backlog och medlemsmappar.

## Vad jag lärde mig

- Filrättigheter måste bedömas utifrån vilken användare tjänsten faktiskt kör
  som, inte bara om root kan läsa filen.
- En godkänd route i Headscale är inte tillräcklig om den aktiva policyn inte
  har laddats korrekt.
- CI/CD-felsökning blir tydligare när varje lager verifieras separat: build,
  autentisering, routing, K3s API, image pull och workload health.
- `hostPort` på ett ennodskluster påverkar hur en rolling update kan genomföras.

## Nästa steg

- Analysera Git-historik och remote branches i kursmiljön.
- Fortsätta den defensiva analysen av webbapplikationen.
- Dokumentera varje observation med risk, bevis och rekommenderad åtgärd.
- Följa upp reproducerbar policyinstallation och deployment med unika
  image-taggar.

Inga hemliga värden eller flaggvärden dokumenteras i denna fil.
