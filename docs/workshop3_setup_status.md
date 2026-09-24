# Workshop 3-4 - setup och verifiering

Ursprungligt datum: 2026-09-21
Senast verifierad: 2026-09-24

## Resultat

Workshopens tekniska setup är genomförd och har byggts vidare med intern DNS,
Ingress, spårbara images och Cosign-enforcement.

| Område | Status | Verifiering |
| --- | --- | --- |
| Kursrepo | Klar | Utbildarens repository är klonat och originalremote finns kvar som `instructor` |
| GitHub-organisation | Klar | `itsx25-team2` är skapad och teamet har repositoryatkomst |
| Applikationsrepo | Klar | `itsx25-team2/company-website` är publikt |
| Primary | Klar | Instansen kör `e2-small` och har verifierad internetatkomst |
| K3s | Klar | K3s är aktivt utan Traefik och metrics-server |
| Kubernetes RBAC | Klar | Begränsad `github-deployer` kan hantera deployment, Service, PVC och Ingress |
| Kubeconfig | Klar | Begränsad kubeconfig lagras som GitHub Secret |
| Headscale CI-användare | Klar | `github-ci` finns och får en tillfällig CI-nod vid deployment |
| Headscale-policy | Klar | `tag:github-runner` får nå `10.0.2.3:6443` och ICMP |
| MagicDNS | Klar | `company-website.team2.arpa` löses till `10.0.2.3` |
| Ingress | Klar | `ingress-nginx` routar det interna namnet och svarar med HTTP `200` |
| CI/CD | Klar | Workflow `36001856279` byggde, signerade och driftsatte mergecommit `9378fc7` |
| GHCR | Klar | Imagen publicerades med `latest`, commit-SHA och oföränderlig digest |
| K3s workload | Klar | Podden är `Running`, PVC är `Bound` och rätt digest är driftsatt |
| Cosign | Klar | Signaturen verifierades mot GitHub Actions OIDC och rätt workflowidentitet |
| Image-policy | Klar | Osignerad image nekades och Team 2:s signerade digest godkändes |

## Viktiga lärdomar

- En policyfil med läge `640` måste ha gruppen `headscale` när tjänsten kör som
  `headscale:headscale`. `root:root` hindrade policyn från att laddas.
- `tailscale/github-action@v4` lägger redan till `--accept-routes`; flaggan ska
  inte skickas en andra gång via `args`.
- En privat GHCR-image ger `ImagePullBackOff` utan registry-credential.
- `hostPort: 80` på ett ennodskluster blockerade både rolling update och K3s
  LoadBalancer. Kubernetes Ingress tog bort den portkopplingen.
- Headscale `reload` läser endast om ACL-policyn i den installerade versionen.
  Ändringar i `extra_records` krävde en fullständig omstart.
- Ett lyckat signeringssteg räcker inte som bevis. Den publicerade digesten
  verifierades separat med Cosign innan enforcement aktiverades.

## GitHub Actions

Senast verifierad körning:

- Run ID: `36001856279`
- Commit: `9378fc752c0436052e4c90a3685c81f1dfdb88ce`
- Image digest: `sha256:a8c98ac624c8e03bce0b63c341f7df71509ad2669428ccd89f613774e721d2c0`
- Resultat: godkänd
- Metadata, build, Cosign-signering, Headscale, route, kubeconfig, Ingress och
  deployment passerade.

## Kvarvarande arbete

1. Dokumentera och verifiera rollback till en tidigare signerad digest i
   APP-08/issue #3.
2. Analysera applikationen i den egna godkända kursmiljön.
3. Dokumentera observationer, risker och defensiva åtgärdsförslag.
4. Genomför endast godkända moment mot den skarpa kursmiljön.
5. Följ framtida deployer och uppdatera Cosign-policyn kontrollerat om workflow
   eller branch ändras.

Hemliga värden och flaggvärden ska inte dokumenteras i detta repository.
